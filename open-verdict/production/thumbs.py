"""Thumbnails for Case 01 (1280x720 JPEG, under 2 MB).

    python thumbs.py <prod_dir>

Renders a clean 1080p hero still of the glass brain (scenes.py) if it isn't there yet,
then sets the type with Pillow. Writes thumb_a.jpg (brain) and thumb_b.jpg (scale).
"""

import os
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gfx as G  # noqa: E402


def hero(prod, name, scene, args):
    out = os.path.join(prod, "renders", f"{name}.png")
    if not os.path.exists(out):
        tmp = os.path.join(prod, "renders", "tmp")
        py = os.environ.get("OV_PY", sys.executable)
        subprocess.run([py, os.path.join(HERE, "scenes.py"), scene, tmp, "--res", "1920x1080",
                        "--samples", "32", f"name={name}", *args], check=True, stdout=subprocess.DEVNULL)
        os.replace(os.path.join(tmp, f"{name}_0000.png"), out)
    return Image.open(out).convert("RGB")


def setup(img, shift):
    """Push the subject left to leave the right third for type."""
    canvas = Image.new("RGB", img.size, G.BG)
    canvas.paste(img, (-shift, 0))
    return canvas


def thumb(base, lines, out):
    img = base.copy()
    d = ImageDraw.Draw(img, "RGBA")
    for x in range(1100, 1920):  # darken the type area
        a = int(210 * min(1, (x - 1100) / 300))
        d.line([x, 0, x, 1080], fill=(8, 9, 12, a))
    y = 300
    for text, size, col in lines:
        f = G.SANS(size, "Bold")
        w = f.getlength(text)
        d.text((1840 - w, y), text, font=f, fill=col)
        y += int(size * 1.08)
    d.rectangle([1840 - 520, y + 50, 1840, y + 62], fill=G.BRASS)
    img = img.resize((1280, 720), Image.LANCZOS).filter(ImageFilter.UnsharpMask(1.2, 60, 2))
    img.save(out, quality=90)
    return out


def main(prod):
    G.FONT_DIR = os.environ.get("OV_FONTS", os.path.join(prod, "fonts"))
    brain = hero(prod, "thumb_brain", "brain", ["tumor=1.2", "glow=1.4", "view=three_q", "orbit=0"])
    scale = hero(prod, "thumb_scale", "scale", ["tilt=-12", "left=1", "right=0"])
    print(thumb(setup(brain, 260), [("IS HE", 190, G.INK), ("GUILTY?", 190, G.BRASS)],
                os.path.join(prod, "thumb_a.jpg")))
    print(thumb(setup(scale, 300), [("A TUMOR", 150, G.INK), ("MADE HIM", 150, G.INK), ("DO IT.", 150, G.BRASS)],
                os.path.join(prod, "thumb_b.jpg")))


if __name__ == "__main__":
    main(sys.argv[1])
