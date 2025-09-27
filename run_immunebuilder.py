from ImmuneBuilder import ABodyBuilder2
from pathlib import Path
import argparse

def read_fasta_dict(path):
    """
    FASTAファイルを {id: sequence} の辞書として読む
    >header の最初のトークンを key にする
    """
    records = {}
    header, seq_buf = None, []
    path = Path(path)

    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith(";"):
                continue
            if line.startswith(">"):
                if header:
                    records[header] = "".join(seq_buf).upper()
                header = line[1:].split()[0]  # 空白までをIDに
                seq_buf = []
            else:
                seq_buf.append(line)
        if header:
            records[header] = "".join(seq_buf).upper()
    return records

def main(fasta_file, hc_key, lc_key, out_pdb):
    # 1. FASTA読み込み
    seqs = read_fasta_dict(fasta_file)
    print("Sequences found:", list(seqs.keys()))

    # 2. HC/LC の抽出
    if hc_key not in seqs or lc_key not in seqs:
        raise ValueError(f"FASTAに {hc_key} または {lc_key} が見つかりません; {list(seqs.keys())} を確認してください")
    heavy_seq = seqs[hc_key]
    light_seq = seqs[lc_key]

    # 3. ImmuneBuilder 実行
    builder = ABodyBuilder2()
    antibody = builder.predict({"H": heavy_seq, "L": light_seq})

    # 4. 保存
    antibody.save(out_pdb)
    print(f"✅ Predicted Fab saved to {out_pdb}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run ImmuneBuilder ABodyBuilder2 with sequences from FASTA"
    )
    parser.add_argument("-i", "--input", required=True, help="入力FASTAファイル")
    parser.add_argument("-o", "--output", required=True, help="出力PDBファイル")
    parser.add_argument("-H", "--hc", required=True, help="Heavy chain FASTAヘッダID")
    parser.add_argument("-L", "--lc", required=True, help="Light chain FASTAヘッダID")
    args = parser.parse_args()

    main(args.input, args.hc, args.lc, args.output)
