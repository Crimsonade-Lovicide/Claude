"""Case 07 cold open, rebuilt on generated footage (prototype for the new look).

    python ep07v2.py <prod_dir> --only S01,...,S09

Same narration, timing and cues as ep07.py; S01-S08 now cut generated B-roll under the
narration every few seconds, with the evidence graphics laid over moving footage instead of black.
Clips are in <prod>/anim/ai_*.mp4 (Higgsfield, Kling 3.0 Turbo), tagged ILLUSTRATIVE · AI-GENERATED.
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
from ep07 import (CHAPTERS, FADE_IN, FADE_OUT, LEAD, NEXT_AT, NEXT_NAME, NEXT_Q, PAD, SILENT,  # noqa: E402,F401
                  music, sfx)

OUT_NAME = "weight_of_evidence_case07_v2.mp4"
TITLE = ep07.TITLE


def build(ctx):
    P = ctx.prod
    at = ctx.at
    shots = ep07.build(ctx)
    old = dict(shots)
    B = lambda *items, **kw: F.broll(P, list(items), **kw)  # noqa: E731
    lower = E2.lower

    t2 = at("S01", "Within the hour")
    shots["S01"] = B(("ai_dome", 5.2), ("ai_house_chamber", t2 - 5.2), "ai_pen_sign",
                     overlay=lower("Washington", "MARCH 21, 2005 · 12:45 A.M.", 2.4))
    shots["S02"] = F.over(B("ai_bill_pages", tag=None), old["S02"])
    t_par = at("S03", "Paramedics")
    shots["S03"] = B(("ai_fl_street", at("S03", "her heart had") - 0.2), ("ai_hallway", t_par - at("S03", "her heart had") + 0.2),
                     "ai_lights")
    t_rows = at("S04", "Her husband")
    shots["S04"] = _seq((B(("ai_blank_page", t_rows)), t_rows),
                        (F.over(B(("ai_ring", 4.5), ("ai_sunrise", 4.5), "ai_courthouse", tag=None),
                                _shift(old["S04"], t_rows)), 1))
    shots["S05"] = F.over(B(("ai_vigil", 4.6), "ai_tv_trucks", tag=None), old["S05"])
    shots["S06"] = F.over(B("ai_form_hands", tag=None), old["S06"])
    t_ch = at("S07", "Their husband")
    shots["S07"] = _seq((old["S07"], t_ch), (B("ai_two_chairs"), 1))
    t_w = at("S08", "At the end")
    shots["S08"] = _seq((B(("ai_archive", t_w / 2), "ai_papers"), t_w), (old["S08"], 1))
    return shots


def _seq(*parts):
    import gfx as G
    return G.seq(*parts)


def _shift(fn, dt):
    """Run a graphic as if the shot had started dt seconds earlier (its cues stay on the words)."""
    def frame(t, dur):
        return fn(t + dt, dur + dt)
    return frame


if __name__ == "__main__":
    E.main(sys.modules[__name__])
