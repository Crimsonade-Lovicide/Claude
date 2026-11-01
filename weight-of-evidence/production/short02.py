"""Case 02 vertical Short (9:16, ~75 s): the cold open, reframed, with word-by-word captions.

    python short02.py <short_prod> --stills | --final

Re-uses Case 02's narration and shots: no new voice, no new 3D. <short_prod> holds a
narration.json listing only the shots below (plus V01), timing.json / words.json copied
from Case 02, and vo/ + anim/ linked to Case 02's production dir. EP02_PROD points at it.
"""

import os
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import edit as E  # noqa: E402
import ep02  # noqa: E402
import gfx as G  # noqa: E402
import score as S  # noqa: E402

EP02_PROD = os.environ.get("EP02_PROD", "/home/user/ovprod/ep02")
OUT_NAME = "weight_of_evidence_case02_short.mp4"
TITLE = "The car saw her 5.6 seconds early. Who's guilty? #shorts"
SILENT = {"V01": 3.6}
LEAD = {k: v for k, v in ep02.LEAD.items()}  # same timing as the episode, so cues still land
PAD = {k: v for k, v in ep02.PAD.items()}
PAD["S07"] = 0.8
FADE_IN = {}
FADE_OUT = {"S05": 0.6, "V01": 0.4}

VW, VH = 1080, 1920
KICKER = "SELF-DRIVING UBER · TEMPE, ARIZONA · 2018"

# How each 16:9 shot sits in 9:16: a horizontal window of the source (fit to width),
# or None for a centre crop of the full height. Tags are redrawn because crops cut them off.
FRAMING = {
    "S02": ((180, 1420), "RECONSTRUCTION FROM NTSB DATA"),
    "S03": ((480, 1440), None),
    "S04": (None, "RECONSTRUCTION"),
    "S05": ((480, 1440), None),
    "S07": (None, None),
}


def feather(size, edge=110):
    w, h = size
    col = [int(255 * min(1.0, y / edge, (h - 1 - y) / edge)) for y in range(h)]
    return Image.frombytes("L", (1, h), bytes(col)).resize((w, h))


