"""Thumbnails for Case 06 (1280x720 JPEG).

    python thumbs06.py <prod_dir> <case01_prod_dir>

A: over the shoulder of the 1980s camera (scenes.py room, view=camera), red light on, at the empty chair,
   pushed left, with THE LIE / IS LEGAL on the right. No photos of the five men at any age, nothing
   from the videotapes, no photo of Trisha Meili (research §K).
B: the Scale (Case 01's hero render), tipped, with WOULD YOU CONFESS?
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
    room = T.hero(prod, "thumb_room_cam", "room", ["view=camera", "tally=1"])
    return T.thumb(T2.feathered(room, 80, 0.85, edge=320), [("THE LIE", 150, G.INK), ("IS LEGAL", 150, G.BRASS)],
                   os.path.join(prod, "thumb_a.jpg"))


def thumb_b(prod, prod1):
    scale = Image.open(os.path.join(prod1, "renders", "thumb_scale.png")).convert("RGB")
    return T.thumb(T2.feathered(scale, 120, 0.7), [("WOULD YOU", 140, G.INK), ("CONFESS?", 150, G.BRASS)],
                   os.path.join(prod, "thumb_b.jpg"))


def main(prod, prod1):
    G.FONT_DIR = os.environ.get("WOE_FONTS", os.path.join(prod, "fonts"))
    os.makedirs(os.path.join(prod, "renders"), exist_ok=True)
    print(thumb_a(prod))
    print(thumb_b(prod, prod1))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
