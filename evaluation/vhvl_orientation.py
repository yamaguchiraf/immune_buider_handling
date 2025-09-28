# evaluation/vhvl_orientation.py
import numpy as np

def vhvl_orientation(refH, refL, predH, predL):
    """
    VH–VL の相対位置の指標を計算
    refH, refL, predH, predL: 各鎖のCα座標配列
    """
    def centroid(coords):
        return np.mean(coords, axis=0)

    ref_vec = centroid(refL) - centroid(refH)
    pred_vec = centroid(predL) - centroid(predH)

    # 距離差
    dist_diff = np.linalg.norm(ref_vec) - np.linalg.norm(pred_vec)

    # 角度差
    cos_theta = np.dot(ref_vec, pred_vec) / (np.linalg.norm(ref_vec) * np.linalg.norm(pred_vec))
    angle_diff = np.degrees(np.arccos(np.clip(cos_theta, -1.0, 1.0)))

    return {"VH-VL_dist": dist_diff, "VH-VL_angle": angle_diff}
