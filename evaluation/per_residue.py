# evaluation/per_residue.py
import numpy as np

def per_residue_error(ref_chain, pred_chain):
    """
    残基ごとのCα距離をリストで返す
    """
    errors = []
    for r_ref, r_pred in zip(ref_chain, pred_chain):
        if "CA" in r_ref and "CA" in r_pred:
            dist = np.linalg.norm(r_ref["CA"].coord - r_pred["CA"].coord)
            errors.append((r_ref.get_id()[1], dist))
    return errors
