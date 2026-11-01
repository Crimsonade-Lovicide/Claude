"""Thumbnails for Case 05 (1280x720 JPEG).

    python thumbs05.py <prod_dir> <case01_prod_dir>

A: the parked car at dusk under one sodium lamp (scenes.py lot, view=wide), pushed left, with
   A COUSIN'S DNA on the right. No photo of the perpetrator or of any victim, no real family
   tree, no company logos (research §F).
B: the Scale (Case 01's hero render), tipped, with YOUR FAMILY?
Writes thumb_a.jpg and thumb_b.jpg into <prod_dir>.
"""

import os
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gfx as G  # noqa: E402
import thumbs as T  # noqa: E402
import thumbs02 as T2  # noqa: E402


def thumb_a(prod):
    car = T.hero(prod, "thumb_lot", "lot", ["view=wide"])
    return T.thumb(T2.feathered(car, 80, 0.85, edge=320), [("A COUSIN'S", 128, G.INK), ("DNA", 200, G.BRASS)],
                   os.path.join(prod, "thumb_a.jpg"))


def thumb_b(prod, prod1):
    scale = Image.open(os.path.join(prod1, "renders", "thumb_scale.png")).convert("RGB")
    return T.thumb(T2.feathered(scale, 120, 0.7), [("YOUR", 170, G.INK), ("FAMILY?", 170, G.BRASS)],
                   os.path.join(prod, "thumb_b.jpg"))


def main(prod, prod1):
    G.FONT_DIR = os.environ.get("WOE_FONTS", os.path.join(prod, "fonts"))
    os.makedirs(os.path.join(prod, "renders"), exist_ok=True)
    print(thumb_a(prod))
    print(thumb_b(prod, prod1))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
