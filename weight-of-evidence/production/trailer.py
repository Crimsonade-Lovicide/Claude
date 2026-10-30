"""Weight of Evidence channel trailer (T shots, 16:9) and its 30-second vertical cut (V shots, 9:16).

    python trailer.py <prod_dir> --final            16:9 trailer
    python trailer.py <prod_dir> --final --vertical  9:16 cut with word-by-word captions
<prod_dir> holds the trailer's narration.json / timing.json / words.json / vo/ (align.py)
and links anim/ to Case 01's rendered clips (the trailer needs nothing new).
"""

import math
import os
import sys

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import edit as E  # noqa: E402
import gfx as G  # noqa: E402
import score as S  # noqa: E402

VERTICAL = "--vertical" in sys.argv
SHOT_PREFIX = "V" if VERTICAL else "T"
OUT_NAME = "weight_of_evidence_trailer_vertical.mp4" if VERTICAL else "weight_of_evidence_trailer.mp4"
TITLE = "Weight of Evidence: trailer"
SILENT = {}
LEAD = {"T01": 1.2, "V01": 0.3}
PAD = {"T05": 0.8, "T07": 0.8, "T08": 0.8, "T09": 3.5, "V04": 2.0}
FADE_IN = {"T01": 1.0}
FADE_OUT = {"T09": 1.2, "V04": 0.8}


