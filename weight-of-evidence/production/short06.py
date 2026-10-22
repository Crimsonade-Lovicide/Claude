"""Case 06 vertical Short (9:16, ~1:50): the cold open, reframed, with word-by-word captions.

    python short06.py <short_prod> --stills | --final

Re-uses Case 06's narration and shots: no new voice, no new 3D. <short_prod> holds a
narration.json listing only the shots below (plus V01), timing.json / words.json copied
from Case 06, and vo/ + anim/ linked to Case 06's production dir. EP06_PROD points at it.
Same recipe as short05.py: 3D shots are cropped, type shots are set again natively for 9:16.
Same care rules as the episode: no image of the five men, nothing from the videotapes.
"""

import os
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import edit as E  # noqa: E402
import ep06  # noqa: E402
import gfx as G  # noqa: E402
import score as S  # noqa: E402
import short02 as S2  # noqa: E402  (feather, captions, grain_v)
import short03 as S3  # noqa: E402  (reframe recipe)
import short04 as S4  # noqa: E402  (type_v, card_v)

EP06_PROD = os.environ.get("EP06_PROD", "/home/user/ovprod/ep06")
OUT_NAME = "weight_of_evidence_case06_short.mp4"
TITLE = "Police Can Still Lie to You in Every State. Should They? #shorts"
SILENT = {"V01": 3.6}
LEAD = dict(ep06.LEAD)  # same timing as the episode, so cues still land
PAD = dict(ep06.PAD)
PAD["S07"] = 0.8
FADE_IN = {"S01": 0.6}
FADE_OUT = {"S05": 0.6, "V01": 0.4}

VW, VH = S2.VW, S2.VH
KICKER = "THE CENTRAL PARK FIVE · NEW YORK · 1989"

FRAMING = {  # 3D shots: a horizontal window of the 16:9 frame, or None for a centre crop
    "S01": ((700, 1780), "RECONSTRUCTION"),
    "S07": (None, None),
}


def reframe(ctx, sid, fn):
    S3.FRAMING[sid] = FRAMING[sid]
    S3.KICKER = KICKER
    return S3.reframe(ctx, sid, fn)


def endcard(t, dur):
    out = Image.new("RGB", (VW, VH), G.BG)
    a = G.fade(t, dur, 0.4, 0.01)
    lines = [("FULL EPISODE ON THE CHANNEL", G.MONO(30, True), G.RED, 640, 0.0, 0.12),
             ("Should police be allowed", G.SERIF_I(76), G.INK, 740, 0.3, 0.0),
             ("to lie to you?", G.SERIF_I(76), G.INK, 835, 0.3, 0.0),
             ("WEIGHT OF EVIDENCE", G.SANS(54, "SemiBold"), G.INK, 1040, 0.6, 0.12),
             ("CASE 06 · THE CENTRAL PARK FIVE", G.MONO(28), G.DIM, 1130, 0.8, 0.12)]
    for text, fnt, col, y, delay, sp in lines:
        lay = G.text_layer(text, fnt, fill=col, spacing=sp)
        G.paste_alpha(out, lay, ((VW - lay.width) // 2, y), a * G.ease((t - delay) / 0.5))
    return S2.grain_v(out, t)


def build(ctx):
    S4.KICKER = KICKER  # S4.kicker reads its module's KICKER
    ep = E.Ctx(EP06_PROD, ep06)  # the episode's own timing, so its shots render exactly as cut
    shots = ep06.build(ep)
    shots["S01"] = E.clip_shot(E.Clip(EP06_PROD, "room_push"), tag=None)  # the crop adds its own tag; no half lower third
    s = {sid: reframe(ctx, sid, shots[sid]) for sid in FRAMING}
    s["S02"] = S4.type_v(ctx, "S02", [("VIDEOTAPED STATEMENTS", G.MONO(34, True), G.DIM, 0.3),
                                      ("4 OF 5", G.SANS(200, "SemiBold"), G.INK, "Four of them"),
                                      ("the fifth was never recorded", G.SANS(44), G.DIM, "The fifth")],
                         source=ep06.AFF, label="RECORD", y0=480)
    s["S03"] = S4.card_v(ctx, "S03", "A detective told him his fingerprints could be on her clothing. "
                                     "There were no such prints.", "INFERENCE",
                         "Trial testimony, as reported by the New York Times")
    s["S04"] = S4.type_v(ctx, "S04", [("NO PHYSICAL", G.SANS(110, "SemiBold"), G.INK, 0.3),
                                      ("EVIDENCE", G.SANS(110, "SemiBold"), G.INK, 0.3),
                                      ("the DNA at the scene matched none of them", G.SANS(44), G.DIM,
                                       "The DNA found"),
                                      ("CONVICTED · 1990", G.MONO(40, True), G.BRASS, "convicted anyway")], y0=460)
    s["S05"] = S4.type_v(ctx, "S05", [("2002", G.MONO(40, True), G.BRASS, 0.3),
                                      ("ANOTHER MAN'S DNA", G.SANS(84, "SemiBold"), G.INK, "His DNA"),
                                      ("every conviction vacated", G.SANS(52), G.DIM, "asked the court")],
                         source=ep06.AFF, label="RECORD", y0=480)
    s["S06"] = S4.card_v(ctx, "S06", "In every state, police may still lie to adults about the evidence. "
                                     "Ten states now restrict it for children.", "INFERENCE",
                         "Frazier v. Cupp, 1969 · Kassin et al., 2025")
    s["V01"] = endcard
    return s


def music(ctx):
    return [("S01", "V01", S.cue_open, 2)]


def sfx(ctx):
    return [("S01", 0.0, S.hum(ctx.dur["S01"], vol=0.025), -18), ("S02", 0.4, S.hit(0.5), -10),
            ("S03", 0.0, S.card_drop(), -10), ("S04", 0.3, S.hit(0.4), -12), ("S06", 0.0, S.card_drop(), -10),
            ("V01", 0.1, S.hit(0.7), -6)]


if __name__ == "__main__":
    E.main(sys.modules[__name__])
