"""Case 07 rebuilt in the hybrid look: the whole episode.

    python ep07v2.py <prod_dir> --only S01,...   |   --final -j 2

Same narration, timing, cards and cues as ep07.py. Under the cards the picture now changes every
few seconds: our Blender clips carry most of it (the courtroom, the care-home room, the desk with
the record's own words, the corridor, the TV that shows only static, the Scale), and Higgsfield clips
(anim/ai_*.mp4) fill in only real places Blender can't do well. Act cards, verdict cards, the
title, the next-case card and the end card stay on black. Each clip carries its own honesty tag.
Care rules unchanged: places and objects only, never her or anyone involved.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import edit as E  # noqa: E402
import ep01 as E1  # noqa: E402
import ep02 as E2  # noqa: E402
import ep07  # noqa: E402
import footage as F  # noqa: E402
import gfx as G  # noqa: E402
from ep07 import (CHAPTERS, FADE_IN, FADE_OUT, LEAD, NEXT_AT, NEXT_NAME, NEXT_Q, PAD, SILENT,  # noqa: E402,F401
                  music, sfx)

OUT_NAME = "weight_of_evidence_case07.mp4"
TITLE = ep07.TITLE

ILL = "ILLUSTRATIVE"
TXT = "RECONSTRUCTION · TEXT FROM "
TAGS = {"desk_act_push": TXT + "PUB. L. 109-3", "desk_act_stack": TXT + "PUB. L. 109-3",
        "desk_directive": "ILLUSTRATIVE · GENERIC FORM", "desk_blank_pen": ILL,
        "desk_petition": "RECONSTRUCTION · TITLE FROM THE 1998 PETITION",
        "desk_greer": TXT + "JUDGE GREER'S ORDER", "desk_dca2003": TXT + "THE 2003 APPEAL RULING",
        "desk_wolfson": TXT + "THE GUARDIAN'S REPORT", "desk_pariente": TXT + "BUSH v. SCHIAVO",
        "desk_birch": TXT + "THE ELEVENTH CIRCUIT", "desk_examiner": TXT + "THE AUTOPSY REPORT",
        "desk_cruzan": TXT + "CRUZAN, 1990", "desk_mca": TXT + "THE MENTAL CAPACITY ACT",
        "brain_clean": "ILLUSTRATION · NOT HER BRAIN"}
for _c in ("court_push", "court_bench", "court_witness", "court_gallery", "dome_push", "tower_push",
           "ward_push", "ward_window", "tv_static", "corridor", "corridor_b", "or_lamp", "park_path",
           "book_closed", "book_night", "evidence_shelf"):
    TAGS[_c] = ILL


def build(ctx):
    P = ctx.prod
    at = ctx.at
    shots = ep07.build(ctx)
    old = dict(shots)

    def B(*items, **kw):
        return F.broll(P, list(items), tags=TAGS, **kw)

    def Bq(*items):  # footage for under a graphic: over() stamps the tag
        return B(*items, stamp=False)

    def under(sid, *items, clear=0.0):
        """The shot's own graphic over footage; the footage plays clean until `clear`."""
        return F.over(Bq(*items), old[sid], clear_until=clear)

    def card_after(sid, d, *items):
        """A card shot whose card lands d seconds in, over footage that plays clean until then."""
        return F.over(Bq(*items), F.delay(old[sid], d), clear_until=d)

    lower = E2.lower
    weight = E1.scale_overlay

    # ------------------------------------------------------------ COLD OPEN
    t2 = at("S01", "Within the hour")
    shots["S01"] = B(("dome_push", 5.2), ("ai_house_chamber", t2 - 5.2), "ai_pen_sign",
                     overlay=lower("Washington", "MARCH 21, 2005 · 12:45 A.M.", 2.4))
    shots["S02"] = under("S02", "desk_act_push", clear=1.2)
    t_card, t_par = at("S03", "when she was"), at("S03", "Paramedics")
    shots["S03"] = under("S03", ("ai_fl_street", t_card), ("ai_lights", t_par - t_card), "corridor", clear=t_card)
    t_h, t_p, t_j = at("S04", "Her husband"), at("S04", "Her parents"), at("S04", "A judge")
    shots["S04"] = under("S04", ("desk_blank_pen", t_h), ("ai_ring", t_p - t_h), ("ai_sunrise", t_j - t_p),
                         "court_bench", clear=t_h)
    shots["S05"] = under("S05", ("ai_vigil", 4.6), "ai_tv_trucks")
    shots["S06"] = under("S06", "desk_directive", clear=at("S06", "only about"))
    t_hw, t_ju = at("S07", "Their husband"), at("S07", "A judge")
    t_po, t_ow = at("S07", "Politicians"), at("S07", "And what should")
    shots["S07"] = G.seq((old["S07"], t_hw),
                         (B(("ai_two_chairs", t_ju - t_hw), ("court_push", t_po - t_ju, 4.0),
                            ("ai_dome", t_ow - t_po), ("desk_directive", None, 4.0)), 1))
    t_l, t_w = at("S08", "the laws Florida"), at("S08", "At the end")
    shots["S08"] = G.seq((B(("evidence_shelf", t_l), "desk_act_stack"), t_w), (old["S08"], 1))

    # ------------------------------------------------------------ I. THE COLLAPSE
    c1, c2, c3, c4 = (at("S11", p) for p in ("She married", "moved with him", "She worked", "Early on February"))
    shots["S11"] = under("S11", ("ai_philly", c2), ("ai_gulf_dawn", c3 - c2), ("ai_fl_street", c4 - c3, 1.0),
                         "ai_hallway", clear=c1)
    shots["S12"] = card_after("S12", 3.0, ("ward_push", 8), ("brain_clean", 8), "ward_window")
    shots["S13"] = card_after("S13", 2.5, ("ai_rain_window", 5), "corridor_b")
    c1, c2 = at("S14", "took her to California"), at("S14", "It didn't help")
    shots["S14"] = card_after("S14", 3.0, ("ward_window", c1, 2.0), ("ai_plane", c2 - c1), "ai_sunrise")
    c1, c2 = at("S15", "That February"), at("S15", "view was that")
    shots["S15"] = under("S15", ("court_bench", c1), ("ai_two_chairs", c2 - c1), "court_gallery")
    c1, c2, c3 = at("S16", "on medical advice"), at("S16", "Her parents went"), at("S16", "They had also")
    shots["S16"] = under("S16", ("ai_nursing_ext", c1 + 3), ("ward_push", c2 - c1 - 3), ("court_push", c3 - c2, 2.0),
                         "park_path", clear=c1)
    shots["S17"] = card_after("S17", 3.0, "desk_petition")

    # ------------------------------------------------------------ II. THE TRIAL
    shots["S20"] = B(("ai_courthouse", 5), ("court_push", 8), ("court_witness", 8), "court_bench",
                     overlay=lower("Clearwater, Florida", "JANUARY 2000", 1.2))
    shots["S21"] = card_after("S21", 3.0, ("court_witness", 8, 3.0), "court_gallery")
    shots["S22"] = card_after("S22", 3.0, ("tv_static", 8), ("court_bench", None, 2.0))
    shots["S23"] = card_after("S23", 2.5, "desk_greer")
    shots["S24"] = card_after("S24", 3.0, ("court_bench", 8, 4.0), ("court_push", None, 4.0))
    c1, c2 = at("S25", "In April"), at("S25", "Two days later")
    shots["S25"] = under("S25", ("ward_window", c2), "ai_courthouse", clear=c1)
    c1 = at("S26", "two chosen")
    shots["S26"] = under("S26", ("corridor", c1 + 3), ("ward_push", 7), "corridor_b", clear=c1)
    d = at("S27", "The appeals judges") - 0.5
    shots["S27"] = card_after("S27", d, ("tv_static", d), ("ai_tv_trucks", 6), ("tv_static", None, 4.0))
    shots["S28"] = card_after("S28", 2.0, ("desk_dca2003", 9), ("court_push", None, 3.0))

    # ------------------------------------------------------------ III. THE POLITICIANS
    shots["S31"] = under("S31", ("ward_window", at("S31", "Six days later"), 2.0), "tower_push")
    shots["S32"] = card_after("S32", 3.5, ("evidence_shelf", 7), "desk_wolfson")
    shots["S33"] = card_after("S33", 3.0, ("ai_courthouse", 5, 1.0), "desk_pariente")
    c1, c2, c3 = at("S34", "Two days later"), at("S34", "The House followed"), at("S34", "The White House")
    shots["S34"] = under("S34", ("ward_push", c1, 3.0), ("ai_dome", c2 - c1, 1.0), ("ai_house_chamber", c3 - c2, 1.0),
                         "ai_pen_sign")
    shots["S35"] = under("S35", ("desk_act_push", None, 3.0))
    c1 = at("S36", "Another")
    shots["S36"] = card_after("S36", 2.5, ("ai_scotus", 6), ("desk_birch", c1 - 6), ("court_bench", None, 5.0))
    shots["S37"] = under("S37", ("ai_tv_trucks", None, 1.5))
    shots["S38"] = under("S38", ("ai_vigil", 5.5, 0.5), "ai_sunrise")
    c1, c2 = at("S39", "her brain weighed"), at("S39", "But the neuropathologist")
    shots["S39"] = under("S39", ("corridor_b", c1 + 3), ("or_lamp", c2 - c1 - 3), "desk_examiner", clear=c1)

    # ------------------------------------------------------------ IV. THE RULES
    c1 = at("S42", "Justice Scalia")
    shots["S42"] = card_after("S42", 3.0, ("ai_scotus", 6), ("book_closed", 8), ("desk_cruzan", c1 - 14),
                              ("dome_push", None, 3.0))
    c1, c2, c3 = at("S43", "chosen anyone"), at("S43", "then your spouse"), at("S43", "then your parents")
    shots["S43"] = under("S43", ("book_night", c2), ("ai_two_chairs", c3 - c2, 1.5), "ward_window", clear=c1)
    c1 = at("S44", "surrogates predicted")
    shots["S44"] = under("S44", ("ai_two_chairs", c1 + 2), "ward_push", clear=c1)
    shots["S45"] = card_after("S45", 4.0, ("ai_westminster", 6), ("desk_mca", 9), "ai_rain_window")
    c1 = at("S46", "disability rights")
    shots["S46"] = card_after("S46", 3.0, ("ai_stpeters", 7), ("ai_church_candles", c1 - 7), "ward_window")
    c1, c2 = at("S47", "In one London"), at("S47", "In her case")
    shots["S47"] = under("S47", ("corridor", c1 + 4), ("brain_clean", c2 - c1 - 4, 2.0), ("court_push", None, 5.0),
                         clear=c1)

    # ------------------------------------------------------------ V. THE VERDICT: the two strongest cases
    q = [at("S50", p) for p in ("A judge heard", "The appeals courts", "Five doctors", "and the autopsy",
                                 "To overrule")]
    shots["S50"] = B(("scale_tip_left", q[0]), ("court_witness", q[1] - q[0]), ("ai_courthouse", q[2] - q[1]),
                     ("corridor", q[3] - q[2]), ("desk_examiner", q[4] - q[3]), ("desk_blank_pen", 6),
                     ("scale_tip_left", None, 3.0),
                     overlay=weight("THE STRONGEST CASE: THE COURTS GOT IT RIGHT"))
    q = [at("S51", p) for p in ("recalled years later", "A guardian appointed", "Missouri would have",
                                 "Surrogates guess wrong", "and the diagnosis", "Her parents were willing",
                                 "When the evidence")]
    shots["S51"] = B(("scale_tip_right", q[0]), ("ai_ring", q[1] - q[0]), ("evidence_shelf", q[2] - q[1]),
                     ("ai_scotus", q[3] - q[2]), ("ai_two_chairs", q[4] - q[3]), ("corridor_b", q[5] - q[4]),
                     ("ward_window", q[6] - q[5]), ("ai_sunrise", 5), ("scale_tip_right", None, 3.0),
                     overlay=weight("THE STRONGEST CASE: WHEN IN DOUBT, CHOOSE LIFE"))
    return shots


if __name__ == "__main__":
    E.main(sys.modules[__name__])
