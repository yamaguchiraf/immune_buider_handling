# evaluation/utils.py
from Bio.PDB import PDBParser
from Bio.SVDSuperimposer import SVDSuperimposer
import numpy as np
from pathlib import Path

def load_structure(pdb_path, structure_id=None):
    """
    PDBをBio.PDB構造オブジェクトとして読み込む
    """
    parser = PDBParser(QUIET=True)
    return parser.get_structure(structure_id or Path(pdb_path).stem, str(pdb_path))

def get_ca_coords(chain):
    """
    鎖からCα座標を抽出
    """
    coords = []
    for res in chain:
        if res.get_id()[0] == " " and "CA" in res:
            coords.append(res["CA"].coord)
    return np.array(coords)


def superimpose_and_rmsd(coords_ref, coords_pred, return_coords=False):
    """
    2つの座標配列を重ね合わせてRMSDを返す
    return_coords=True の場合は (RMSD, transformed_pred) を返す
    """
    ref = np.asarray(coords_ref, dtype=float)
    pred = np.asarray(coords_pred, dtype=float)

    if ref.shape != pred.shape:
        raise ValueError("Coordinates must have matching shapes for RMSD calculation")

    sup = SVDSuperimposer()
    sup.set(ref, pred)
    sup.run()
    rms = sup.get_rms()
    if return_coords:
        return rms, sup.get_transformed()
    return rms


import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def plot_superposition(coords_ref, coords_pred, out_path="superimposed.png"):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")

    # 参照 (青)
    ax.plot(coords_ref[:,0], coords_ref[:,1], coords_ref[:,2], color="blue", label="Reference")

    # 整列後 (赤)
    ax.plot(coords_pred[:,0], coords_pred[:,1], coords_pred[:,2], color="red", label="Predicted")

    ax.legend()
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(f"[出力] 重ね合わせ図: {out_path}")
