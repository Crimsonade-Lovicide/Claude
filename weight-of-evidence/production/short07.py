"""Case 07 vertical Short (9:16, ~1:35): the cold open, reframed, with word-by-word captions.

    python short07.py <short_prod> --stills | --final

Re-uses Case 07's narration and footage: no new voice, no new 3D. <short_prod> holds a
narration.json listing only the shots below (plus V01), timing.json / words.json copied
from Case 07, and vo/ linked to Case 07's production dir. EP07_PROD points at the hybrid
production (its anim/ holds the Blender and generated clips). Type shots are set natively for
9:16 and laid over the episode's footage cropped to vertical (footage.over_v), as in the episode.
Same care rules as the episode: no image of Terri Schiavo, nothing from the videotapes, places
and objects only.
"""

import os
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import edit as E  # noqa: E402
import ep07  # noqa: E402
import ep07v2  # noqa: E402
import footage as F  # noqa: E402
import gfx as G  # noqa: E402
import score as S  # noqa: E402
import short02 as S2  # noqa: E402  (feather, captions, grain_v)
import short03 as S3  # noqa: E402  (reframe recipe)
import short04 as S4  # noqa: E402  (type_v, card_v)

EP07_PROD = os.environ.get("EP07_PROD", "/home/user/ovprod/ep07v2")
OUT_NAME = "weight_of_evidence_case07_short.mp4"
TITLE = "Congress Passed a Law for One Woman. Who Should Decide When We Die? #shorts"
SILENT = {"V01": 3.6}
LEAD = dict(ep07.LEAD)  # same timing as the episode, so cues still land
PAD = dict(ep07.PAD)
PAD["S07"] = 0.8
FADE_IN = {"S01": 0.6}
FADE_OUT = {"S06": 0.6, "V01": 0.4}

VW, VH = S2.VW, S2.VH
KICKER = "TERRI SCHIAVO · FLORIDA · 1990–2005"

def captions_only(ctx, sid):
    """Kicker and word-by-word captions on black: laid over clean footage by over_v."""
    def frame(t, dur):
        out = Image.new("RGB", (VW, VH), G.BG)
        S3.kicker(out)
        S2.captions(ctx, sid, out, t)
        return out
    return frame


