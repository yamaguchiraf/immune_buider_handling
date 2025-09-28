# evaluation/rmsd.py
import numpy as np
from .utils import superimpose_and_rmsd

def rmsd_by_region(coords_ref, coords_pred, region_labels):
    """
    領域ごとのRMSDを計算
    coords_ref, coords_pred: dict {region: [coords]}
    region_labels: list of region names
    """
    results = {}
    for region in region_labels:
        if region not in coords_ref or region not in coords_pred:
            continue
        X = np.array(coords_ref[region])
        Y = np.array(coords_pred[region])
        n = min(len(X), len(Y))
        if n > 3:
            rmsd = superimpose_and_rmsd(X[:n], Y[:n])
            results[region] = (rmsd, n)
    return results


from pymol import cmd

def pymol_rmsd(ref_pdb, pred_pdb, chain="all"):
    """
    PyMOL の align を使って RMSD を計算する
    ref_pdb: 参照PDBファイル
    pred_pdb: 比較PDBファイル
    chain: "all" なら全体、それ以外は "chain H" のように指定
    """
    cmd.reinitialize()  # PyMOL セッションをリセット

    # 構造読み込み
    cmd.load(ref_pdb, "ref")
    cmd.load(pred_pdb, "pred")

    # 鎖指定 (例: "chain H") か全体
    sel_ref = "ref" if chain == "all" else f"ref and {chain}"
    sel_pred = "pred" if chain == "all" else f"pred and {chain}"

    # PyMOL の align 実行
    # align は [RMSD, n_atoms, n_ref, n_mov, n_cycles, final_rms] を返す
    result = cmd.align(sel_pred, sel_ref)
    rmsd = result[0]

    return rmsd

