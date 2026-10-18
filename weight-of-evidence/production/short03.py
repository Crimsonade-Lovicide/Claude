"""Case 03 vertical Short (9:16, ~95 s): the cold open, reframed, with word-by-word captions.

    python short03.py <short_prod> --stills | --final

Re-uses Case 03's narration and shots: no new voice, no new 3D. <short_prod> holds a
narration.json listing only the shots below (plus V01), timing.json / words.json copied
from Case 03, and vo/ + anim/ linked to Case 03's production dir. EP03_PROD points at it.
Same recipe as short02.py.
"""

import os
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import edit as E  # noqa: E402
import ep03  # noqa: E402
import gfx as G  # noqa: E402
import score as S  # noqa: E402
import short02 as S2  # noqa: E402  (feather, captions, grain_v)

EP03_PROD = os.environ.get("EP03_PROD", "/home/user/ovprod/ep03")
OUT_NAME = "weight_of_evidence_case03_short.mp4"
TITLE = "They ate the cabin boy to survive. Was it murder? #shorts"
SILENT = {"V01": 3.6}
LEAD = dict(ep03.LEAD)  # same timing as the episode, so cues still land
PAD = dict(ep03.PAD)
PAD["S07"] = 0.8
FADE_IN = {"S01": 0.6}
FADE_OUT = {"S05": 0.6, "V01": 0.4}

VW, VH = S2.VW, S2.VH
KICKER = "THE MIGNONETTE · SOUTH ATLANTIC · 1884"

# How each 16:9 shot sits in 9:16: a horizontal window of the source (fit to width), or None
# for a centre crop of the full height. Tags are redrawn because crops cut them off.
FRAMING = {
    "S01": ((560, 1640), "RECONSTRUCTION"),
    "S03": ((480, 1440), None),
    "S04": ((290, 1630), "RECONSTRUCTION"),
    "S05": ((480, 1440), None),
    "S07": (None, None),
}
ROWS = {  # text-row shots rebuilt natively for 9:16
    "S02": ([("", "2 tins of turnips", "two tins"), ("DAY 4", "1 small turtle", "On the fourth day"),
             ("LAST 8 DAYS", "Nothing at all", "For the last eight days")], "Special verdict, Exeter, 1884"),
    "S06": ([("SEPT 1884", "They tell the authorities everything", "When they reached England"),
             ("DEC 1884", "Sentenced to death for murder", "Three months later"),
             ("1885", "Released after six months", "They served six months")], "Falmouth depositions · R v Dudley and Stephens · HO 144/141"),
}


def kicker(out):
    k = G.text_layer(KICKER, G.MONO(26, True), fill=G.BRASS, spacing=0.12)
    G.paste_alpha(out, k, ((VW - k.width) // 2, 92), 0.9)


def reframe(ctx, sid, fn):
    window, tag = FRAMING[sid]

    def frame(t, dur):
        src = fn(t, dur)
        out = Image.new("RGB", (VW, VH), G.BG)
        if window:
            x0, x1 = window
            part = src.crop((x0, 0, x1, src.height))
            part = part.resize((VW, int(part.height * VW / part.width)), Image.LANCZOS)
            out.paste(part, (0, 800 - part.height // 2), S2.feather(part.size))
        else:
            h = 1240
            big = src.resize((int(src.width * h / src.height), h), Image.LANCZOS)
            x = (big.width - VW) // 2
            out.paste(big.crop((x, 0, x + VW, h)), (0, 180))
        a = G.fade(t, dur, 0.3, 0.3)
        kicker(out)
        if tag:
            s = G.stamp(tag, 18)
            G.paste_alpha(out, s, (VW - s.width - 40, 196), 0.85 * a)
        S2.captions(ctx, sid, out, t)
        return out
    return frame


def rows_v(ctx, sid):
    rows, source = ROWS[sid]
    times = [ctx.at(sid, r[2]) for r in rows]

    def frame(t, dur):
        out = Image.new("RGB", (VW, VH), G.BG)
        a = G.fade(t, dur, 0.3, 0.3)
        y = 420
        for (date, event, _), at in zip(rows, times):
            k = a * G.ease((t - at) / 0.5)
            if date:
                G.paste_alpha(out, G.text_layer(date, G.MONO(32, True), fill=G.BRASS, spacing=0.12), (110, y), k)
            for i, line in enumerate(G.wrap(event, G.SANS(58, "SemiBold"), VW - 220)):
                G.paste_alpha(out, G.text_layer(line, G.SANS(58, "SemiBold"), fill=G.INK), (110, y + 58 + i * 74), k)
            y += 300
        src = G.text_layer(source, G.MONO(18), fill=G.DIM)
        G.paste_alpha(out, src, ((VW - src.width) // 2, 1340), 0.7 * a)
        kicker(out)
        S2.captions(ctx, sid, out, t)
        return S2.grain_v(out, t)
    return frame


def endcard(t, dur):
    out = Image.new("RGB", (VW, VH), G.BG)
    a = G.fade(t, dur, 0.4, 0.01)
    lines = [("FULL EPISODE ON THE CHANNEL", G.MONO(30, True), G.RED, 640, 0.0, 0.12),
             ("Was it murder?", G.SERIF_I(92), G.INK, 760, 0.3, 0.0),
             ("WEIGHT OF EVIDENCE", G.SANS(54, "SemiBold"), G.INK, 1010, 0.6, 0.12),
             ("CASE 03 · THE MIGNONETTE", G.MONO(28), G.DIM, 1100, 0.8, 0.12)]
    for text, fnt, col, y, delay, sp in lines:
        lay = G.text_layer(text, fnt, fill=col, spacing=sp)
        G.paste_alpha(out, lay, ((VW - lay.width) // 2, y), a * G.ease((t - delay) / 0.5))
    return S2.grain_v(out, t)


def build(ctx):
    ep = E.Ctx(EP03_PROD, ep03)  # the episode's own timing, so its shots render exactly as cut
    shots = ep03.build(ep)
    s = {sid: reframe(ctx, sid, shots[sid]) for sid in FRAMING}
    for sid in ROWS:
        s[sid] = rows_v(ctx, sid)
    s["V01"] = endcard
    return s


def music(ctx):
    return [("S01", "V01", S.cue_open, 2)]


def sfx(ctx):
    return [("S01", 0.0, S.sea(ctx.dur["S01"], 0.05), -16), ("S05", 0.4, S.hit(0.5), -10),
            ("V01", 0.1, S.hit(0.7), -6)]


if __name__ == "__main__":
    E.main(sys.modules[__name__])
