"""Thumbnails for Case 09 (1280x720 JPEG).

    python thumbs09.py <prod_dir> <case01_prod_dir>

A: the fax machine on the night desk (scenes.py fax, push view), pushed left, with 4 DAYS / BEFORE on the
   right. No photograph of anyone involved; no image of the house, the fire or an execution chamber
   (research §K).
B: the Scale (Case 01's hero render), tipped, with NO PROOF / OF ARSON (Beyler's finding, not a claim
   about his guilt).
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
    fax = T.hero(prod, "thumb_fax", "fax", ["view=push", "page_out=0.7"])
    fax = ImageEnhance.Brightness(fax).enhance(1.35)  # reads at 120 px
    return T.thumb(T2.feathered(fax, 80, 0.85, edge=320), [("4 DAYS", 150, G.INK), ("BEFORE", 150, G.BRASS)],
                   os.path.join(prod, "thumb_a.jpg"))


def thumb_b(prod, prod1):
    scale = Image.open(os.path.join(prod1, "renders", "thumb_scale.png")).convert("RGB")
    return T.thumb(T2.feathered(scale, 120, 0.7), [("NO PROOF", 140, G.INK), ("OF ARSON", 140, G.BRASS)],
                   os.path.join(prod, "thumb_b.jpg"))


def main(prod, prod1):
    G.FONT_DIR = os.environ.get("WOE_FONTS", os.path.join(prod, "fonts"))
    os.makedirs(os.path.join(prod, "renders"), exist_ok=True)
    print(thumb_a(prod))
    print(thumb_b(prod, prod1))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
