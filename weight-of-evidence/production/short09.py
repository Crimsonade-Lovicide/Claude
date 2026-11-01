"""Case 09 vertical Short (9:16): the cold open, reframed, with word-by-word captions.

    python short09.py <short_prod> --stills | --final

Re-uses Case 09's narration and footage: no new voice, no new 3D. <short_prod> holds a
narration.json listing only the shots below (plus V01), timing.json / words.json copied
from Case 09, and vo/ linked to Case 09's production dir. EP09_PROD points at the episode's
production (its anim/ holds the Blender and generated clips). Type shots are set natively for
9:16 and laid over the episode's footage cropped to vertical (footage.over_v), as in the episode.
Same care rules as the episode: no image of anyone involved, no fire imagery (the cold open has
none), the children only as the narration names them.
"""

import os
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import edit as E  # noqa: E402
import ep09  # noqa: E402
import footage as F  # noqa: E402
import gfx as G  # noqa: E402
import score as S  # noqa: E402
import short02 as S2  # noqa: E402  (feather, captions, grain_v)
import short03 as S3  # noqa: E402  (reframe recipe)
import short04 as S4  # noqa: E402  (type_v, card_v)

EP09_PROD = os.environ.get("EP09_PROD", "/home/user/ovprod/ep09")
OUT_NAME = "weight_of_evidence_case09_short.mp4"
TITLE = "A Fire Scientist Said the Arson Evidence Didn't Hold Up. Texas Executed Him 4 Days Later. #shorts"
SILENT = {"V01": 3.6}
LEAD = dict(ep09.LEAD)  # same timing as the episode, so cues still land
PAD = dict(ep09.PAD)
PAD["S07"] = 0.8
FADE_IN = {"S01": 0.6}
FADE_OUT = {"S06": 0.6, "V01": 0.4}

