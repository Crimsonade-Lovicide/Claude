"""Weight of Evidence graphics kit: one look for every motion-graphics shot.

A shot is a function frame(t, dur) -> PIL.Image (1920x1080 RGB). These helpers keep
type, colour, motion and the evidence labels consistent across episodes.

Fonts (OFL, from google/fonts) live in $WOE_FONTS (default: ./fonts):
PlexSans.ttf (variable), PlexSerif*.ttf, PlexMono*.ttf, CourierPrime.ttf.
"""

import math
import os
import random

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1920, 1080
FPS = 24

# Palette: near-black ground, paper cream for documents, brass for evidence, cyan for
# medicine. RED is used only for the verdict line and warnings.
BG = (8, 9, 12)
INK = (234, 230, 220)
DIM = (128, 131, 140)
FAINT = (52, 55, 62)
PAPER = (231, 224, 208)
PAPER_INK = (34, 32, 30)
BRASS = (201, 162, 92)
CYAN = (96, 200, 214)
RED = (214, 84, 64)

LABEL_COLOURS = {"RECORD": BRASS, "INFERENCE": CYAN, "ARGUMENT": (176, 150, 214),
                 "RECONSTRUCTION": DIM}

FONT_DIR = os.environ.get("WOE_FONTS", "fonts")
_fonts = {}


def font(name, size, weight=None):
    key = (name, size, weight)
    if key not in _fonts:
        f = ImageFont.truetype(os.path.join(FONT_DIR, f"{name}.ttf"), size)
        if weight:
            try:
                f.set_variation_by_name(weight)
            except Exception:
                pass
        _fonts[key] = f
    return _fonts[key]


def SANS(size, weight="Regular"):
    return font("PlexSans", size, weight)


def SERIF(size):
    return font("PlexSerif", size)


def SERIF_I(size):
    return font("PlexSerifItalic", size)


def SERIF_B(size):
    return font("PlexSerifSemiBold", size)


def MONO(size, bold=False):
    return font("PlexMonoSemiBold" if bold else "PlexMono", size)


def TYPE(size):
    return font("CourierPrime", size)


# ---------------------------------------------------------------- timing helpers

def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def ease(x):
    """Smoothstep in/out."""
    x = clamp(x)
    return x * x * (3 - 2 * x)


def ease_out(x):
    x = clamp(x)
    return 1 - (1 - x) ** 3


def ramp(t, start, length):
    """0 before start, eased to 1 over length seconds."""
    return ease((t - start) / length) if length > 0 else float(t >= start)


def fade(t, dur, fin=0.4, fout=0.4):
    """Opacity for a whole shot: fade in at the head, out at the tail."""
    a = clamp(t / fin) if fin else 1.0
    b = clamp((dur - t) / fout) if fout else 1.0
    return min(a, b)


# ---------------------------------------------------------------- surfaces

_grain_cache = []


