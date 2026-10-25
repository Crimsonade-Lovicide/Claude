"""Case 07 cold open, rebuilt in the hybrid look (prototype for every case).

    python ep07v2.py <prod_dir> --only S01,...,S09

Same narration, timing and cues as ep07.py. The picture changes every few seconds: our Blender
clips carry most of it (the dome, the desk with the act's real text, the corridor, the courtroom,
the Scale, the archive), and Higgsfield clips (anim/ai_*.mp4) fill in only the real-world places
Blender can't do well (the House chamber, a Florida street, the vigil, the TV trucks). Cards, rows
and numbers sit over darkened footage. Each clip carries its own honesty tag (footage.py).
Care rules unchanged: places and objects only, never her or anyone involved.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import edit as E  # noqa: E402
import ep02 as E2  # noqa: E402
import ep07  # noqa: E402
import footage as F  # noqa: E402
import gfx as G  # noqa: E402
from ep07 import (CHAPTERS, FADE_IN, FADE_OUT, LEAD, NEXT_AT, NEXT_NAME, NEXT_Q, PAD, SILENT,  # noqa: E402,F401
                  music, sfx)

OUT_NAME = "weight_of_evidence_case07_v2.mp4"
TITLE = ep07.TITLE

ACT = "RECONSTRUCTION · TEXT FROM PUB. L. 109-3"
TAGS = {"desk_act_push": ACT, "desk_act_stack": ACT,
        "desk_directive": "ILLUSTRATIVE · GENERIC FORM", "desk_blank_pen": "ILLUSTRATIVE",
        "corridor": "ILLUSTRATIVE", "evidence_shelf": "ILLUSTRATIVE"}


def build(ctx):
    P = ctx.prod
    at = ctx.at
    shots = ep07.build(ctx)
    old = dict(shots)

    def B(*items, **kw):
        return F.broll(P, list(items), tags=TAGS, **kw)

    def Bq(*items):  # footage for under a graphic: over() stamps the tag
        return B(*items, stamp=False)

    lower = E2.lower

    # S01  the vote and the signature
    t2 = at("S01", "Within the hour")
    shots["S01"] = B(("dome_push", 5.2), ("ai_house_chamber", t2 - 5.2), "ai_pen_sign",
                     overlay=lower("Washington", "MARCH 21, 2005 · 12:45 A.M.", 2.4))
    # S02  the act itself, real text, under its quote card
    shots["S02"] = F.over(Bq("desk_act_push"), old["S02"], clear_until=1.2)
    # S03  Florida, then the night it happened; the "26" card arrives on "when she was"
    t_card, t_par = at("S03", "when she was"), at("S03", "Paramedics")
    shots["S03"] = F.over(Bq(("ai_fl_street", t_card), ("ai_lights", t_par - t_card), "corridor"),
                          old["S03"], clear_until=t_card)
    # S04  nothing in writing; then the three positions over a ring, a dawn, the court
    t_h, t_p, t_j = at("S04", "Her husband"), at("S04", "Her parents"), at("S04", "A judge")
    shots["S04"] = F.over(Bq(("desk_blank_pen", t_h), ("ai_ring", t_p - t_h), ("ai_sunrise", t_j - t_p),
                             "courtroom_bench"), old["S04"], clear_until=t_h)
    # S05  the last thirteen days
    shots["S05"] = F.over(Bq(("ai_vigil", 4.6), "ai_tv_trucks"), old["S05"])
    # S06  the blank form; the figure lands on "only about"
    shots["S06"] = F.over(Bq("desk_directive"), old["S06"], clear_until=at("S06", "only about"))
    # S07  the question on the Scale, then one picture per answer
    t_hw, t_ju = at("S07", "Their husband"), at("S07", "A judge")
    t_po, t_ow = at("S07", "Politicians"), at("S07", "And what should")
    shots["S07"] = G.seq((old["S07"], t_hw),
                         (B(("ai_two_chairs", t_ju - t_hw), ("courtroom_push", t_po - t_ju, 4.0),
                            ("ai_dome", t_ow - t_po), ("desk_directive", None, 4.0)), 1))
    # S08  the record we read, then the promise
    t_l, t_w = at("S08", "the laws Florida"), at("S08", "At the end")
    shots["S08"] = G.seq((B(("evidence_shelf", t_l), "desk_act_stack"), t_w), (old["S08"], 1))
    return shots


if __name__ == "__main__":
    E.main(sys.modules[__name__])