VW, VH = S2.VW, S2.VH
KICKER = "CAMERON TODD WILLINGHAM · TEXAS · 1991–2004"
CARD = 3.0  # cards land this far in, over footage that plays clean first (as CARD_AT in the episode)


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
             ("Should a state", G.SERIF_I(76), G.INK, 720, 0.3, 0.0),
             ("execute someone when", G.SERIF_I(76), G.INK, 815, 0.3, 0.0),
             ("the evidence is disputed?", G.SERIF_I(76), G.INK, 910, 0.3, 0.0),
             ("WEIGHT OF EVIDENCE", G.SANS(54, "SemiBold"), G.INK, 1100, 0.6, 0.12),
             ("CASE 09 · CAMERON TODD WILLINGHAM", G.MONO(28), G.DIM, 1190, 0.8, 0.12)]
    for text, fnt, col, y, delay, sp in lines:
        lay = G.text_layer(text, fnt, fill=col, spacing=sp)
        G.paste_alpha(out, lay, ((VW - lay.width) // 2, y), a * G.ease((t - delay) / 0.5))
    return S2.grain_v(out, t)


def build(ctx):
    S4.KICKER = KICKER  # S4.kicker reads its module's KICKER
    S3.KICKER = KICKER
    at = ctx.at
    mono, sans = G.MONO(34, True), G.SANS(52)

    def B(*items):
        return F.broll(EP09_PROD, list(items), tags=ep09.TAGS, stamp=False)

    s = {}
    s["S02"] = S4.card_v(ctx, "S02", "“…most of the conclusions reached by the Fire Marshall would be considered "
                         "invalid in light of current knowledge.”", "RECORD",
                         "Dr. Gerald Hurst, clemency report, Feb 13, 2004")
    s["S03"] = S4.type_v(ctx, "S03", [("DEC 23, 1991", mono, G.BRASS, "The fire was"),
                                      ("A house fire in Corsicana, Texas", sans, G.INK, "The fire was"),
                                      ("AUG 1992", mono, G.BRASS, "Their father"),
                                      ("Convicted of capital murder", sans, G.INK, "Their father"),
                                      ("FEB 17, 2004", mono, G.BRASS, "Their father"),
                                      ("Executed", sans, G.INK, "Their father")],
                         source="Willingham v. State, 1995 · TDCJ", label="RECORD", y0=420)
    s["S04"] = S4.type_v(ctx, "S04", [("FEB 13, 2004", mono, G.BRASS, "The parole board"),
                                      ("Parole board: 15–0 against clemency", sans, G.INK, "The parole board"),
                                      ("FEB 17, 2004", mono, G.BRASS, "The governor"),
                                      ("No reprieve from the governor; executed", sans, G.INK, "The governor")],
                         source="Board of Pardons and Paroles · TDCJ", label="RECORD", y0=420)
    t_st = max(0.5, at("S05", "And the girls'") - CARD)  # the whole shot is delayed by CARD
    s["S05"] = G.seq((S4.card_v(ctx, "S05", "“A finding of arson could not be sustained.”", "RECORD",
                                "Craig Beyler, Texas Forensic Science Commission, 2009"), t_st),
                     (S4.card_v(ctx, "S05", "“My ex-husband murdered my daughters, and just before he was executed, "
                                "he told me he did it.”", "ARGUMENT", "Stacy Kuykendall, Oct 6, 2010"), 1))
    s["S06"] = S4.type_v(ctx, "S06", [("DEATH SENTENCES THAT ARE FALSE CONVICTIONS", mono, G.DIM, 0.3),
                                      ("4%", G.SANS(200, "SemiBold"), G.BRASS, "at least four"),
                                      ("at least · a conservative estimate", G.SANS(44), G.DIM, "at least four")],
                         source="Gross, O'Brien, Hu & Kennedy, PNAS, 2014", label="RECORD", y0=480)
    # the footage under each shot, as in the episode's cold open
    c1, c2 = at("S01", "A fire scientist"), at("S01", "The execution")
    s["S01"] = F.over_v(B(("fax_push", c1), ("ai_capitol", c2 - c1), "fax_page"),
                        captions_only(ctx, "S01"), dim=1, blur=0)
    s["S02"] = F.over_v(B(("fax_page", 6), "desk_hurst"), F.delay(s["S02"], CARD), clear_until=CARD)
    c1 = at("S03", "The fire was")
    s["S03"] = F.over_v(B(("ai_tx_town", c1 + 4), "ai_tx_road"), s["S03"], clear_until=c1)
    c1, c2 = at("S04", "The parole board"), at("S04", "The governor")
    s["S04"] = F.over_v(B(("ai_hearing", c2), ("ai_capitol", 5), "ai_razor_wire"), s["S04"], clear_until=c1)
    s["S05"] = F.over_v(B(("ai_fire_lab", 6), ("desk_beyler", 7), "ai_tx_road"), F.delay(s["S05"], CARD),
                        clear_until=CARD)
    c1 = at("S06", "at least four")
    s["S06"] = F.over_v(B(("ai_razor_wire", c1 + 2), "tier_corridor"), s["S06"], clear_until=c1)
    s["S07"] = F.over_v(B(("scale_empty", 6), ("fax_page", 6), ("ai_court_corridor", 5), "scale_empty"),
                        captions_only(ctx, "S07"), dim=1, blur=0)
    s["V01"] = endcard
    return s


def music(ctx):
    return [("S01", "V01", S.cue_open, 2)]


def sfx(ctx):
    at = ctx.at
    return [("S01", 0.0, S.hum(ctx.dur["S01"], vol=0.025), -18), ("S02", CARD, S.card_drop(), -10),
            ("S05", CARD, S.card_drop(), -10), ("S06", at("S06", "at least four"), S.hit(0.4), -12),
            ("V01", 0.1, S.hit(0.7), -6)]


if __name__ == "__main__":
    E.main(sys.modules[__name__])
