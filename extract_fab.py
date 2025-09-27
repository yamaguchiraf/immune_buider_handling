#!/usr/bin/env python3
from pathlib import Path
import argparse
from Bio.PDB import PDBParser, PDBIO, PPBuilder, Select
from ImmuneBuilder.sequence_checks import number_sequences

def read_fasta_dict(path: Path):
    """FASTAを {id: sequence} 辞書に変換"""
    recs = {}
    head, buf = None, []
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            s = line.strip()
            if not s or s.startswith(";"):
                continue
            if s.startswith(">"):
                if head:
                    recs[head] = "".join(buf).upper()
                head = s[1:].split()[0]
                buf = []
            else:
                buf.append(s)
    if head:
        recs[head] = "".join(buf).upper()
    return recs

def get_chain_sequences(structure):
    """PDBから各チェーンの一次配列を抽出"""
    ppb = PPBuilder()
    seqs = {}
    for ch in structure.get_chains():
        peptides = ppb.build_peptides(ch)
        if not peptides:
            continue
        seq = "".join(str(p.get_sequence()) for p in peptides)
        seqs[ch.id] = (ch, seq)
    return seqs

def map_subseq_to_resseqs(chain, pdb_seq, subseq):
    """pdb_seq中でsubseqが一致する区間のresseq集合を返す"""
    start = pdb_seq.find(subseq)
    if start < 0:
        return set()
    idx2resseq = [res.id[1] for res in chain if res.id[0] == " "]
    return set(idx2resseq[start:start+len(subseq)])

class RangeSelect(Select):
    def __init__(self, keep_map):
        self.keep_map = keep_map
    def accept_residue(self, residue):
        ch_id = residue.get_parent().id
        resseq = residue.id[1]
        return (ch_id in self.keep_map) and (resseq in self.keep_map[ch_id])

def unwrap_entry(entry):
    """ImmuneBuilder返り値の揺れを吸収して sequence文字列を返す"""
    if isinstance(entry, dict):
        return entry["sequence"]
    elif isinstance(entry, list):
        # ANARCI形式 [(pos, aa), ...]
        if all(isinstance(x, tuple) and len(x) == 2 for x in entry):
            return "".join(res for (_, res) in entry if res != "-")
        # [dict] 形式
        elif len(entry) > 0 and isinstance(entry[0], dict):
            return entry[0]["sequence"]
    raise TypeError(f"Unexpected entry format: {entry}")

def extract_fv(pdb_file: Path, fasta_file: Path, hc_key: str, lc_key: str, out_pdb: Path):
    # FASTAからHC/LC配列を読む
    seqs_raw = read_fasta_dict(fasta_file)
    if hc_key not in seqs_raw or lc_key not in seqs_raw:
        raise ValueError(f"FASTAに {hc_key} または {lc_key} がありません")
    seqs_in = {"H": seqs_raw[hc_key], "L": seqs_raw[lc_key]}

    # ImmuneBuilderの番号付け → Fvへ正規化
    numbered = number_sequences(seqs_in, scheme="imgt")
    if isinstance(numbered, dict):
        num_dict = numbered
    elif isinstance(numbered, list):
        num_dict = {chain_type: info for chain_type, info in numbered}
    else:
        raise TypeError(f"Unexpected return type from number_sequences: {type(numbered)}")

    h_trim = unwrap_entry(num_dict["H"])
    l_trim = unwrap_entry(num_dict["L"])

    # PDBをロードしてチェーン配列を抽出
    parser = PDBParser(QUIET=True)
    structure = parser.get_structure("antibody", str(pdb_file))
    chain_seq = get_chain_sequences(structure)

    # HC/LCに一致する区間を探索
    keep = {}
    for cid, (chain, pseq) in chain_seq.items():
        if "H" not in keep:
            resset = map_subseq_to_resseqs(chain, pseq, h_trim)
            if resset:
                keep[cid] = resset
                continue
        if "L" not in keep:
            resset = map_subseq_to_resseqs(chain, pseq, l_trim)
            if resset:
                keep[cid] = resset

    if not keep:
        raise RuntimeError("PDB中にFv領域が見つかりませんでした")

    io = PDBIO()
    io.set_structure(structure)
    io.save(str(out_pdb), RangeSelect(keep))
    print(f"✅ Fv extracted with number_sequences → {out_pdb}")

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Extract Fv (VH/VL) using ImmuneBuilder.number_sequences")
    ap.add_argument("-p", "--pdb", required=True, help="入力PDBファイル")
    ap.add_argument("-i", "--input", required=True, help="入力FASTAファイル（HC/LC）")
    ap.add_argument("-H", "--hc", required=True, help="FASTA中のHeavy chain ID")
    ap.add_argument("-L", "--lc", required=True, help="FASTA中のLight chain ID")
    ap.add_argument("-o", "--output", required=True, help="出力PDBファイル（Fvのみ）")
    args = ap.parse_args()

    extract_fv(Path(args.pdb), Path(args.input), args.hc, args.lc, Path(args.output))
