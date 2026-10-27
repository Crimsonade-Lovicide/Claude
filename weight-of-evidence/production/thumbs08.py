"""Thumbnails for Case 08 (1280x720 JPEG).

    python thumbs08.py <prod_dir> <case01_prod_dir>

A: the empty cell (scenes.py cell, push view, sun through the high window), pushed left, with
   1,110 DAYS / NO TRIAL on the right. No photograph of Kalief Browder, nothing from the 2015
   surveillance videos, no reference to his death (research §J).
B: the Scale (Case 01's hero render), tipped, with NEVER / TRIED.
Writes thumb_a.jpg and thumb_b.jpg into <prod_dir>.
"""

import os
import sys

from PIL import Image, ImageEnhance

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gfx as G  # noqa: E402
import thumbs as T  # noqa: E402
import thumbs02 as T2  # noqa: E402


def thumb_a(prod):
    cell = T.hero(prod, "thumb_cell", "cell", ["view=push"])
    cell = ImageEnhance.Contrast(ImageEnhance.Brightness(cell).enhance(1.9)).enhance(1.15)  # reads at 120 px
    return T.thumb(T2.feathered(cell, 80, 0.85, edge=320), [("1,110 DAYS", 140, G.INK), ("NO TRIAL", 150, G.BRASS)],
                   os.path.join(prod, "thumb_a.jpg"))


def thumb_b(prod, prod1):
    scale = Image.open(os.path.join(prod1, "renders", "thumb_scale.png")).convert("RGB")
    return T.thumb(T2.feathered(scale, 120, 0.7), [("NEVER", 150, G.INK), ("TRIED", 150, G.BRASS)],
                   os.path.join(prod, "thumb_b.jpg"))


def main(prod, prod1):
    G.FONT_DIR = os.environ.get("WOE_FONTS", os.path.join(prod, "fonts"))
    os.makedirs(os.path.join(prod, "renders"), exist_ok=True)
    print(thumb_a(prod))
    print(thumb_b(prod, prod1))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
