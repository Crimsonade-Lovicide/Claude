"""Case 04 vertical Short (9:16, ~105 s): the cold open, reframed, with word-by-word captions.

    python short04.py <short_prod> --stills | --final

Re-uses Case 04's narration and shots: no new voice, no new 3D. <short_prod> holds a
narration.json listing only the shots below (plus V01), timing.json / words.json copied
from Case 04, and vo/ + anim/ linked to Case 04's production dir. EP04_PROD points at it.
Same recipe as short03.py. The type shots (S02–S06) are too wide to crop, so they are set
again natively for 9:16. Same care rules as the episode: no plate, no name next to the atlas.
"""

import os
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import edit as E  # noqa: E402
import ep04  # noqa: E402
import gfx as G  # noqa: E402
import score as S  # noqa: E402
import short02 as S2  # noqa: E402  (feather, captions, grain_v)
import short03 as S3  # noqa: E402  (reframe recipe)

EP04_PROD = os.environ.get("EP04_PROD", "/home/user/ovprod/ep04")
OUT_NAME = "weight_of_evidence_case04_short.mp4"
TITLE = "Surgeons still use this atlas from Nazi Vienna. Should they? #shorts"
SILENT = {"V01": 3.6}
LEAD = dict(ep04.LEAD)  # same timing as the episode, so cues still land
PAD = dict(ep04.PAD)
PAD["S07"] = 0.8
FADE_IN = {"S01": 0.6}
FADE_OUT = {"S05": 0.6, "V01": 0.4}

VW, VH = S2.VW, S2.VH
KICKER = "THE PERNKOPF ATLAS · VIENNA · 1937–1960"

FRAMING = {  # 3D shots: a horizontal window of the 16:9 frame, or None for a centre crop
    "S01": ((420, 1500), "RECONSTRUCTION"),
    "S07": (None, None),
}


def kicker(out):
    k = G.text_layer(KICKER, G.MONO(26, True), fill=G.BRASS, spacing=0.12)
    G.paste_alpha(out, k, ((VW - k.width) // 2, 92), 0.9)


def reframe(ctx, sid, fn):
    S3.FRAMING[sid] = FRAMING[sid]
    S3.KICKER = KICKER
    return S3.reframe(ctx, sid, fn)


def type_v(ctx, sid, items, source=None, label=None, y0=520):
    """Lines of type stacked and centred for 9:16: items = [(text, font, colour, phrase or seconds)]."""
    times = [ctx.at(sid, w) if isinstance(w, str) else w for *_, w in items]

    def frame(t, dur):
        out = Image.new("RGB", (VW, VH), G.BG)
        a = G.fade(t, dur, 0.3, 0.3)
        y = y0
        for (text, fnt, col, _), ts in zip(items, times):
            k = a * G.ease((t - ts) / 0.6)
            for line in G.wrap(text, fnt, VW - 160):
                lay = G.text_layer(line, fnt, fill=col, spacing=0.06)
                G.paste_alpha(out, lay, ((VW - lay.width) // 2, y), k)
                y += int(lay.height * 1.25)
            y += 40
        if source:
            src = G.text_layer(source, G.MONO(18), fill=G.DIM)
            G.paste_alpha(out, src, ((VW - src.width) // 2, 1340), 0.7 * a)
        if label:
            st = G.stamp(label, 18)
            G.paste_alpha(out, st, ((VW - st.width) // 2, y0 - 110), a)
        kicker(out)
        S2.captions(ctx, sid, out, t)
        return S2.grain_v(out, t)
    return frame


def card_v(ctx, sid, claim, label, source):
    card = G.evidence_card(claim, label, source, width=940)

    def frame(t, dur):
        out = Image.new("RGB", (VW, VH), G.BG)
        k = G.ease_out(t / 0.7) * G.fade(t, dur, 0.01, 0.3)
        G.paste_alpha(out, card, ((VW - card.width) // 2, 760 - card.height // 2 + int((1 - k) * 80)), k)
        kicker(out)
        S2.captions(ctx, sid, out, t)
        return S2.grain_v(out, t)
    return frame


def endcard(t, dur):
    out = Image.new("RGB", (VW, VH), G.BG)
    a = G.fade(t, dur, 0.4, 0.01)
    lines = [("FULL EPISODE ON THE CHANNEL", G.MONO(30, True), G.RED, 640, 0.0, 0.12),
             ("Should surgeons use it?", G.SERIF_I(80), G.INK, 760, 0.3, 0.0),
             ("WEIGHT OF EVIDENCE", G.SANS(54, "SemiBold"), G.INK, 1010, 0.6, 0.12),
             ("CASE 04 · THE PERNKOPF ATLAS", G.MONO(28), G.DIM, 1100, 0.8, 0.12)]
    for text, fnt, col, y, delay, sp in lines:
        lay = G.text_layer(text, fnt, fill=col, spacing=sp)
        G.paste_alpha(out, lay, ((VW - lay.width) // 2, y), a * G.ease((t - delay) / 0.5))
    return S2.grain_v(out, t)


def build(ctx):
    ep = E.Ctx(EP04_PROD, ep04)  # the episode's own timing, so its shots render exactly as cut
    shots = ep04.build(ep)
    shots["S01"] = E.clip_shot(E.Clip(EP04_PROD, "or_lamp"))  # the crop would cut the lower third in half
    s = {sid: reframe(ctx, sid, shots[sid]) for sid in FRAMING}
    big = G.SANS(96, "SemiBold")
    s["S02"] = type_v(ctx, "S02", [("ONE PAGE", G.SANS(130, "SemiBold"), G.BRASS, 0.4),
                                   ("from an atlas printed in 1963", G.SERIF_I(52), G.DIM, "an old anatomy atlas")])
    s["S03"] = type_v(ctx, "S03", [("TOPOGRAPHISCHE ANATOMIE DES MENSCHEN", G.SANS(64, "SemiBold"), G.INK, 0.4),
                                   ("Vienna · 1937–1960", G.SERIF_I(52), G.DIM, "between")])
    s["S04"] = type_v(ctx, "S04", [("AT LEAST", G.MONO(34, True), G.DIM, 0.3),
                                   ("1,377", G.SANS(170, "SemiBold"), G.INK, "at least"),
                                   ("people executed by the Nazi regime whose bodies went to his institute, 1938–1945",
                                    G.SANS(44), G.DIM, "at least")],
                      source="University of Vienna, Senate Project, 1998", label="RECORD", y0=480)
    s["S05"] = type_v(ctx, "S05", [("NO ONE IN ANY PAINTING", big, G.INK, "No one in any"),
                                   ("HAS EVER BEEN IDENTIFIED", big, G.INK, "has ever been")])
    s["S06"] = card_v(ctx, "S06", "The patient was not told at the time that the atlas had been used.",
                      "INFERENCE", "STAT, May 30, 2019")
    s["V01"] = endcard
    return s


def music(ctx):
    return [("S01", "V01", S.cue_open, 2)]


def sfx(ctx):
    return [("S01", 0.0, S.hum(ctx.dur["S01"]), -16), ("S04", ctx.at("S04", "at least"), S.hit(0.4), -12),
            ("S05", 0.4, S.hit(0.5), -10), ("S06", 0.0, S.card_drop(), -10), ("V01", 0.1, S.hit(0.7), -6)]


if __name__ == "__main__":
    E.main(sys.modules[__name__])