def road_words(text, at):
    """Typed place/date over a road centre line rushing toward the camera (case 02 tease)."""
    def frame(t, dur):
        img = G.canvas()
        d = ImageDraw.Draw(img)
        a = G.fade(t, dur, 0.3, 0.4)
        vx, vy = G.W / 2, G.H * 0.42
        for k in range(14):  # dashes in perspective
            z = ((k / 14) + t * 0.35) % 1.0
            y0 = vy + (G.H - vy) * z ** 2
            y1 = vy + (G.H - vy) * min(1, (z + 0.03)) ** 2
            w0, w1 = 2 + 26 * z ** 2, 2 + 26 * min(1, z + 0.03) ** 2
            c = tuple(int(v * a * (0.25 + 0.75 * z)) for v in (200, 170, 90))
            d.polygon([(vx - w0, y0), (vx + w0, y0), (vx + w1, y1), (vx - w1, y1)], fill=c)
        n = int(len(text) * G.clamp((t - at) / 1.2))
        lay = G.text_layer(text[:n] or " ", G.MONO(54, True), fill=G.INK, spacing=0.1)
        G.paste_alpha(img, lay, ((G.W - G.text_layer(text, G.MONO(54, True), spacing=0.1).width) // 2, 220), a)
        G.recon_tag(img, a, "CASE 02 · COMING")
        return G.finish(img, t)
    return frame


def sea_words(text, at):
    def frame(t, dur):
        img = G.canvas()
        d = ImageDraw.Draw(img)
        a = G.fade(t, dur, 0.3, 0.4)
        for k in range(26):  # slow swell lines
            y = G.H * 0.5 + k * 22
            pts = [(x, y + 10 * math.sin(x / 140 + t * 0.8 + k * 0.7) * (1 + k / 12)) for x in range(0, G.W + 40, 40)]
            c = tuple(int(v * a * (0.25 + k / 40)) for v in (60, 90, 110))
            d.line(pts, fill=c, width=2)
        lay = G.text_layer(text, G.SERIF(70), fill=G.INK)
        G.centered(img, lay, 300, a * G.ease((t - at) / 0.8))
        G.recon_tag(img, a, "CASE 03 · COMING")
        return G.finish(img, t)
    return frame


def book_words(text, at):
    def frame(t, dur):
        img = G.canvas()
        d = ImageDraw.Draw(img)
        a = G.fade(t, dur, 0.3, 0.4)
        bw, bh = 520, 700
        x0, y0 = (G.W - bw) // 2, (G.H - bh) // 2 + 20
        d.rectangle([x0, y0, x0 + bw, y0 + bh], fill=tuple(int(v * a) for v in (38, 30, 26)))
        d.rectangle([x0 + 24, y0 + 24, x0 + bw - 24, y0 + bh - 24], outline=tuple(int(v * a) for v in (90, 74, 52)), width=2)
        lay = G.text_layer(text, G.SERIF_B(44), fill=G.PAPER)
        G.centered(img, lay, y0 + 180, a * G.ease((t - at) / 0.8))
        G.recon_tag(img, a, "CASE 04 · COMING")
        return G.finish(img, t)
    return frame


def stamps_then(clip_fn, at, swap_at):
    labels = ["RECORD", "INFERENCE", "ARGUMENT"]

    def frame(t, dur):
        if t >= swap_at:
            return clip_fn(t - swap_at, dur - swap_at)
        img = G.canvas()
        a = G.fade(t, dur, 0.3, 0.01)
        for i, lab in enumerate(labels):
            k = G.ease((t - at - i * 0.9) / 0.4) * a
            st = G.stamp(lab, 44)
            G.paste_alpha(img, st, ((G.W - st.width) // 2, 330 + i * 150), k)
        return G.finish(img, t)
    return frame


def meter_shot(at):
    def frame(t, dur):
        img = G.canvas()
        a = G.fade(t, dur, 0.4, 0.4)
        k = G.text_layer("VERDICT", G.MONO(30, True), fill=G.RED, spacing=0.35)
        G.paste_alpha(img, k, ((G.W - k.width) // 2, 300), a)
        G.verdict_meter(img, 70, fill=G.clamp((t - at) / 1.8), y=560, alpha=a)
        h = G.text_layer("WHAT WOULD CHANGE OUR MIND", G.MONO(26), fill=G.DIM, spacing=0.3)
        G.paste_alpha(img, h, ((G.W - h.width) // 2, 720), a * G.ease((t - at - 2.0) / 0.6))
        return G.finish(img, t)
    return frame


def build(ctx):
    P = ctx.prod
    C = lambda name, **kw: E.Clip(P, name, **kw)
    at = ctx.at
    cap = lambda text: (lambda img, t, d: G.lower_third(img, text, None, G.ramp(t, 0.4, 0.5) * G.fade(t, d, 0.01, 0.4)))
    s = {
        "T01": E.clip_shot(C("scale_empty"), tag=None, fin=1.0),
        "T02": E.xfade_shot(C("brain_tumor", start=3), C("brain_clean", start=3), 999, glow="a", overlay=cap("CASE 01 · VIRGINIA, 2000")),
        "T03": road_words("TEMPE, ARIZONA · MARCH 18, 2018", 0.2),
        "T04": sea_words("The Mignonette · 1884", 0.3),
        "T05": book_words("THE PERNKOPF ATLAS", 0.3),
        "T06": stamps_then(E.clip_shot(C("scale_tip_right"), tag=None), at("T06", "what's on the record"),
                           at("T06", "only an argument", end=True) + 0.2),
        "T07": meter_shot(at("T07", "We tell you how sure")),
        "T08": E.clip_shot(C("scale_swing"), tag=None),
        "T09": G.title_shot("WEIGHT OF EVIDENCE", "One question. The evidence. A verdict.", "CASE 01 · THE TUMOR DEFENSE · OUT NOW"),
        "V01": E.xfade_shot(C("brain_tumor", start=3), C("brain_clean", start=3), 999, glow="a", tag=None),
        "V02": E.clip_shot(C("scale_tip_right"), tag=None),
        "V03": meter_shot(at("V03", "We gave a verdict")),
        "V04": G.title_shot("WEIGHT OF EVIDENCE", "Case 01 · full episode on the channel"),
    }
    if VERTICAL:
        fit = {"V03", "V04"}  # full-width graphics: scale to fit instead of centre-cropping
        s = {k: vertical(ctx, k, fn, fit=k in fit) for k, fn in s.items() if k.startswith("V")}
    return s


def feather(size, edge=140):
    """Alpha mask fading the top and bottom edges, so a fitted 16:9 frame has no visible seam."""
    w, h = size
    col = [int(255 * min(1.0, y / edge, (h - 1 - y) / edge)) for y in range(h)]
    return Image.frombytes("L", (1, h), bytes(col)).resize((w, h))


def vertical(ctx, sid, fn, fit=False):
    """Reframe a 16:9 frame into 1080x1920: centre crop scaled up, captions word by word."""
    VW, VH = 1080, 1920
    words = ctx.text[sid].split()
    ws = ctx.words.get(sid, [])
    lead = ctx.lead(sid)

    def frame(t, dur):
        src = fn(t, dur)
        out = Image.new("RGB", (VW, VH), G.BG)
        if fit:
            small = src.resize((VW, int(src.height * VW / src.width)), Image.LANCZOS)
            out.paste(small, (0, 780 - small.height // 2), feather(small.size))
        else:
            h = 1240
            w = int(src.width * h / src.height)
            big = src.resize((w, h), Image.LANCZOS)
            x = (w - VW) // 2
            out.paste(big.crop((x, 0, x + VW, h)), (0, 160))
        # current word index by time
        k = 0
        for i, w_ in enumerate(ws):
            if t - lead >= w_[1]:
                k = round(i * len(words) / max(1, len(ws)))
        chunk_start = (k // 3) * 3
        chunk = words[chunk_start:chunk_start + 3]
        if ws and t - lead >= ws[0][1] - 0.05:
            text = " ".join(chunk).upper()
            lay = G.text_layer(text, G.SANS(76, "Bold"), fill=G.INK)
            if lay.width > VW - 80:
                lay = lay.resize((VW - 80, int(lay.height * (VW - 80) / lay.width)), Image.LANCZOS)
            out.paste(lay, ((VW - lay.width) // 2, 1500), lay)
        return out
    return frame


def music(ctx):
    first, last = ctx.order[0], ctx.order[-1]
    return [(first, last, S.cue_open, 4)]


def sfx(ctx):
    if VERTICAL:
        return [("V04", 0.1, S.hit(0.7), -6)]
    at = ctx.at
    ev = [("T09", 0.1, S.hit(), -3), ("T03", 0.2, S.typing(1.2), -14), ("T08", 0.3, S.clink(), -10),
          ("T07", at("T07", "We tell you how sure"), S.whoosh(1.4), -12)]
    for i in range(3):
        ev.append(("T06", at("T06", "what's on the record") + i * 0.9, S.card_drop(), -10))
    return ev


if __name__ == "__main__":
    sys.argv = [a for a in sys.argv if a != "--vertical"]
    E.main(sys.modules[__name__])
