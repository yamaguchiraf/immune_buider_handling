# evaluation モジュール

このディレクトリは **ImmuneBuilder の予測構造と実験構造の比較評価** を行うためのツール群です。  
RMSD 計算、IMGT 領域別評価、VH–VL 配向解析、残基ごとの誤差プロファイルなど、論文で報告された精度指標を再現できるように設計されています。

---

## ディレクトリ構成

```

evaluation/
├── __init__.py
├── rmsd.py              # RMSD 計算 (全体/領域別)
├── imgt.py              # IMGT 領域定義とマッピング
├── vhvl_orientation.py  # VH–VL 配向パラメータ計算
├── per_residue.py       # 残基ごとの誤差プロファイル
└── utils.py             # 共通ユーティリティ (PDB 読み込み、座標抽出、RMSD整列)

````

---

## 依存ライブラリ

- Python 3.10+
- [Biopython](https://biopython.org/) (Bio.PDB)
- NumPy
- [PyMOL](https://pymol.org/) （RMSD 計算に推奨）

インストール例:
```bash
pip install biopython numpy pymol-open-source
````

---

## 使い方

### 1. `main.py` を使った一括評価

`main.py` を実行すると、以下の処理を行います:

* 実験構造 (`--ref`) と予測構造 (`--pred`) を読み込み
* Heavy 鎖 RMSD を計算
* VH–VL 配向差を計算
* 残基ごとの Cα 誤差を出力

#### 実行例

```bash
python main.py --ref data/6B9Z_fv_ref.pdb --pred data/6B9Z_ib_pred.pdb --outdir results/6B9Z_eval
```

#### 出力例（report.txt）

```
== RMSD (全体, Heavy鎖のみ) ==
Heavy chain RMSD: 13.379 Å   ← 自作版（SVD整列, 未完成）

== RMSD (全体, PyMOL align) ==
Overall RMSD (PyMOL): 0.306 Å   ← 推奨値
```

---

## RMSD の目安

抗体構造モデリングにおける RMSD の一般的な解釈:

* **< 1.0 Å** : 実験構造とほぼ同等。非常に高精度。
* **1.0–2.0 Å** : 高精度モデル。フレームワーク領域ではこの範囲が目安。
* **2.0–3.0 Å** : まずまず良好。CDR ループではこの範囲も多い。
* **> 3.0 Å** : 大きなずれ。特に CDR-H3 は誤差が大きくなりやすい。

---

## PyMOL GUIでの重ね合わせ
PyMOLのターミナル上で
```
load data/6B9Z_fab.pdb, ref
load results/trastuzumab_ib.pdb, pred
align pred, ref
```

### PyMOL Tips
基本はPyMOLの独自コマンドしか使えないが、一部Linuxコマンドに似せたコマンドが使える
```
ls
pwd
cd <path>
```

## 注意点

* **自作版 RMSD** (`utils.superimpose_and_rmsd`) は残基対応を単純にインデックス順で行うため、残基番号のずれがあると値が不正確になります。**現時点では未完成**です。
* **PyMOL align による RMSD** は内部で配列アラインメントを行い、見た目通りに重ね合わせて RMSD を返すため、**こちらの値を参照することを推奨**します。

---

## 今後の拡張予定

* ANARCI 番号付けを統合し、CDR/Framework RMSD を自動出力
* IMGT 領域ごとの RMSD レポート生成
* 複数ペアの一括評価 (CSV 入力対応)
* Matplotlib を使った誤差プロファイル可視化

---

