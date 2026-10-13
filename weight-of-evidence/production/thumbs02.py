"""Thumbnails for Case 02 (1280x720 JPEG).

    python thumbs02.py <prod_dir> <case01_prod_dir>

A: the night road from the driver's seat (scenes.py road, view=push) with a detection box in
   the lane, its label flickering VEHICLE? OTHER? BICYCLE?, and IT SAW HER. on the right.
B: the Scale (Case 01's hero render), tipped, with WHO'S GUILTY?
Writes thumb_a.jpg and thumb_b.jpg into <prod_dir>.
"""

import os
import sys

from PIL import Image, ImageDraw, ImageEnhance

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gfx as G  # noqa: E402
import thumbs as T  # noqa: E402


def road(prod):
    out = os.path.join(prod, "renders", "thumb_road.png")
    if not os.path.exists(out):
        T.hero(prod, "thumb_road", "road", ["view=push", "dist=60"])
    return Image.open(out).convert("RGB")


def thumb_a(prod):
    img = ImageEnhance.Brightness(road(prod)).enhance(1.25)
    d = ImageDraw.Draw(img, "RGBA")
    # detection box in the lane ahead, slightly left of centre (where she was crossing)
    cx, cy, s = 700, 690, 86
    d.rectangle([cx + s + 14, cy - s - 30, cx + s + 400, cy - s + 172], fill=(6, 7, 10, 215))
    for k, (txt, col, a) in enumerate((("VEHICLE?", G.CYAN, 120), ("OTHER?", G.DIM, 160), ("BICYCLE?", G.BRASS, 255))):
        off = (2 - k) * 10
        d.rectangle([cx - s - off, cy - s - off, cx + s + off, cy + s + off], outline=col + (a,), width=5 if k == 2 else 3)
        lay = G.text_layer(txt, G.MONO(50, True), fill=col if k == 2 else tuple(min(255, int(v * 1.35)) for v in col), spacing=0.08)
        G.paste_alpha(img, lay, (cx + s + 34, cy - s - 18 + k * 62), 1.0 if k == 2 else 0.8)
    for x in range(1180, 1920):  # darken the type area
        a = int(200 * min(1, (x - 1180) / 260))
        d.line([x, 0, x, 1080], fill=(8, 9, 12, a))
    y = 360
    for text, size, col in (("IT SAW", 170, G.INK), ("HER.", 170, G.BRASS)):
        f = G.SANS(size, "Bold")
        d.text((1840 - f.getlength(text), y), text, font=f, fill=col)
        y += int(size * 1.08)
    d.rectangle([1840 - 420, y + 40, 1840, y + 52], fill=G.BRASS)
    out = os.path.join(prod, "thumb_a.jpg")
    img.resize((1280, 720), Image.LANCZOS).save(out, quality=90)
    return out


def thumb_b(prod, prod1):
    scale = Image.open(os.path.join(prod1, "renders", "thumb_scale.png")).convert("RGB")
    out = os.path.join(prod, "thumb_b.jpg")
    return T.thumb(feathered(scale, 330, 0.82), [("WHO'S", 170, G.INK), ("GUILTY?", 170, G.BRASS)], out)


def feathered(img, shift, zoom, edge=160):
    """Like thumbs.setup, but the shrunken render fades into the canvas instead of ending in a seam."""
    canvas = Image.new("RGB", img.size, img.getpixel((4, 4)))
    small = img.resize((int(img.width * zoom), int(img.height * zoom)), Image.LANCZOS)
    w, h = small.size
    mask = Image.new("L", (w, h), 255)
    md = ImageDraw.Draw(mask)
    for i in range(edge):
        v = int(255 * i / edge)
        md.line([w - 1 - i, 0, w - 1 - i, h], fill=v)       # right edge
        md.line([0, h - 1 - i, w, h - 1 - i], fill=v)       # bottom edge
        md.line([0, i, w, i], fill=v)                        # top edge
    canvas.paste(small, (-shift, (canvas.height - h) // 2), mask)
    return canvas


def main(prod, prod1):
    G.FONT_DIR = os.environ.get("WOE_FONTS", os.path.join(prod, "fonts"))
    print(thumb_a(prod))
    print(thumb_b(prod, prod1))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
