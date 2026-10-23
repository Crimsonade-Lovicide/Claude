"""Thumbnails for Case 03 (1280x720 JPEG).

    python thumbs03.py <prod_dir> <case01_prod_dir>

A: the empty dinghy from high above on dark water (scenes.py sea, view=above), small in the
   left third, with 20 DAYS. 4 MEN. on the right. Twenty days, as in the special verdict and
   the narration.
B: the Scale (Case 01's hero render), tipped, with MURDER?
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
    boat = T.hero(prod, "thumb_boat", "sea", ["view=above", "mood=day", "sun_az=150", "exposure=-0.5", "tiles=5"])
    boat = boat.point(lambda v: int(255 * (v / 255) ** 0.8))  # lift the water just enough to read as water
    return T.thumb(boat, [("20 DAYS.", 170, G.INK), ("4 MEN.", 170, G.BRASS)], os.path.join(prod, "thumb_a.jpg"))


def thumb_b(prod, prod1):
    scale = Image.open(os.path.join(prod1, "renders", "thumb_scale.png")).convert("RGB")
    return T.thumb(T2.feathered(scale, 120, 0.7), [("MURDER?", 150, G.BRASS)], os.path.join(prod, "thumb_b.jpg"))


def main(prod, prod1):
    G.FONT_DIR = os.environ.get("WOE_FONTS", os.path.join(prod, "fonts"))
    os.makedirs(os.path.join(prod, "renders"), exist_ok=True)
    print(thumb_a(prod))
    print(thumb_b(prod, prod1))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
