"""Channel art: profile picture, banner and video watermark.

    python channel_art.py <prod_dir> <out_dir>

Uses the Scale hero render from thumbs.py (<prod_dir>/renders/thumb_scale.png).
Writes:
  avatar_800.png     profile picture, 800x800 (YouTube shows it as a 98 px circle)
  banner_2048.jpg    2048x1152; everything that matters sits in the 1235x338 centre
                     area that every device shows
  banner_check.png   the banner with the TV / desktop / mobile / all-devices crops drawn on
  watermark_150.png  150x150 transparent, for Studio > Customization > Video watermark
"""

import os
import sys

from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gfx as G  # noqa: E402

# Banner crop zones (centred), from YouTube's banner guidelines.
ZONES = {"tv": (2048, 1152), "desktop": (2048, 423), "mobile": (1546, 423), "all devices": (1235, 338)}


def mark(size, bg=G.BG, pct=70):
    """The show's mark: 'OV' over a verdict meter filled to pct. Built at 4x, then reduced."""
    s = size * 4
    img = Image.new("RGBA", (s, s), bg + (255,) if bg else (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    f = G.SANS(int(s * 0.36), "SemiBold")
    lay = G.text_layer("OV", f, fill=G.INK, spacing=0.06)
    img.alpha_composite(lay, ((s - lay.width) // 2, int(s * 0.215)))
    # meter: outline, brass fill, ticks
    x0, x1 = int(s * 0.22), int(s * 0.78)
    y0 = int(s * 0.605)
    h = int(s * 0.075)
    lw = max(2, s // 110)
    d.rectangle([x0, y0, x1, y0 + h], outline=G.DIM + (255,), width=lw)
    xf = x0 + (x1 - x0) * pct / 100
    d.rectangle([x0 + 2 * lw, y0 + 2 * lw, int(xf), y0 + h - 2 * lw], fill=G.BRASS + (255,))
    return img.resize((size, size), Image.LANCZOS)


def avatar(out):
    img = mark(800).convert("RGB")
    img.save(os.path.join(out, "avatar_800.png"))
    return img


def watermark(out):
    img = mark(150, bg=None)
    img.save(os.path.join(out, "watermark_150.png"))
    return img


def banner(prod, out):
    W, H = 2048, 1152
    scale = Image.open(os.path.join(prod, "renders", "thumb_scale.png")).convert("RGB")
    scale = scale.resize((W, int(scale.height * W / scale.width)), Image.LANCZOS)
    img = Image.new("RGB", (W, H), scale.getpixel((4, 4)))
    img.paste(scale, (0, 260))  # drop the beam into the centre strip
    # darken behind the type so the beam reads as texture, not subject
    shade = Image.new("L", (W, H), 0)
    sd = ImageDraw.Draw(shade)
    sd.ellipse([W // 2 - 760, H // 2 - 260, W // 2 + 760, H // 2 + 260], fill=238)
    shade = shade.filter(ImageFilter.GaussianBlur(120))
    img = Image.composite(Image.new("RGB", (W, H), G.BG), img, shade)

    d = ImageDraw.Draw(img)
    cy = H // 2
    k = G.text_layer("ONE QUESTION  ·  THE EVIDENCE  ·  A VERDICT", G.MONO(26), fill=G.DIM, spacing=0.3)
    img.paste(k, ((W - k.width) // 2, cy - 132), k)
    t = G.text_layer("OPEN VERDICT", G.SANS(118, "SemiBold"), fill=G.INK, spacing=0.12)
    img.paste(t, ((W - t.width) // 2, cy - 92), t)
    d.line([W // 2 - 300, cy + 66, W // 2 + 300, cy + 66], fill=G.BRASS, width=3)
    s = G.text_layer("Hard questions, argued from the record.", G.SERIF_I(44), fill=G.INK)
    img.paste(s, ((W - s.width) // 2, cy + 92), s)
    img.save(os.path.join(out, "banner_2048.jpg"), quality=92)

    chk = img.copy()
    cd = ImageDraw.Draw(chk)
    for name, (zw, zh) in ZONES.items():
        box = [(W - zw) // 2, (H - zh) // 2, (W + zw) // 2 - 1, (H + zh) // 2 - 1]
        cd.rectangle(box, outline=(80, 200, 120), width=3)
        cd.text((box[0] + 10, box[1] + 8), name, font=G.MONO(26), fill=(80, 200, 120))
    chk.save(os.path.join(out, "banner_check.png"))
    return img


def main(prod, out):
    G.FONT_DIR = os.environ.get("OV_FONTS", os.path.join(prod, "fonts"))
    os.makedirs(out, exist_ok=True)
    avatar(out)
    watermark(out)
    banner(prod, out)
    # what the avatar looks like where people actually see it
    a = Image.open(os.path.join(out, "avatar_800.png"))
    m = Image.new("L", (800, 800), 0)
    ImageDraw.Draw(m).ellipse([0, 0, 799, 799], fill=255)
    prev = Image.new("RGB", (800, 800), (255, 255, 255))
    prev.paste(a, (0, 0), m)
    prev.resize((98, 98), Image.LANCZOS).save(os.path.join(out, "avatar_check_98.png"))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
