"""Thumbnails for Case 07 (1280x720 JPEG).

    python thumbs07.py <prod_dir> <case01_prod_dir>

A: the empty courtroom (scenes.py courtroom, view=bench), pushed left, with WHO DECIDES? on the right.
   No photograph of Terri Schiavo, nothing from the 2002 videotapes, no bedside, hospice or medical
   imagery (research §K).
B: the Scale (Case 01's hero render), tipped, with NOTHING IN / WRITING.
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
    court = T.hero(prod, "thumb_courtroom", "courtroom", ["view=bench"])
    return T.thumb(T2.feathered(court, 80, 0.85, edge=320), [("WHO", 150, G.INK), ("DECIDES?", 150, G.BRASS)],
                   os.path.join(prod, "thumb_a.jpg"))


def thumb_b(prod, prod1):
    scale = Image.open(os.path.join(prod1, "renders", "thumb_scale.png")).convert("RGB")
    return T.thumb(T2.feathered(scale, 120, 0.7), [("NOTHING IN", 130, G.INK), ("WRITING", 150, G.BRASS)],
                   os.path.join(prod, "thumb_b.jpg"))


def main(prod, prod1):
    G.FONT_DIR = os.environ.get("WOE_FONTS", os.path.join(prod, "fonts"))
    os.makedirs(os.path.join(prod, "renders"), exist_ok=True)
    print(thumb_a(prod))
    print(thumb_b(prod, prod1))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
