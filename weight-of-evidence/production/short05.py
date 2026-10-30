"""Case 05 vertical Short (9:16, ~1:50): the cold open, reframed, with word-by-word captions.

    python short05.py <short_prod> --stills | --final

Re-uses Case 05's narration and shots: no new voice, no new 3D. <short_prod> holds a
narration.json listing only the shots below (plus V01), timing.json / words.json copied
from Case 05, and vo/ + anim/ linked to Case 05's production dir. EP05_PROD points at it.
Same recipe as short04.py: 3D shots are cropped, type shots are set again natively for 9:16.
Same care rules as the episode: no image of the perpetrator, no relative identified.
"""

import os
import sys

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import edit as E  # noqa: E402
import ep05  # noqa: E402
import gfx as G  # noqa: E402
import score as S  # noqa: E402
import short02 as S2  # noqa: E402  (feather, captions, grain_v)
import short03 as S3  # noqa: E402  (reframe recipe)
import short04 as S4  # noqa: E402  (type_v, card_v)

EP05_PROD = os.environ.get("EP05_PROD", "/home/user/ovprod/ep05")
OUT_NAME = "weight_of_evidence_case05_short.mp4"
TITLE = "His Cousins' DNA Caught a Serial Killer. Should Police Search Yours? #shorts"
SILENT = {"V01": 3.6}
LEAD = dict(ep05.LEAD)  # same timing as the episode, so cues still land
PAD = dict(ep05.PAD)
PAD["S07"] = 0.8
FADE_IN = {"S01": 0.6}
FADE_OUT = {"S05": 0.6, "V01": 0.4}

VW, VH = S2.VW, S2.VH
KICKER = "THE GOLDEN STATE KILLER · CALIFORNIA"

FRAMING = {  # 3D shots: a horizontal window of the 16:9 frame, or None for a centre crop
    "S01": ((560, 1640), "RECONSTRUCTION"),
    "S07": (None, None),
}


def reframe(ctx, sid, fn):
    S3.FRAMING[sid] = FRAMING[sid]
    S3.KICKER = KICKER
    return S3.reframe(ctx, sid, fn)


def strike_v(ctx, sid):
    """'NOT A POLICE DATABASE' struck through, then 'A FAMILY TREE', set for 9:16."""
    t_strike = ctx.at(sid, "He wasn't found", end=True)
    t_tree = ctx.at(sid, "He was found through")

    def frame(t, dur):
        out = Image.new("RGB", (VW, VH), G.BG)
        a = G.fade(t, dur, 0.3, 0.3)
        lines = [G.text_layer(w, G.SANS(84, "SemiBold"), fill=G.DIM, spacing=0.06) for w in ("NOT A POLICE", "DATABASE")]
        y = 480
        for lay in lines:
            G.paste_alpha(out, lay, ((VW - lay.width) // 2, y), a)
            k = G.ease((t - t_strike) / 0.5)
            if k > 0:
                x0 = (VW - lay.width) // 2
                ImageDraw.Draw(out).line([x0 - 8, y + lay.height // 2 + 4, x0 - 8 + (lay.width + 16) * k,
                                          y + lay.height // 2 + 4], fill=tuple(int(c * a) for c in G.RED), width=7)
            y += 120
        tree = G.text_layer("A FAMILY TREE", G.SANS(100, "SemiBold"), fill=G.BRASS, spacing=0.06)
        G.paste_alpha(out, tree, ((VW - tree.width) // 2, 860), a * G.ease((t - t_tree) / 0.6))
        S4.kicker(out)
        S2.captions(ctx, sid, out, t)
        return S2.grain_v(out, t)
    return frame


def endcard(t, dur):
    out = Image.new("RGB", (VW, VH), G.BG)
    a = G.fade(t, dur, 0.4, 0.01)
    lines = [("FULL EPISODE ON THE CHANNEL", G.MONO(30, True), G.RED, 640, 0.0, 0.12),
             ("Should police search", G.SERIF_I(76), G.INK, 740, 0.3, 0.0),
             ("your family's DNA?", G.SERIF_I(76), G.INK, 835, 0.3, 0.0),
             ("WEIGHT OF EVIDENCE", G.SANS(54, "SemiBold"), G.INK, 1040, 0.6, 0.12),
             ("CASE 05 · THE GOLDEN STATE KILLER", G.MONO(28), G.DIM, 1130, 0.8, 0.12)]
    for text, fnt, col, y, delay, sp in lines:
        lay = G.text_layer(text, fnt, fill=col, spacing=sp)
        G.paste_alpha(out, lay, ((VW - lay.width) // 2, y), a * G.ease((t - delay) / 0.5))
    return S2.grain_v(out, t)


def build(ctx):
    S4.KICKER = KICKER  # S4.kicker reads its module's KICKER
    ep = E.Ctx(EP05_PROD, ep05)  # the episode's own timing, so its shots render exactly as cut
    shots = ep05.build(ep)
    shots["S01"] = E.clip_shot(E.Clip(EP05_PROD, "lot_push"))  # the crop would cut the lower third in half
    s = {sid: reframe(ctx, sid, shots[sid]) for sid in FRAMING}
    big = G.SANS(96, "SemiBold")
    s["S02"] = S4.type_v(ctx, "S02", [("MATCH", G.SANS(150, "SemiBold"), G.BRASS, 0.4),
                                      ("DNA from a double murder", G.SERIF_I(52), G.DIM, "double murder"),
                                      ("Ventura County · 1980", G.MONO(34, True), G.DIM, "double murder")])
    s["S03"] = strike_v(ctx, "S03")
    s["S04"] = S4.card_v(ctx, "S04", "The relatives whose DNA led to him were never asked, and most have never been named.",
                         "INFERENCE", ep05.LAT + " · AP, 2018")
    s["S05"] = S4.type_v(ctx, "S05", [("MURDERED", G.MONO(34, True), G.DIM, 0.3),
                                      ("13", G.SANS(200, "SemiBold"), G.INK, "he murdered"),
                                      ("between 1975 and 1986, and dozens more attacked", G.SANS(44), G.DIM, "he murdered")],
                         source=ep05.DAS, label="RECORD", y0=480)
    s["S06"] = S4.type_v(ctx, "S06", [("CASES CLEARED BY", G.MONO(34, True), G.DIM, 0.3),
                                      ("GENETIC GENEALOGY", G.MONO(34, True), G.DIM, 0.3),
                                      ("1,182", G.SANS(170, "SemiBold"), G.BRASS, "well over"),
                                      ("to February 2024 · one researcher's count", G.SANS(44), G.DIM, "well over")],
                         source="T. L. Dowdeswell, 2024", y0=460)
    s["V01"] = endcard
    return s


def music(ctx):
    return [("S01", "V01", S.cue_open, 2)]


def sfx(ctx):
    return [("S01", 0.0, S.hum(ctx.dur["S01"], vol=0.025), -18), ("S02", 0.3, S.hit(0.4), -12),
            ("S04", 0.0, S.card_drop(), -10), ("S05", 0.4, S.hit(0.5), -10), ("V01", 0.1, S.hit(0.7), -6)]


if __name__ == "__main__":
    E.main(sys.modules[__name__])
