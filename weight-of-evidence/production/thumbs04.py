"""Thumbnails for Case 04 (1280x720 JPEG).

    python thumbs04.py <prod_dir> <case01_prod_dir>

A: the closed, untitled book (scenes.py book, mood=night) under one lamp, pushed left and
   shrunk, with STILL IN USE on the right. No plate, no signature, no photograph of Pernkopf,
   and no number that implies the atlas was "made from" the 1,377 (research §F).
B: the Scale (Case 01's hero render), tipped, with SHOULD THEY?
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
    book = T.hero(prod, "thumb_book", "book", ["mood=night", "push=0"])
    return T.thumb(T2.feathered(book, 60, 0.78, edge=360), [("STILL", 190, G.INK), ("IN USE", 190, G.BRASS)],
                   os.path.join(prod, "thumb_a.jpg"))


def thumb_b(prod, prod1):
    scale = Image.open(os.path.join(prod1, "renders", "thumb_scale.png")).convert("RGB")
    return T.thumb(T2.feathered(scale, 120, 0.7), [("SHOULD", 160, G.INK), ("THEY?", 160, G.BRASS)],
                   os.path.join(prod, "thumb_b.jpg"))


def main(prod, prod1):
    G.FONT_DIR = os.environ.get("WOE_FONTS", os.path.join(prod, "fonts"))
    os.makedirs(os.path.join(prod, "renders"), exist_ok=True)
    print(thumb_a(prod))
    print(thumb_b(prod, prod1))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
