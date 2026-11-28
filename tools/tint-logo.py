# -*- coding: utf-8 -*-
"""
把徽标源图（灰线 + 黑底）染成「透明底 + 指定颜色」，输出顶栏用的 logo.png。

用法：
    python tools/tint-logo.py                      # 默认用主色 #5cff9d
    python tools/tint-logo.py 5cff9d 160           # 指定颜色 / 输出宽度

依赖：Pillow（`pip install pillow`）。DSH 自带的 Python 里已经有了。

原理：
  1. 亮度当透明度 —— 黑底变全透明，灰线按亮度变不透明（图像素稿专用）
  2. 用「最长连续行段/列段」切掉画面里的孤立杂点（源图右侧有个小方块）
  3. 裁到内容边界，加 3% 透明留白（防止图形尖端压在图片边上）
  4. 等比缩放到指定宽度，保存 PNG
"""
import os
import sys

import numpy as np
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "assets", "img", "logo-source.jpg")
OUT = os.path.join(ROOT, "assets", "img", "logo.png")

HEX = sys.argv[1] if len(sys.argv) > 1 else "5cff9d"
SIZE = int(sys.argv[2]) if len(sys.argv) > 2 else 128
RGB = tuple(int(HEX[i:i + 2], 16) for i in (0, 2, 4))


def longest_run(flags, max_gap=8):
    """返回最长的一段连续 True 的 (起, 止)，允许中间有 max_gap 的小空隙。"""
    best = (0, 0)
    start = last = None
    gap = 0
    for i, f in enumerate(flags):
        if f:
            if start is None:
                start = i
            last = i
            gap = 0
        elif start is not None:
            gap += 1
            if gap > max_gap:
                if (last - start) > (best[1] - best[0]):
                    best = (start, last)
                start = None
                gap = 0
    if start is not None and (last - start) > (best[1] - best[0]):
        best = (start, last)
    return best


def main():
    if not os.path.exists(SRC):
        sys.exit("找不到源图：%s" % SRC)

    a = np.array(Image.open(SRC).convert("L"), dtype=np.float32)

    mask = a > 40
    x0, x1 = longest_run(mask.any(axis=0))
    y0, y1 = longest_run(mask.any(axis=1))
    a = a[y0:y1 + 1, x0:x1 + 1]

    alpha = np.clip(a * (255.0 / max(a.max(), 1)), 0, 255)
    alpha[alpha < 10] = 0
    alpha = alpha.astype(np.uint8)

    h, w = alpha.shape
    rgba = np.zeros((h, w, 4), dtype=np.uint8)
    rgba[..., 0], rgba[..., 1], rgba[..., 2] = RGB
    rgba[..., 3] = alpha

    img = Image.fromarray(rgba, "RGBA").crop(Image.fromarray(rgba, "RGBA").getbbox())
    pad = max(1, round(img.width * 0.03))
    canvas = Image.new("RGBA", (img.width + pad * 2, img.height + pad * 2), (0, 0, 0, 0))
    canvas.paste(img, (pad, pad))

    scale = SIZE / canvas.width
    canvas = canvas.resize((SIZE, max(1, round(canvas.height * scale))), Image.LANCZOS)
    canvas.save(OUT)
    print("已生成 %s  %dx%d  颜色 #%s" % (OUT, canvas.width, canvas.height, HEX))


if __name__ == "__main__":
    main()