def captions(ctx, sid, out, t):
    """Three words at a time, uppercase, timed to the aligned narration."""
    words = ctx.text[sid].split()
    ws = ctx.words.get(sid, [])
    lead = ctx.lead(sid)
    if not ws or t - lead < ws[0][1] - 0.05:
        return
    k = 0
    for i, w in enumerate(ws):
        if t - lead >= w[1]:
            k = round(i * len(words) / max(1, len(ws)))
    chunk = words[(k // 3) * 3:(k // 3) * 3 + 3]
    lay = G.text_layer(" ".join(chunk).upper(), G.SANS(76, "Bold"), fill=G.INK)
    if lay.width > VW - 100:
        lay = lay.resize((VW - 100, int(lay.height * (VW - 100) / lay.width)), Image.LANCZOS)
    out.paste(lay, ((VW - lay.width) // 2, 1480), lay)


def reframe(ctx, sid, fn):
    window, tag = FRAMING[sid]

    def frame(t, dur):
        src = fn(t, dur)
        out = Image.new("RGB", (VW, VH), G.BG)
        if window:
            x0, x1 = window
            part = src.crop((x0, 0, x1, src.height))
            part = part.resize((VW, int(part.height * VW / part.width)), Image.LANCZOS)
            out.paste(part, (0, 800 - part.height // 2), feather(part.size))
        else:
            h = 1240
            big = src.resize((int(src.width * h / src.height), h), Image.LANCZOS)
            x = (big.width - VW) // 2
            out.paste(big.crop((x, 0, x + VW, h)), (0, 180))
        a = G.fade(t, dur, 0.3, 0.3)
        k = G.text_layer(KICKER, G.MONO(26, True), fill=G.BRASS, spacing=0.12)
        G.paste_alpha(out, k, ((VW - k.width) // 2, 92), 0.9)
        if tag:
            s = G.stamp(tag, 18)
            G.paste_alpha(out, s, (VW - s.width - 40, 196), 0.85 * a)
        captions(ctx, sid, out, t)
        return out
    return frame


def endcard(t, dur):
    out = Image.new("RGB", (VW, VH), G.BG)
    a = G.fade(t, dur, 0.4, 0.01)
    lines = [("FULL EPISODE ON THE CHANNEL", G.MONO(30, True), G.RED, 640, 0.0),
             ("Who's guilty?", G.SERIF_I(92), G.INK, 760, 0.3),
             ("WEIGHT OF EVIDENCE", G.SANS(54, "SemiBold"), G.INK, 1010, 0.6),
             ("CASE 02 · THE SAFETY DRIVER", G.MONO(28), G.DIM, 1100, 0.8)]
    for text, fnt, col, y, delay in lines:
        lay = G.text_layer(text, fnt, fill=col, spacing=0.0 if col == G.INK and y == 760 else 0.12)
        G.paste_alpha(out, lay, ((VW - lay.width) // 2, y), a * G.ease((t - delay) / 0.5))
    return grain_v(out, t)


def grain_v(img, t):
    """The kit's film grain, transposed to fit a 9:16 frame."""
    import numpy as np
    g = G._grain_frames()[int(t * G.FPS) % 8].T
    a = np.asarray(img).astype(np.float32) + g[..., None]
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def timeline(ctx):
    """S06 rebuilt for 9:16: the three dated rows stacked large enough to read on a phone."""
    rows = [("MARCH 2018", "Uber settles with her family", "Ten days later"),
            ("MARCH 2019", "No criminal charges for Uber", "A year later"),
            ("AUGUST 2020", "Safety driver charged with negligent homicide", "Two years after")]
    times = [ctx.at("S06", r[2]) for r in rows]

    def frame(t, dur):
        out = Image.new("RGB", (VW, VH), G.BG)
        a = G.fade(t, dur, 0.3, 0.3)
        y = 420
        for (date, event, _), at in zip(rows, times):
            k = a * G.ease((t - at) / 0.5)
            d = G.text_layer(date, G.MONO(32, True), fill=G.BRASS, spacing=0.12)
            G.paste_alpha(out, d, (110, y), k)
            for i, line in enumerate(G.wrap(event, G.SANS(58, "SemiBold"), VW - 220)):
                G.paste_alpha(out, G.text_layer(line, G.SANS(58, "SemiBold"), fill=G.INK), (110, y + 58 + i * 74), k)
            y += 300
        src = G.text_layer("Reuters/AP 2018 · Yavapai County Attorney 2019 · Maricopa County 2020", G.MONO(18), fill=G.DIM)
        G.paste_alpha(out, src, ((VW - src.width) // 2, 1340), 0.7 * a)
        k = G.text_layer(KICKER, G.MONO(26, True), fill=G.BRASS, spacing=0.12)
        G.paste_alpha(out, k, ((VW - k.width) // 2, 92), 0.9)
        captions(ctx, "S06", out, t)
        return grain_v(out, t)
    return frame


def build(ctx):
    ep = E.Ctx(EP02_PROD, ep02)  # the episode's own timing, so its shots render exactly as cut
    shots = ep02.build(ep)
    s = {sid: reframe(ctx, sid, shots[sid]) for sid in FRAMING}
    s["S06"] = timeline(ctx)
    s["V01"] = endcard
    return s


def music(ctx):
    return [("S02", "V01", S.cue_open, 2)]


def sfx(ctx):
    return [("S02", 0.0, S.hum(ctx.dur["S02"], vol=0.025), -18), ("S04", 0.0, S.hum(ctx.dur["S04"]), -18),
            ("S05", 0.4, S.hit(0.5), -10), ("V01", 0.1, S.hit(0.7), -6)]


if __name__ == "__main__":
    E.main(sys.modules[__name__])
