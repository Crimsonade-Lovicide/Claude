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

NAME = "Weight of Evidence"

# Banner crop zones (centred), from YouTube's banner guidelines.
ZONES = {"tv": (2048, 1152), "desktop": (2048, 423), "mobile": (1546, 423), "all devices": (1235, 338)}


def mark(size, bg=G.BG):
    """The show's mark: a brass balance, beam tipped by the heavier pan. Built at 4x, then reduced."""
    s = size * 4
    img = Image.new("RGBA", (s, s), bg + (255,) if bg else (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    P = lambda x, y: (int(x * s), int(y * s))
    brass = G.BRASS + (255,)
    # base and post
    d.polygon([P(0.42, 0.80), P(0.58, 0.80), P(0.64, 0.835), P(0.36, 0.835)], fill=brass)
    d.line([P(0.5, 0.24), P(0.5, 0.80)], fill=brass, width=int(s * 0.024))
    d.ellipse([*P(0.465, 0.18), *P(0.535, 0.25)], fill=brass)  # finial
    # beam: left end lower, the evidence outweighs
    left, right = (0.23, 0.325), (0.77, 0.265)
    d.line([P(*left), P(*right)], fill=brass, width=int(s * 0.02))
    for (x, y) in (left, right):
        d.ellipse([*P(x - 0.02, y - 0.02), *P(x + 0.02, y + 0.02)], fill=brass)
        rim = y + 0.25
        for dx in (-0.105, 0.105):  # strings
            d.line([P(x, y), P(x + dx, rim)], fill=brass, width=max(2, int(s * 0.008)))
        d.pieslice([*P(x - 0.115, rim - 0.055), *P(x + 0.115, rim + 0.055)], 0, 180, fill=brass)  # pan
    # the evidence: a stack of papers on the heavier pan
    rim = left[1] + 0.25
    paper = G.PAPER + (255,)
    d.polygon([P(0.16, rim - 0.004), P(0.30, rim - 0.004), P(0.285, rim - 0.034), P(0.175, rim - 0.034)], fill=paper)
    d.line([P(0.17, rim - 0.019), P(0.29, rim - 0.019)], fill=G.BG + (255,), width=max(2, int(s * 0.004)))
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
    size = 118
    while True:  # largest size that keeps the title inside the all-devices area
        t = G.text_layer(NAME.upper(), G.SANS(size, "SemiBold"), fill=G.INK, spacing=0.10)
        if t.width <= 1140:
            break
        size -= 2
    img.paste(t, ((W - t.width) // 2, cy - 30 - t.height // 2), t)
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
    G.FONT_DIR = os.environ.get("WOE_FONTS", os.path.join(prod, "fonts"))
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
