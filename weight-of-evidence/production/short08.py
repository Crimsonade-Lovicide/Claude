"""Case 08 vertical Short (9:16): the cold open, reframed, with word-by-word captions.

    python short08.py <short_prod> --stills | --final

Re-uses Case 08's narration and footage: no new voice, no new 3D. <short_prod> holds a
narration.json listing only the shots below (plus V01), timing.json / words.json copied
from Case 08, and vo/ linked to Case 08's production dir. EP08_PROD points at the episode's
production (its anim/ holds the Blender and generated clips). Type shots are set natively for
9:16 and laid over the episode's footage cropped to vertical (footage.over_v), as in the episode.
Same care rules as the episode: no image of Kalief Browder, nothing from the surveillance videos,
no reference to his death; the jail is the empty Blender cell.
"""

import os
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import edit as E  # noqa: E402
import ep08  # noqa: E402
import footage as F  # noqa: E402
import gfx as G  # noqa: E402
import score as S  # noqa: E402
import short02 as S2  # noqa: E402  (feather, captions, grain_v)
import short03 as S3  # noqa: E402  (reframe recipe)
import short04 as S4  # noqa: E402  (type_v, card_v)

EP08_PROD = os.environ.get("EP08_PROD", "/home/user/ovprod/ep08")
OUT_NAME = "weight_of_evidence_case08_short.mp4"
TITLE = "1,110 Days in Jail. No Trial. Should Anyone Wait That Long? #shorts"
SILENT = {"V01": 3.6}
LEAD = dict(ep08.LEAD)  # same timing as the episode, so cues still land
PAD = dict(ep08.PAD)
PAD["S07"] = 0.8
FADE_IN = {"S01": 0.6}
FADE_OUT = {"S06": 0.6, "V01": 0.4}

VW, VH = S2.VW, S2.VH
KICKER = "KALIEF BROWDER · NEW YORK · 2010–2013"


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
             ("Should anyone", G.SERIF_I(76), G.INK, 720, 0.3, 0.0),
             ("be jailed for years", G.SERIF_I(76), G.INK, 815, 0.3, 0.0),
             ("before a trial?", G.SERIF_I(76), G.INK, 910, 0.3, 0.0),
             ("WEIGHT OF EVIDENCE", G.SANS(54, "SemiBold"), G.INK, 1100, 0.6, 0.12),
             ("CASE 08 · KALIEF BROWDER", G.MONO(28), G.DIM, 1190, 0.8, 0.12)]
    for text, fnt, col, y, delay, sp in lines:
        lay = G.text_layer(text, fnt, fill=col, spacing=sp)
        G.paste_alpha(out, lay, ((VW - lay.width) // 2, y), a * G.ease((t - delay) / 0.5))
    return S2.grain_v(out, t)


def build(ctx):
    S4.KICKER = KICKER  # S4.kicker reads its module's KICKER
    S3.KICKER = KICKER
    at = ctx.at

    def B(*items):
        return F.broll(EP08_PROD, list(items), tags=ep08.TAGS, stamp=False)

    s = {}
    s["S02"] = S4.type_v(ctx, "S02", [("ACCUSED", G.MONO(34, True), G.BRASS, "He was accused"),
                                      ("Robbing a man of his backpack", G.SANS(52), G.INK, "He was accused"),
                                      ("HE SAID", G.MONO(34, True), G.BRASS, "He said"),
                                      ("“I didn't rob anybody”", G.SANS(52), G.INK, "He said"),
                                      ("THE CASE", G.MONO(34, True), G.BRASS, "The case against"),
                                      ("One man's memory", G.SANS(52), G.INK, "The case against")],
                         source="Jennifer Gonnerman, " + ep08.NY, label="INFERENCE", y0=420)
    s["S03"] = S4.type_v(ctx, "S03", [("BAIL · MAY 16, 2010", G.MONO(34, True), G.DIM, 0.3),
                                      ("$3,000", G.SANS(200, "SemiBold"), G.BRASS, "For the first"),
                                      ("His family couldn't pay", G.SANS(44), G.DIM, "For the first"),
                                      ("THEN, ON PROBATION", G.MONO(34, True), G.BRASS, "After that"),
                                      ("Held without bail", G.SANS(52), G.INK, "After that")],
                         source=ep08.NY, label="INFERENCE", y0=420)
    s["S04"] = S4.card_v(ctx, "S04", "“If you want that, I will do that today.”", "INFERENCE",
                         "Judge DiMango, March 13, 2013 · The New Yorker")
    s["S05"] = S4.type_v(ctx, "S05", [("DAYS HELD", G.MONO(34, True), G.DIM, 0.3),
                                      ("1,110", G.SANS(200, "SemiBold"), G.INK, "went into Rikers"),
                                      ("never tried · the case was dismissed", G.SANS(44), G.DIM, "went into Rikers")],
                         source="our count from The New Yorker's dates", label="INFERENCE", y0=480)
    s["S06"] = S4.type_v(ctx, "S06", [("PEOPLE IN US JAILS NOT CONVICTED", G.MONO(34, True), G.DIM, 0.3),
                                      ("450,700", G.SANS(180, "SemiBold"), G.BRASS, "In mid-2024"),
                                      ("68% of everyone in local jails · midyear 2024", G.SANS(40), G.DIM,
                                       "In mid-2024")],
                         source="Bureau of Justice Statistics, 2026", label="RECORD", y0=480)
    # the footage under each shot, as in the episode's cold open
    c1, c2 = at("S01", "He will wait"), at("S01", "The trial will")
    s["S01"] = F.over_v(B(("cell_push", c1), ("ai_bridge", c2 - c1 + 1.0), "cell_window"),
                        captions_only(ctx, "S01"), dim=1, blur=0)
    c1 = at("S02", "He was accused")
    s["S02"] = F.over_v(B(("ai_bronx_night", c1 + 4), "ai_lights"), s["S02"], clear_until=c1)
    c1, c2 = at("S03", "For the first"), at("S03", "After that")
    s["S03"] = F.over_v(B(("ai_court_ext", c2), ("court_bench", 6), "cell_door"), s["S03"], clear_until=c1)
    s["S04"] = F.over_v(B(("court_witness", 6), "court_gallery"), F.delay(s["S04"], 3.0), clear_until=3.0)
    c1, c2 = at("S05", "Then the case"), at("S05", "went into Rikers")
    s["S05"] = F.over_v(B(("ai_island", c1 + 5), ("cell_door", c2 - c1 - 5, 1.0), "tier_corridor"), s["S05"],
                        clear_until=c2)
    c1 = at("S06", "In mid-2024")
    s["S06"] = F.over_v(B(("ai_razor_wire", c1), "tier_dorm"), s["S06"], clear_until=c1)
    s["S07"] = F.over_v(B(("scale_empty", 6), ("cell_slot", 6), ("ai_court_corridor", 5), "scale_empty"),
                        captions_only(ctx, "S07"), dim=1, blur=0)
    s["V01"] = endcard
    return s


def music(ctx):
    return [("S01", "V01", S.cue_open, 2)]


def sfx(ctx):
    at = ctx.at
    return [("S01", 0.0, S.hum(ctx.dur["S01"], vol=0.025), -18), ("S04", 3.0, S.card_drop(), -10),
            ("S05", at("S05", "went into Rikers"), S.hit(0.5), -10),
            ("S06", at("S06", "In mid-2024"), S.hit(0.4), -12), ("V01", 0.1, S.hit(0.7), -6)]


if __name__ == "__main__":
    E.main(sys.modules[__name__])
