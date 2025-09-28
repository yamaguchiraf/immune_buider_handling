# PyMOLで重ね合わせGIFを作る手順まとめ

## 0. 準備

* **ImageMagick** をインストール

  ```bash
  sudo apt update
  sudo apt install imagemagick-6.q16
  convert -version   # 確認
  ```

---

## 1. 構造を読み込む

PyMOL コマンドラインで：

```pml
load data/6B9Z_fab_ref.pdb, ref
load data/6B9Z_fab_pred.pdb, pred
```

---

## 2. 色付け（見やすい配色）

論文や発表に使いやすい navy × salmon を採用：

```pml
set_color navyblue, [0.1, 0.2, 0.6]
set_color salmon, [0.95, 0.5, 0.5]

color navyblue, ref
color salmon, pred
```

---

## 3. 背景設定

* 透明背景で書き出したい場合：

  ```pml
  bg_color white
  set ray_opaque_background, off
  ```
* 白背景固定で良ければ：

  ```pml
  bg_color white
  ```

---

## 4. フレーム出力（ray + png, `.pml`スクリプト）

透明背景つき高解像度レンダリングを安定して出すには **スクリプト化**がおすすめ。
`make_movie.pml` を用意：

```pml
# 回転アニメーション用 120フレーム
mset 1 x120
util.mroll(1,120,1)

# Python ブロックで ray+png を各フレーム実行
python
from pymol import cmd
nframes = 120
for i in range(1, nframes+1):
    cmd.frame(i)
    cmd.ray(800, 800)  # 800x800 px, ray-traced
    cmd.png(f"rotation/frame{i:04d}.png")
python end
```

実行は PyMOL 内で：

```pml
@make_movie.pml
```

---

## 5. GIF 生成（ImageMagick）

白背景で安定させたい場合：

```bash
convert -delay 5 rotation/frame*.png -background white -alpha remove -dispose Background -loop 0 rotation.gif
```

* `-delay 5` → フレーム間隔 (0.05秒, 約20fps)
* `-loop 0` → 無限ループ
* `-background white -alpha remove` → 背景白で重ね書きを防ぐ
* `-dispose Background` → 各フレームごとにリセット

---

## 出力

* `rotation/frame0001.png` 〜 `frame0120.png` : 各フレーム画像
* `rotation.gif` : 最終的な回転アニメーション