def _grain_frames(n=8, amount=7):
    if not _grain_cache:
        rng = np.random.default_rng(7)
        for _ in range(n):
            g = rng.normal(0, amount, (H // 2, W // 2)).astype(np.int16)
            _grain_cache.append(np.kron(g, np.ones((2, 2), dtype=np.int16)))
    return _grain_cache


def _vignette():
    y, x = np.ogrid[:H, :W]
    d = np.sqrt(((x - W / 2) / (W / 2)) ** 2 + ((y - H / 2) / (H / 2)) ** 2)
    return np.clip(1.0 - 0.38 * d ** 2.2, 0.45, 1.0)


_VIG = None


def finish(img, t=0.0, grain=True, vignette=True):
    """Last pass on every frame: vignette and a little moving film grain."""
    global _VIG
    a = np.asarray(img.convert("RGB")).astype(np.float32)
    if vignette:
        if _VIG is None:
            _VIG = _vignette()[..., None]
        a *= _VIG
    if grain:
        g = _grain_frames()[int(t * FPS) % 8]
        a += g[..., None]
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def canvas(colour=BG):
    return Image.new("RGB", (W, H), colour)


def paste_alpha(base, layer, xy, alpha=1.0):
    """Paste an RGBA layer at xy with an extra overall opacity."""
    if alpha <= 0:
        return base
    layer = layer.convert("RGBA")
    if alpha < 1:
        a = layer.getchannel("A").point(lambda v: int(v * alpha))
        layer.putalpha(a)
    base.paste(layer, (int(xy[0]), int(xy[1])), layer)
    return base


def text_layer(text, fnt, fill=INK, spacing=0.0, pad=4):
    """Text on a transparent layer, with optional letter-spacing (em fraction)."""
    if spacing:
        widths = [fnt.getlength(c) for c in text]
        extra = fnt.size * spacing
        w = int(sum(widths) + extra * max(0, len(text) - 1)) + pad * 2
    else:
        w = int(fnt.getlength(text)) + pad * 2
    asc, desc = fnt.getmetrics()
    layer = Image.new("RGBA", (max(1, w), asc + desc + pad * 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    if spacing:
        x = pad
        for c, cw in zip(text, widths):
            d.text((x, pad), c, font=fnt, fill=fill)
            x += cw + extra
    else:
        d.text((pad, pad), text, font=fnt, fill=fill)
    return layer


def wrap(text, fnt, width):
    """Greedy word wrap to a pixel width."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if fnt.getlength(trial) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def centered(base, layer, cy, alpha=1.0, dx=0):
    return paste_alpha(base, layer, ((W - layer.width) // 2 + dx, cy - layer.height // 2), alpha)


# ---------------------------------------------------------------- the evidence labels

def stamp(label, size=22):
    """The RECORD / INFERENCE / ARGUMENT / RECONSTRUCTION stamp."""
    col = LABEL_COLOURS.get(label, DIM)
    t = text_layer(label, MONO(size, bold=True), fill=col, spacing=0.18)
    pad_x, pad_y = 14, 6
    layer = Image.new("RGBA", (t.width + pad_x * 2, t.height + pad_y * 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.rectangle([1, 1, layer.width - 2, layer.height - 2], outline=col + (255,), width=2)
    layer.paste(t, (pad_x, pad_y), t)
    return layer


def recon_tag(base, alpha=1.0, text="RECONSTRUCTION"):
    """Small corner tag on any rebuilt image (3D scene, recreated page, illustrative scan)."""
    s = stamp(text, 18)
    return paste_alpha(base, s, (W - s.width - 56, 48), 0.85 * alpha)


def evidence_card(claim, label, source=None, width=1180):
    """A paper card: claim in serif, label stamp top-right, source in mono underneath."""
    body = SERIF(46)
    lines = wrap(claim, body, width - 140)
    lh = 62
    src_h = 60 if source else 0
    h = 120 + lh * len(lines) + src_h + 40
    card = Image.new("RGBA", (width, h), PAPER + (255,))
    d = ImageDraw.Draw(card)
    rng = random.Random(len(claim))
    for _ in range(1400):  # paper tooth
        x, y = rng.randrange(width), rng.randrange(h)
        v = rng.randrange(-10, 6)
        d.point((x, y), fill=tuple(clamp_c(c + v) for c in PAPER) + (255,))
    d.rectangle([0, 0, width - 1, h - 1], outline=(200, 190, 170, 255), width=2)
    s = stamp(label, 20)
    # stamp ink on paper: darken the label colour so it reads on cream
    card.paste(darken(s, 0.75), (width - s.width - 36, 32), s)
    y = 110
    for ln in lines:
        d.text((70, y), ln, font=body, fill=PAPER_INK)
        y += lh
    if source:
        d.line([70, y + 18, 70 + 120, y + 18], fill=(150, 140, 120, 255), width=2)
        d.text((70, y + 30), source, font=MONO(24), fill=(96, 90, 80, 255))
    return card


def clamp_c(v):
    return max(0, min(255, v))


def darken(layer, k):
    a = np.asarray(layer).astype(np.float32)
    a[..., :3] *= k
    return Image.fromarray(a.astype(np.uint8), "RGBA")


def drop_shadow(layer, blur=24, offset=(0, 18), opacity=150):
    sh = Image.new("RGBA", (layer.width + blur * 4, layer.height + blur * 4), (0, 0, 0, 0))
    mask = layer.getchannel("A").point(lambda v: opacity if v else 0)
    sh.paste((0, 0, 0, 255), (blur * 2 + offset[0], blur * 2 + offset[1]), mask)
    sh = sh.filter(ImageFilter.GaussianBlur(blur))
    sh.paste(layer, (blur * 2, blur * 2), layer)
    return sh, blur * 2


def card_shot(claim, label, source=None):
    """Evidence card slides up and settles; slight push-in through the shot."""
    card = evidence_card(claim, label, source)
    shadowed, off = drop_shadow(card)

    def frame(t, dur):
        img = canvas()
        k = ease_out(t / 0.7)
        z = 1.0 + 0.03 * (t / max(dur, 0.01))
        layer = shadowed.resize((int(shadowed.width * z), int(shadowed.height * z)), Image.LANCZOS)
        y = H // 2 - layer.height // 2 + int((1 - k) * 90)
        paste_alpha(img, layer, ((W - layer.width) // 2, y), k * fade(t, dur, 0.01, 0.35))
        return finish(img, t)
    return frame


# ---------------------------------------------------------------- documents

def document(lines, header=None, width=1400, typed=1.0, font_fn=TYPE, size=40,
             highlight=None, hi_amount=0.0, footer=None):
    """A recreated typed page. typed (0..1) reveals characters; highlight=(line, start, end)
    sweeps a marker over part of a line by hi_amount (0..1)."""
    fnt = font_fn(size)
    lh = int(size * 1.55)
    h = 160 + lh * len(lines) + (80 if footer else 40) + (70 if header else 0)
    page = Image.new("RGBA", (width, h), PAPER + (255,))
    d = ImageDraw.Draw(page)
    rng = random.Random(width + len(lines))
    for _ in range(2600):
        x, y = rng.randrange(width), rng.randrange(h)
        v = rng.randrange(-12, 5)
        d.point((x, y), fill=tuple(clamp_c(c + v) for c in PAPER) + (255,))
    y = 90
    if header:
        d.text((90, y), header, font=MONO(26, bold=True), fill=(90, 84, 74, 255))
        y += 70
    total = sum(len(ln) for ln in lines)
    budget = int(total * clamp(typed))
    for i, ln in enumerate(lines):
        shown = ln[:max(0, budget)]
        budget -= len(ln)
        if highlight and highlight[0] == i and hi_amount > 0:
            s, e = highlight[1], highlight[2]
            x0 = 90 + fnt.getlength(ln[:s])
            x1 = x0 + (fnt.getlength(ln[:e]) - fnt.getlength(ln[:s])) * clamp(hi_amount)
            d.rectangle([x0 - 4, y + 6, x1 + 4, y + lh - 8], fill=(232, 196, 110, 255))
        d.text((90, y), shown, font=fnt, fill=PAPER_INK)
        y += lh
    if footer:
        d.text((90, h - 70), footer, font=MONO(22), fill=(110, 104, 94, 255))
    return page


def document_shot(lines, header=None, footer=None, type_secs=None, highlight=None,
                  hi_at=None, size=40, width=1400, tag="RECONSTRUCTION", drift=0.05,
                  font_fn=TYPE):
    """Page on the desk with a slow push; optional typing and marker sweep."""
    def frame(t, dur):
        typed = 1.0 if not type_secs else clamp(t / type_secs)
        hi = 0.0 if hi_at is None else clamp((t - hi_at) / 0.8)
        page = document(lines, header, width, typed, font_fn=font_fn, size=size,
                        highlight=highlight, hi_amount=hi, footer=footer)
        page = page.rotate(-0.6, resample=Image.BICUBIC, expand=True)
        z = 0.92 + drift * ease(t / max(dur, 0.01))
        page = page.resize((int(page.width * z), int(page.height * z)), Image.LANCZOS)
        shadowed, _ = drop_shadow(page, blur=30, offset=(0, 24))
        img = canvas((14, 15, 18))
        y = (H - shadowed.height) // 2
        if shadowed.height > H:  # tall pages scroll slowly
            y = int(-(shadowed.height - H) * ease(t / max(dur, 0.01)) * 0.6)
        paste_alpha(img, shadowed, ((W - shadowed.width) // 2, y), fade(t, dur, 0.4, 0.4))
        if tag:
            recon_tag(img, fade(t, dur, 0.6, 0.4))
        return finish(img, t)
    return frame


# ---------------------------------------------------------------- titles and type

def title_shot(main, sub=None, kicker=None):
    """Episode or act title: letter-spaced sans, thin rule, optional kicker and subtitle."""
    def frame(t, dur):
        img = canvas()
        a = fade(t, dur, 0.8, 0.6)
        if kicker:
            k = text_layer(kicker, MONO(26), fill=DIM, spacing=0.3)
            centered(img, k, H // 2 - 120, a * ramp(t, 0.1, 0.6))
        m = text_layer(main, SANS(92, "SemiBold"), fill=INK, spacing=0.12)
        centered(img, m, H // 2 - 10, a * ramp(t, 0.3, 0.9))
        d = ImageDraw.Draw(img)
        rw = int(520 * ramp(t, 0.6, 1.0))
        if rw > 0:
            d.line([W // 2 - rw // 2, H // 2 + 62, W // 2 + rw // 2, H // 2 + 62],
                   fill=tuple(int(c * a) for c in BRASS), width=2)
        if sub:
            s = text_layer(sub, SERIF_I(44), fill=INK)
            centered(img, s, H // 2 + 130, a * ramp(t, 0.9, 0.8))
        return finish(img, t)
    return frame


def words_shot(text, size=74, fnt=None, colour=INK, emphasis=None, per_word=0.18,
               width=1500, start=0.2):
    """Big centred statement, revealed word by word. emphasis: set of words in brass."""
    fnt = fnt or SERIF(size)
    lines = wrap(text, fnt, width)
    lh = int(size * 1.35)

    def frame(t, dur):
        img = canvas()
        a = fade(t, dur, 0.3, 0.5)
        y0 = H // 2 - lh * len(lines) // 2
        n = 0
        d = ImageDraw.Draw(img)
        for i, ln in enumerate(lines):
            x = (W - fnt.getlength(ln)) // 2
            for word in ln.split(" "):
                k = clamp((t - start - n * per_word) / 0.35) * a
                bare = word.strip(".,;:!?“”\"'").lower()
                c = BRASS if emphasis and bare in emphasis else colour
                c = tuple(int(BG[j] + (c[j] - BG[j]) * k) for j in range(3))
                d.text((x, y0 + i * lh + int((1 - k) * 10)), word, font=fnt, fill=c)
                x += fnt.getlength(word + " ")
                n += 1
        return finish(img, t)
    return frame


def lower_third(img, line1, line2=None, alpha=1.0):
    d = ImageDraw.Draw(img)
    x, y = 120, H - 210
    a = clamp(alpha)
    d.line([x, y, x, y + (96 if line2 else 52)], fill=tuple(int(c * a) for c in BRASS), width=4)
    l1 = text_layer(line1, SANS(40, "SemiBold"), fill=INK)
    paste_alpha(img, l1, (x + 24, y - 6), a)
    if line2:
        l2 = text_layer(line2, MONO(26), fill=DIM)
        paste_alpha(img, l2, (x + 26, y + 50), a)
    return img


# ---------------------------------------------------------------- the verdict

def verdict_meter(img, pct, fill=1.0, y=760, alpha=1.0, label="CONFIDENCE"):
    """0-100% bar that fills to pct; the number counts up with it."""
    d = ImageDraw.Draw(img)
    x0, x1 = 360, W - 360
    a = clamp(alpha)
    col = lambda c: tuple(int(BG[i] + (c[i] - BG[i]) * a) for i in range(3))
    d.rectangle([x0, y, x1, y + 18], outline=col(FAINT), width=2)
    for k in range(11):
        xx = x0 + (x1 - x0) * k / 10
        d.line([xx, y + 24, xx, y + 32], fill=col(FAINT), width=2)
    cur = pct * ease(fill)
    xf = x0 + (x1 - x0) * cur / 100
    if xf - 3 > x0 + 3:
        d.rectangle([x0 + 3, y + 3, xf - 3, y + 15], fill=col(BRASS))
    lab = text_layer(label, MONO(24), fill=col(DIM), spacing=0.3)
    img.paste(lab, (x0, y - 52), lab)
    num = text_layer(f"{round(cur)}%", SANS(64, "SemiBold"), fill=col(INK))
    img.paste(num, (int(x1 - num.width + 4), y - 86), num)
    return img


def verdict_shot(verdict, pct, change=None, meter_at=1.6, change_at=None, offset=0.0,
                 kicker="VERDICT"):
    """VERDICT (one sentence) / CONFIDENCE meter / WHAT WOULD CHANGE OUR MIND."""
    vf = SERIF(58)
    vl = wrap(verdict, vf, 1300)

    def frame(t, dur):
        img = canvas()
        a = fade(t, dur, 0.5 if not offset else 0.01, 0.6)
        t = t + offset
        k = text_layer(kicker, MONO(28, bold=True), fill=RED, spacing=0.35)
        paste_alpha(img, k, ((W - k.width) // 2, 170), a * ramp(t, 0.0, 0.5))
        for i, ln in enumerate(vl):
            layer = text_layer(ln, vf, fill=INK)
            paste_alpha(img, layer, ((W - layer.width) // 2, 250 + i * 78), a * ramp(t, 0.3 + 0.2 * i, 0.6))
        verdict_meter(img, pct, fill=clamp((t - meter_at) / 1.6), y=640, alpha=a * ramp(t, meter_at - 0.3, 0.4))
        if change:
            ca = a * ramp(t, change_at if change_at is not None else meter_at + 2.2, 0.6)
            h = text_layer("WHAT WOULD CHANGE OUR MIND", MONO(24), fill=DIM, spacing=0.3)
            paste_alpha(img, h, ((W - h.width) // 2, 780), ca)
            for i, ln in enumerate(wrap(change, SERIF_I(38), 1300)):
                layer = text_layer(ln, SERIF_I(38), fill=INK)
                paste_alpha(img, layer, ((W - layer.width) // 2, 830 + i * 52), ca)
        return finish(img, t)
    return frame


# ---------------------------------------------------------------- stills and clips

def still_shot(path, zoom=(1.0, 1.08), pan=(0.0, 0.0), tag=None, darken_to=1.0, overlay=None):
    """Ken Burns on a rendered still. pan is the drift in fractions of the frame."""
    cache = {}

    def load():
        if "img" not in cache:
            if os.path.exists(path):
                im = Image.open(path).convert("RGB")
                cache["img"] = im if im.size == (W, H) else im.resize((W, H), Image.LANCZOS)
            else:  # placeholder so the edit always renders
                im = canvas((20, 22, 26))
                centered(im, text_layer(f"[{os.path.basename(path)}]", MONO(30), fill=DIM), H // 2)
                cache["img"] = im
        return cache["img"]

    def frame(t, dur):
        src = load()
        u = ease(t / max(dur, 0.01))
        z = zoom[0] + (zoom[1] - zoom[0]) * u
        cw, ch = W / z, H / z
        cx = W / 2 + pan[0] * W * (u - 0.5)
        cy = H / 2 + pan[1] * H * (u - 0.5)
        box = (cx - cw / 2, cy - ch / 2, cx + cw / 2, cy + ch / 2)
        img = src.resize((W, H), Image.BICUBIC, box=box)
        a = fade(t, dur, 0.4, 0.4) * darken_to
        if a < 1:
            img = Image.blend(canvas(), img, a)
        if overlay:
            overlay(img, t, dur)
        if tag:
            recon_tag(img, fade(t, dur, 0.6, 0.4), tag)
        return finish(img, t)
    return frame


def seq(*parts):
    """Chain shots: parts are (frame_fn, seconds); the last one takes the remainder."""
    def frame(t, dur):
        acc = 0.0
        for i, (fn, secs) in enumerate(parts):
            last = i == len(parts) - 1
            length = (dur - acc) if last else secs
            if t < acc + length or last:
                return fn(t - acc, max(length, 0.01))
            acc += length
    return frame


# ---------------------------------------------------------------- rendering

def render(frame_fn, dur, out_path, fps=FPS, audio=None):
    """Pipe frames into ffmpeg (H.264, yuv420p). Optional audio file muxed in."""
    import subprocess
    w, h = frame_fn(0.0, dur).size  # 16:9 by default; the vertical cut renders 9:16
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
           "-s", f"{w}x{h}", "-r", str(fps), "-i", "-"]
    if audio:
        cmd += ["-i", audio, "-c:a", "aac", "-b:a", "192k", "-shortest"]
    cmd += ["-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", out_path]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    n = int(round(dur * fps))
    for i in range(n):
        p.stdin.write(frame_fn(i / fps, dur).tobytes())
    p.stdin.close()
    p.wait()
    if p.returncode:
        raise RuntimeError(f"ffmpeg failed for {out_path}")
    return out_path