def endcard(t, dur):
    out = Image.new("RGB", (VW, VH), G.BG)
    a = G.fade(t, dur, 0.4, 0.01)
    lines = [("FULL EPISODE ON THE CHANNEL", G.MONO(30, True), G.RED, 620, 0.0, 0.12),
             ("Who should decide", G.SERIF_I(76), G.INK, 720, 0.3, 0.0),
             ("when to stop keeping", G.SERIF_I(76), G.INK, 815, 0.3, 0.0),
             ("someone alive?", G.SERIF_I(76), G.INK, 910, 0.3, 0.0),
             ("WEIGHT OF EVIDENCE", G.SANS(54, "SemiBold"), G.INK, 1100, 0.6, 0.12),
             ("CASE 07 · TERRI SCHIAVO", G.MONO(28), G.DIM, 1190, 0.8, 0.12)]
    for text, fnt, col, y, delay, sp in lines:
        lay = G.text_layer(text, fnt, fill=col, spacing=sp)
        G.paste_alpha(out, lay, ((VW - lay.width) // 2, y), a * G.ease((t - delay) / 0.5))
    return S2.grain_v(out, t)


def build(ctx):
    S4.KICKER = KICKER  # S4.kicker reads its module's KICKER
    S3.KICKER = KICKER
    at = ctx.at

    def B(*items):
        return F.broll(EP07_PROD, list(items), tags=ep07v2.TAGS, stamp=False)

    s = {}
    s["S02"] = S4.card_v(ctx, "S02", "“Any parent of Theresa Marie Schiavo shall have standing … Nothing in this Act "
                                     "shall constitute a precedent with respect to future legislation.”", "RECORD",
                         "Pub. L. 109-3, March 21, 2005")
    s["S03"] = S4.type_v(ctx, "S03", [("FEBRUARY 25, 1990", G.MONO(34, True), G.DIM, 0.3),
                                      ("26", G.SANS(200, "SemiBold"), G.INK, "when she was"),
                                      ("her heart stopped at home in Florida", G.SANS(44), G.DIM, "her heart had")],
                         source=ep07.GREER + " · Medical Examiner, 2005", label="RECORD", y0=480)
    s["S04"] = S4.type_v(ctx, "S04", [("NOTHING IN WRITING", G.MONO(34, True), G.DIM, 0.3),
                                      ("HER HUSBAND", G.MONO(34, True), G.BRASS, "Her husband"),
                                      ("She wouldn't want to live like that", G.SANS(52), G.INK, "Her husband"),
                                      ("HER PARENTS", G.MONO(34, True), G.BRASS, "Her parents"),
                                      ("She is still aware", G.SANS(52), G.INK, "Her parents"),
                                      ("A JUDGE", G.MONO(34, True), G.BRASS, "A judge"),
                                      ("Sided with her husband", G.SANS(52), G.INK, "A judge")],
                         source=ep07.GREER + " · Wolfson report, 2003", label="INFERENCE", y0=420)
    s["S05"] = S4.type_v(ctx, "S05", [("MARCH 2005", G.MONO(40, True), G.BRASS, 0.3),
                                      ("THE FEDERAL COURTS DECLINE", G.SANS(72, "SemiBold"), G.INK, "declined"),
                                      ("She died thirteen days after the tube was removed. She was 41.", G.SANS(44),
                                       G.DIM, "She died")],
                         source="Eleventh Circuit, 2005 · Medical Examiner, 2005", label="RECORD", y0=480)
    s["S06"] = S4.type_v(ctx, "S06", [("US ADULTS WITH AN ADVANCE DIRECTIVE", G.MONO(34, True), G.DIM, 0.3),
                                      ("1 IN 3", G.SANS(200, "SemiBold"), G.BRASS, "only about"),
                                      ("a review of 150 studies, 2011–2016", G.SANS(44), G.DIM, "only about")],
                         source="Yadav et al., Health Affairs, 2017", label="RECORD", y0=480)
    # the footage under each shot, as in the episode's cold open
    t_card, t_par = at("S03", "when she was"), at("S03", "Paramedics")
    t_h, t_p, t_j = at("S04", "Her husband"), at("S04", "Her parents"), at("S04", "A judge")
    t_hw, t_ju = at("S07", "Their husband"), at("S07", "A judge")
    t_po, t_ow = at("S07", "Politicians"), at("S07", "And what should")
    t2 = at("S01", "Within the hour")
    s["S01"] = F.over_v(B(("ai_dome", 5.2), ("ai_house_chamber", t2 - 5.2), "ai_pen_sign"),
                        captions_only(ctx, "S01"), dim=1, blur=0)
    s["S02"] = F.over_v(B("desk_act_push"), s["S02"], clear_until=1.2, cx=0.45)
    s["S03"] = F.over_v(B(("ai_fl_street", t_card), ("ai_lights", t_par - t_card), "corridor"), s["S03"],
                        clear_until=t_card)
    s["S04"] = F.over_v(B(("desk_blank_pen", t_h), ("ai_ring", t_p - t_h), ("ai_sunrise", t_j - t_p), "court_bench"),
                        s["S04"], clear_until=t_h)
    s["S05"] = F.over_v(B(("ai_vigil", 4.6), "ai_tv_trucks"), s["S05"])
    s["S06"] = F.over_v(B("desk_directive"), s["S06"], clear_until=at("S06", "only about"))
    s["S07"] = F.over_v(B(("scale_empty", t_hw), ("ai_two_chairs", t_ju - t_hw), ("court_push", t_po - t_ju, 4.0),
                          ("ai_dome", t_ow - t_po), ("desk_directive", None, 4.0)),
                        captions_only(ctx, "S07"), dim=1, blur=0)
    s["V01"] = endcard
    return s


def music(ctx):
    return [("S01", "V01", S.cue_open, 2)]


def sfx(ctx):
    return [("S01", 0.0, S.hum(ctx.dur["S01"], vol=0.025), -18), ("S02", 0.0, S.card_drop(), -10),
            ("S03", 0.4, S.hit(0.5), -10), ("S06", 0.4, S.hit(0.4), -12), ("V01", 0.1, S.hit(0.7), -6)]


if __name__ == "__main__":
    E.main(sys.modules[__name__])
