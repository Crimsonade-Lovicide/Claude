"""Weight of Evidence, Case 02: The Safety Driver. Shot definitions for edit.py.

    python ep02.py <prod_dir> --stills | --only S02,S13 | --final -j 2

Shot ids, picture notes and research IDs are in episodes/02-the-safety-driver/script.md.
The sensor diagram is rebuilt from the timeline in NTSB/HAR-19/03 (pp.15–16); positions are
schematic (straight-line approach at ~44 mph), labels and times are the report's.
"""

import math
import os
import sys

from PIL import ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import edit as E  # noqa: E402
import ep01 as E1  # noqa: E402  (shared helpers: stacked words, end card, overlays, span)
import gfx as G  # noqa: E402
import score as S  # noqa: E402

OUT_NAME = "weight_of_evidence_case02.mp4"
TITLE = "Weight of Evidence, Case 02: The Safety Driver"

SILENT = {"S09": 6.5, "S10": 3.4, "S20": 3.4, "S36": 3.4, "S47": 3.4, "S54": 3.4, "S62": 20.0}
LEAD = {"S01": 2.0, "S02": 0.6, "S05": 0.8, "S11": 0.4, "S21": 0.6, "S37": 0.4, "S48": 0.6,
        "S55": 0.6, "S61": 0.8}
PAD = {"S01": 0.8, "S03": 1.6, "S04": 1.0, "S05": 2.4, "S06": 1.2, "S07": 1.6, "S08": 1.2,
       "S15": 1.4, "S17": 1.6, "S18": 1.0, "S19": 1.4, "S23": 1.0, "S25": 1.0, "S28": 1.0,
       "S34": 1.2, "S35": 1.6, "S41": 1.0, "S45": 1.6, "S46": 1.8, "S49": 1.0, "S53": 1.6,
       "S57": 3.0, "S58": 3.0, "S59": 3.0, "S60": 2.0, "S61": 2.4}
FADE_IN = {"S01": 1.4, "S10": 0.6, "S20": 0.6, "S36": 0.6, "S47": 0.6, "S54": 0.6}
FADE_OUT = {"S05": 0.8, "S08": 0.4, "S09": 1.0, "S19": 1.0, "S35": 1.2, "S46": 1.2, "S53": 1.0,
            "S60": 1.5, "S62": 1.5}
CHAPTERS = [("S01", "9:58 p.m., Mill Avenue"), ("S10", "I. The machine"), ("S20", "II. The safety driver"),
            ("S36", "III. The company"), ("S47", "IV. No one at the wheel"), ("S54", "V. The verdict"),
            ("S61", "Next case")]

NTSB = "NTSB/HAR-19/03 (2019)"


# ---------------------------------------------------------------- the sensor diagram

CLS_COL = {"VEHICLE": G.CYAN, "OTHER": G.DIM, "BICYCLE": G.BRASS}
ROAD_X0, ROAD_X1 = 300, 820          # median edge .. curb
LANES = [(380, 560), (560, 740)]     # left and right northbound lanes; 740..820 bike lane
CAR_Y = 860                          # car's front bumper
PX_PER_FT = 1.95
MPH = 44.0


def her_xy(tti):
    """Schematic position of the crossing pedestrian at time-to-impact tti (s)."""
    d_ft = MPH * 5280 / 3600 * tti
    y = CAR_Y - d_ft * PX_PER_FT
    u = G.clamp(1 - tti / 5.6)
    x = 405 + (640 - 405) * u  # from near the median curb (left lane) to the car's lane
    return x, y


def path_arrow(d, x, y, kind, col):
    """Predicted path: 'lane' = along the lane (up), 'static' = a dot."""
    if kind == "lane":
        d.line([x, y, x, y - 110], fill=col, width=4)
        d.polygon([(x - 12, y - 100), (x + 12, y - 100), (x, y - 126)], fill=col)
    elif kind == "static":
        d.ellipse([x - 7, y - 7, x + 7, y + 7], outline=col, width=3)


def sensor_shot(events, clock=None, log=None, overlay=None, upto=None):
    """events: [(t_shot, tti, cls, path)] — the box relabels at each t_shot.
    clock: [(t_shot, tti)] keyframes for the countdown (piecewise linear); defaults to events.
    log: [(t_shot, text)] lines added to the right-hand log. overlay(img, d, t, tti)."""
    keys = clock or [(e[0], e[1]) for e in events]

    def tti_at(t):
        if t <= keys[0][0]:
            return keys[0][1]
        for (t0, a), (t1, b) in zip(keys, keys[1:]):
            if t <= t1:
                return a + (b - a) * G.clamp((t - t0) / max(1e-3, t1 - t0))
        return keys[-1][1]

    def frame(t, dur):
        img = G.canvas()
        a = G.fade(t, dur, 0.4, 0.5)
        d = ImageDraw.Draw(img)
        dim = lambda c, k=1.0: tuple(int(v * a * k) for v in c)
        # road
        d.rectangle([ROAD_X0 - 90, 60, ROAD_X0, 1020], fill=dim((22, 24, 22)))
        G.paste_alpha(img, G.text_layer("MEDIAN", G.MONO(20), fill=G.FAINT, spacing=0.3), (ROAD_X0 - 84, 70), a)
        d.rectangle([ROAD_X0, 60, ROAD_X1, 1020], fill=dim((18, 19, 22)))
        d.line([LANES[0][0], 60, LANES[0][0], 1020], fill=dim(G.BRASS, 0.7), width=3)
        for y in range(60, 1020, 46):
            d.line([LANES[1][0], y, LANES[1][0], y + 22], fill=dim(G.DIM, 0.8), width=3)
        d.line([LANES[1][1], 60, LANES[1][1], 1020], fill=dim(G.DIM, 0.8), width=2)
        d.line([ROAD_X1, 60, ROAD_X1, 1020], fill=dim(G.DIM), width=3)
        tti = tti_at(t)
        # her actual path (dotted, across the lanes)
        x0, y0 = her_xy(5.6)
        x1, y1 = her_xy(0.0)
        for k in range(0, 40, 2):
            u0, u1 = k / 40, (k + 1) / 40
            d.line([x0 + (x1 - x0) * u0, y0 + (y1 - y0) * u0, x0 + (x1 - x0) * u1, y0 + (y1 - y0) * u1],
                   fill=dim(G.FAINT), width=2)
        # the car (fixed; the world moves toward it)
        cx = (LANES[1][0] + LANES[1][1]) // 2
        d.rounded_rectangle([cx - 58, CAR_Y, cx + 58, CAR_Y + 150], radius=14, fill=dim((60, 62, 68)), outline=dim(G.INK, 0.6), width=2)
        d.ellipse([cx - 14, CAR_Y + 50, cx + 14, CAR_Y + 78], outline=dim(G.CYAN), width=2)  # roof lidar
        G.paste_alpha(img, G.text_layer(f"{MPH:.0f} MPH" if tti > 1.3 else "39 MPH", G.MONO(22, True), fill=G.DIM), (cx - 44, CAR_Y + 160), a)
        # detection box with its current label
        cur = None
        for e in events:
            if t >= e[0]:
                cur = e
        if cur is not None:
            hx, hy = her_xy(tti)
            col = CLS_COL[cur[2]]
            kb = G.ease((t - cur[0]) / 0.25)
            s = 34
            d.rectangle([hx - s, hy - s, hx + s, hy + s], outline=dim(col), width=4)
            for cxs in (-1, 1):  # corner ticks
                d.line([hx + cxs * (s + 10), hy - s, hx + cxs * (s + 10), hy + s], fill=dim(col, 0.4), width=1)
            path_arrow(d, hx, hy - s - 6, cur[3], dim(col))
            lab = G.text_layer(cur[2], G.MONO(26, True), fill=col, spacing=0.12)
            G.paste_alpha(img, lab, (int(hx + s + 14), int(hy - s)), a * kb)
        # right panel: countdown and log
        G.paste_alpha(img, G.text_layer("TIME TO IMPACT", G.MONO(24), fill=G.DIM, spacing=0.3), (1040, 120), a)
        clk = G.text_layer(f"−{tti:0.1f} s", G.SANS(120, "SemiBold"), fill=G.INK)
        G.paste_alpha(img, clk, (1032, 158), a)
        if log:
            y = 360
            for ts, text in log:
                if t < ts:
                    continue
                k = G.ease((t - ts) / 0.35) * a
                col = G.INK
                for name, c in CLS_COL.items():
                    if name in text:
                        col = c
                G.paste_alpha(img, G.text_layer(text, G.MONO(30), fill=col), (1040, y), k)
                y += 52
        if overlay:
            overlay(img, d, t, tti, a)
        G.paste_alpha(img, G.text_layer("Positions schematic · labels and times from " + NTSB, G.MONO(20), fill=G.FAINT), (1040, 990), a)
        G.recon_tag(img, a, "RECONSTRUCTION FROM NTSB DATA")
        return G.finish(img, t)
    return frame


def suppression_overlay(t_start, t_end, alert_at=None):
    def ov(img, d, t, tti, a):
        k = G.clamp((t - t_start) / max(0.1, t_end - t_start))
        if t < t_start - 0.2:
            return
        y = 760
        G.paste_alpha(img, G.text_layer("ACTION SUPPRESSION · BRAKING HELD", G.MONO(28, True), fill=G.RED, spacing=0.1), (1040, y - 54), a)
        d.rectangle([1040, y, 1780, y + 26], outline=tuple(int(c * a) for c in G.RED), width=2)
        if k > 0:
            d.rectangle([1044, y + 4, 1044 + int(732 * k), y + 22], fill=tuple(int(c * a) for c in G.RED))
        G.paste_alpha(img, G.text_layer("1.0 s", G.MONO(24), fill=G.DIM), (1700, y + 36), a)
        lit = alert_at is not None and t >= alert_at
        txt = "OPERATOR ALERT: ON" if lit else "OPERATOR ALERT: NONE"
        G.paste_alpha(img, G.text_layer(txt, G.MONO(28, True), fill=G.BRASS if lit else G.DIM, spacing=0.1), (1040, y + 90), a)
    return ov


# ---------------------------------------------------------------- other graphics

def gaze_shot(ctx, sid):
    t_long = ctx.at(sid, "Her longest look")
    t_last = ctx.at(sid, "In the final three minutes")

    def frame(t, dur):
        img = G.canvas()
        a = G.fade(t, dur, 0.4, 0.5)
        d = ImageDraw.Draw(img)
        G.paste_alpha(img, G.text_layer("31.5 MINUTES OF DRIVING", G.MONO(26), fill=G.DIM, spacing=0.3), (220, 230), a)
        x0, x1, y = 220, 1700, 290
        d.rectangle([x0, y, x1, y + 90], outline=tuple(int(c * a) for c in G.FAINT), width=2)
        k = G.ease((t - 0.8) / 1.6)
        xf = x0 + (x1 - x0) * 0.34 * k
        if xf > x0 + 4:
            d.rectangle([x0 + 4, y + 4, xf, y + 86], fill=tuple(int(c * a) for c in G.BRASS))
        G.paste_alpha(img, G.text_layer(f"{round(34 * k)}%", G.SANS(64, "SemiBold"), fill=G.INK), (int(xf) + 24, y + 6), a)
        G.paste_alpha(img, G.text_layer("LOOKING DOWN TOWARD THE CENTER CONSOLE, WHERE HER PHONE WAS", G.MONO(24), fill=G.BRASS, spacing=0.1), (x0, y + 110), a * k)
        for i, (num, lab, ts) in enumerate([("26.5 s", "longest single look down", t_long),
                                            ("23", "looks down in the final three minutes", t_last)]):
            kk = G.ease((t - ts) / 0.6) * a
            G.paste_alpha(img, G.text_layer(num, G.SANS(110, "SemiBold"), fill=G.INK), (220 + i * 780, 560), kk)
            G.paste_alpha(img, G.text_layer(lab, G.SANS(34), fill=G.DIM), (226 + i * 780, 710), kk)
        G.paste_alpha(img, G.text_layer(NTSB + " · inward-facing camera", G.MONO(22), fill=G.FAINT), (220, G.H - 140), a)
        st = G.stamp("RECORD", 20)
        G.paste_alpha(img, st, (G.W - 220 - st.width, 160), a)
        return G.finish(img, t)
    return frame


def clock_shot(ctx, sid):
    """Mackworth's clock test, illustrated: the hand steps; now and then it jumps twice; a
    tally of caught and missed double jumps grows, with more misses as the watch goes on."""
    import random
    rng = random.Random(1948)
    steps = []  # (time, double, caught)
    t, n = 0.6, 0
    while t < 60:
        double = n % 7 == 5
        minute = 30 * G.clamp(t / 18)
        caught = rng.random() > (0.08 + 0.42 * (minute / 30)) if double else True
        steps.append((t, double, caught))
        t += 0.42
        n += 1

    def frame(tt, dur):
        img = G.canvas()
        a = G.fade(tt, dur, 0.4, 0.5)
        d = ImageDraw.Draw(img)
        cx, cy, r = 620, 540, 300
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=tuple(int(c * a) for c in G.INK), width=4)
        for k in range(100):
            ang = 2 * math.pi * k / 100
            r0 = r - (22 if k % 10 == 0 else 10)
            d.line([cx + r0 * math.sin(ang), cy - r0 * math.cos(ang), cx + (r - 4) * math.sin(ang), cy - (r - 4) * math.cos(ang)],
                   fill=tuple(int(c * a) for c in G.DIM), width=2)
        pos, flash, tally = 0, None, []
        for ts, double, caught in steps:
            if ts > tt:
                break
            pos += 2 if double else 1
            if double:
                tally.append(caught)
                if tt - ts < 0.35:
                    flash = caught
        ang = 2 * math.pi * pos / 100
        d.line([cx, cy, cx + (r - 40) * math.sin(ang), cy - (r - 40) * math.cos(ang)],
               fill=tuple(int(c * a) for c in (G.BRASS if flash is not None else G.INK)), width=6)
        d.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], fill=tuple(int(c * a) for c in G.INK))
        minute = 30 * G.clamp(tt / 18)
        G.paste_alpha(img, G.text_layer("MINUTES ON WATCH", G.MONO(24), fill=G.DIM, spacing=0.3), (1080, 220), a)
        G.paste_alpha(img, G.text_layer(f"{int(minute):02d}", G.SANS(120, "SemiBold"), fill=G.INK), (1074, 256), a)
        G.paste_alpha(img, G.text_layer("DOUBLE JUMPS", G.MONO(24), fill=G.DIM, spacing=0.3), (1080, 470), a)
        for i, c in enumerate(tally[-40:]):
            x, y = 1080 + (i % 10) * 64, 520 + (i // 10) * 64
            col = G.CYAN if c else G.RED
            if c:
                d.ellipse([x, y, x + 40, y + 40], outline=tuple(int(v * a) for v in col), width=4)
            else:
                d.line([x + 4, y + 4, x + 36, y + 36], fill=tuple(int(v * a) for v in col), width=5)
                d.line([x + 36, y + 4, x + 4, y + 36], fill=tuple(int(v * a) for v in col), width=5)
        G.paste_alpha(img, G.text_layer("Mackworth, 1948 · after Q J Exp Psychol 1:6–21", G.MONO(22), fill=G.FAINT), (1080, G.H - 140), a)
        G.recon_tag(img, a, "ILLUSTRATION · NOT DATA")
        return G.finish(img, tt)
    return frame


def rows_shot(rows, times, header=None, label=None, source=None, strike=False):
    """Dated rows (or plain lines) that land one by one: rows = [(left, right)]."""
    def frame(t, dur):
        img = G.canvas()
        a = G.fade(t, dur, 0.4, 0.5)
        if header:
            G.paste_alpha(img, G.text_layer(header, G.MONO(26, True), fill=G.DIM, spacing=0.35), (220, 200), a)
        y0 = 300 if header else 260
        gap = min(130, 560 // max(1, len(rows)))
        for i, ((left, right), ts) in enumerate(zip(rows, times)):
            k = G.ease((t - ts) / 0.5) * a
            if k <= 0:
                continue
            y = y0 + i * gap
            if left:
                G.paste_alpha(img, G.text_layer(left, G.MONO(32, True), fill=G.BRASS, spacing=0.1), (220, y + 8), k)
            lay = G.text_layer(right, G.SANS(48, "SemiBold"), fill=G.INK, spacing=0.04)
            x = 640 if left else 220
            G.paste_alpha(img, lay, (x, y), k)
            if strike:
                d = ImageDraw.Draw(img)
                w = lay.width * G.ease((t - ts - 0.3) / 0.4)
                d.line([x, y + lay.height // 2 + 4, x + w, y + lay.height // 2 + 4], fill=tuple(int(c * k) for c in G.RED), width=4)
        if source:
            G.paste_alpha(img, G.text_layer(source, G.MONO(22), fill=G.FAINT), (220, G.H - 140), a)
        if label:
            st = G.stamp(label, 20)
            G.paste_alpha(img, st, (G.W - 220 - st.width, 160), a)
        return G.finish(img, t)
    return frame


def stat_count_shot(ctx, sid):
    t0 = ctx.at(sid, "more than four hundred thousand")

    def frame(t, dur):
        img = G.canvas()
        a = G.fade(t, dur, 0.4, 0.5)
        k = G.ease((t - t0 + 0.6) / 1.8)
        n = int(400000 * k / 1000) * 1000
        num = G.text_layer(f"{n:,}+", G.SANS(170, "SemiBold"), fill=G.BRASS)
        G.centered(img, num, 430, a)
        G.centered(img, G.text_layer("RIDES A WEEK · NO ONE IN THE DRIVER'S SEAT", G.MONO(34, True), fill=G.INK, spacing=0.2), 610, a * G.ease((t - t0) / 0.8))
        G.centered(img, G.text_layer("Waymo, February 2026 (company figure)", G.MONO(24), fill=G.FAINT), G.H - 150, a)
        st = G.stamp("RECORD", 20)
        G.paste_alpha(img, st, (G.W - 220 - st.width, 160), a)
        return G.finish(img, t)
    return frame


def two_col_shot(ctx, sid):
    t1 = ctx.at(sid, "In California")
    t2 = ctx.at(sid, "The company has faced")
    cols = [("THE DRIVER", G.CYAN, t1, ["Tesla on Autopilot, 2019 · two killed",
                                        "Driver pleads no contest to",
                                        "vehicular manslaughter · probation"]),
            ("THE COMPANY", G.BRASS, t2, ["Benavides v. Tesla · Miami · 2025",
                                          "Jury: Autopilot defective, Tesla 33% at fault",
                                          "About $243 million · on appeal"])]

    def frame(t, dur):
        img = G.canvas()
        a = G.fade(t, dur, 0.4, 0.5)
        d = ImageDraw.Draw(img)
        for i, (head, col, ts, lines) in enumerate(cols):
            k = G.ease((t - ts) / 0.6) * a
            x = 200 + i * 800
            d.line([x, 300, x, 760], fill=tuple(int(c * k) for c in col), width=4)
            G.paste_alpha(img, G.text_layer(head, G.MONO(30, True), fill=col, spacing=0.25), (x + 40, 300), k)
            for j, ln in enumerate(lines):
                G.paste_alpha(img, G.text_layer(ln, G.SERIF(40), fill=G.INK), (x + 40, 400 + j * 70), k)
            G.paste_alpha(img, G.text_layer("CRIMINAL" if i == 0 else "CIVIL", G.MONO(24), fill=G.DIM, spacing=0.3), (x + 40, 640), k)
        G.paste_alpha(img, G.text_layer("AP 2023 (Riad) · S.D. Fla. No. 21-cv-21940, judgment Aug 2025", G.MONO(22), fill=G.FAINT), (200, G.H - 140), a)
        return G.finish(img, t)
    return frame


def big_words(text, size=84, colour=G.INK, sub=None, sub_at=1.2):
    def frame(t, dur):
        img = G.canvas()
        a = G.fade(t, dur, 0.5, 0.6)
        G.centered(img, G.text_layer(text, G.SANS(size, "SemiBold"), fill=colour, spacing=0.06), G.H // 2 - (40 if sub else 0), a * G.ease(t / 0.8))
        if sub:
            G.centered(img, G.text_layer(sub, G.SERIF_I(44), fill=G.DIM), G.H // 2 + 70, a * G.ease((t - sub_at) / 0.8))
        return G.finish(img, t)
    return frame


def lower(text, sub=None, at=1.2):
    return lambda img, t, d: G.lower_third(img, text, sub, G.ramp(t, at, 0.8) * G.fade(t, d, 0.01, 0.6))


# ---------------------------------------------------------------- the shots

def build(ctx):
    P = ctx.prod
    C = lambda name, **kw: E.Clip(P, name, **kw)
    at = ctx.at
    doc = G.document_shot
    span = E1.span
    shots = {}

    # COLD OPEN
    shots["S01"] = E.clip_shot(C("road_push"), overlay=lower("Tempe, Arizona", "MARCH 18, 2018 · 9:58 P.M.", 2.4))
    s02 = [(at("S02", "decided it was a vehicle"), 5.6, "VEHICLE", "none"),
           (at("S02", "something else"), 5.2, "OTHER", "static"),
           (at("S02", "a vehicle again"), 4.2, "VEHICLE", "static"),
           (at("S02", "Then a bicycle"), 2.6, "BICYCLE", "static")]
    shots["S02"] = sensor_shot(s02, clock=[(0.0, 5.6)] + [(e[0], e[1]) for e in s02])
    shots["S03"] = big_words("Elaine Herzberg, 49", 84, sub="walking a bicycle across the road", sub_at=at("S03", "walking"))
    shots["S04"] = E.clip_shot(C("road_push", start=7, speed=0.8))
    shots["S05"] = big_words("39 mph", 110, colour=G.DIM)
    shots["S06"] = rows_shot([("MARCH 2018", "Uber settles with her family"),
                              ("MARCH 2019", "No criminal charges for Uber"),
                              ("AUGUST 2020", "Safety driver charged with negligent homicide")],
                             [at("S06", "Ten days later"), at("S06", "A year later"), at("S06", "Two years after")],
                             source="Reuters/AP 2018 · Yavapai County Attorney 2019 · Maricopa County indictment 2020")
    shots["S07"] = E.clip_shot(C("scale_empty"), tag=None)
    shots["S08"] = G.words_shot("We'll give you a verdict, and tell you how sure we are.", size=64,
                                emphasis={"how", "sure"}, per_word=0.3, start=at("S08", "At the end"))
    shots["S09"] = G.title_shot("THE SAFETY DRIVER", "When the machine kills, who's guilty?", "WEIGHT OF EVIDENCE · CASE 02")

    # I. THE MACHINE
    shots["S10"] = G.title_shot("I · THE MACHINE")
    shots["S11"] = E.clip_shot(C("car_orbit"), tag="GENERIC VEHICLE · SIMPLIFIED")
    shots["S12"] = doc(["NATIONAL TRANSPORTATION SAFETY BOARD", "HIGHWAY ACCIDENT REPORT", "",
                        "Collision Between Vehicle Controlled by",
                        "Developmental Automated Driving System",
                        "and Pedestrian", "Tempe, Arizona · March 18, 2018", "", "NTSB/HAR-19/03 · adopted November 19, 2019"],
                       font_fn=G.SERIF, size=44, footer="Title page recreated")
    s13 = [(at("S13", "called her a vehicle"), 5.6, "VEHICLE", "none"),
           (at("S13", "Then, other"), 5.2, "OTHER", "static"),
           (at("S13", "Then vehicle"), 4.2, "VEHICLE", "lane"),
           (at("S13", "other, vehicle again"), 3.4, "OTHER", "static"),
           (at("S13", "vehicle again"), 2.9, "VEHICLE", "lane"),
           (at("S13", "a bicycle"), 2.6, "BICYCLE", "static"),
           (at("S13", "At 1 5 other"), 1.5, "OTHER", "static"),
           (at("S13", "At 1 2 a bicycle"), 1.2, "BICYCLE", "lane")]
    log13 = [(s13[0][0], "−5.6  VEHICLE   radar"), (s13[1][0], "−5.2  OTHER     lidar"),
             (s13[2][0], "−4.2  VEHICLE"), (s13[3][0], "−3.8…−2.7  VEHICLE ↔ OTHER"),
             (s13[5][0], "−2.6  BICYCLE"), (s13[6][0], "−1.5  OTHER"), (s13[7][0], "−1.2  BICYCLE, in lane")]
    shots["S13"] = sensor_shot(s13, clock=[(0.0, 5.6)] + [(e[0], e[1]) for e in s13], log=log13)
    why = ["NTSB/HAR-19/03 · SYSTEM DESIGN", "",
           "If the perception process changed the classification of a",
           "detected object, it no longer considered the tracking history",
           "of that object when generating a new trajectory.", "",
           "Certain object classifications (“other”) were not assigned goals.", "",
           "Pedestrians outside the vicinity of a crosswalk were also not",
           "assigned an explicit goal."]
    t_goal = at("S14", "And it gave no predicted goal")
    shots["S14"] = G.seq((doc(why, size=34, width=1500, font_fn=G.SERIF, highlight=span(why, "it no longer considered the tracking history"),
                              hi_at=at("S14", "threw away"), footer="Excerpt · recreated"), t_goal),
                         (doc(why, size=34, width=1500, font_fn=G.SERIF, highlight=span(why, "Pedestrians outside the vicinity of a crosswalk were also not"),
                              hi_at=at("S14", "pedestrians away", offset=-t_goal), footer="Excerpt · recreated", drift=0.0), 1))
    shots["S15"] = E1.stacked_words_shot([("It saw her for 5.6 seconds.", G.SANS(64, "SemiBold"), G.INK),
                                          ("It never understood what it was seeing.", G.SERIF_I(56), G.BRASS)],
                                         [0.4, at("S15", "It never understood")])
    t_sup0, t_sup1 = at("S16", "For one full second"), at("S16", "It didn't warn the driver")
    shots["S16"] = sensor_shot([(0.0, 1.2, "BICYCLE", "lane")],
                               clock=[(0.0, 1.2), (t_sup0, 1.2), (t_sup1, 0.2)],
                               log=[(0.2, "−1.2  EMERGENCY DECLARED")],
                               overlay=suppression_overlay(t_sup0, t_sup1))
    shots["S17"] = sensor_shot([(0.0, 0.2, "BICYCLE", "lane")], clock=[(0.0, 0.2)],
                               log=[(0.0, "−1.2  EMERGENCY DECLARED"), (0.3, "−0.2  ALERT · SLOW GENTLY")],
                               overlay=suppression_overlay(-2, -1, alert_at=0.3))
    shots["S18"] = G.card_shot("In Volvo's simulations, its own emergency braking avoided the collision in 17 of 20 variations.",
                               "RECORD", "NTSB/HAR-19/03 · Volvo simulation; Uber deactivated it in autonomous mode")
    shots["S19"] = E.clip_shot(C("scale_tip_left"), tag=None, overlay=E1.scale_overlay("EVIDENCE · THE SYSTEM SAW HER AND DID NOT UNDERSTAND"))

    # II. THE SAFETY DRIVER
    shots["S20"] = G.title_shot("II · THE SAFETY DRIVER")
    shots["S21"] = E.clip_shot(C("road_top"), overlay=E1.caption_overlay("ROUTE DRIVEN 73 TIMES IN AUTONOMOUS MODE", 1.0))
    shots["S22"] = G.card_shot("“During September–October 2017, ATG consolidated the responsibilities of two vehicle operators into that of a single operator.”",
                               "RECORD", NTSB)
    shots["S23"] = gaze_shot(ctx, "S23")
    shots["S24"] = G.card_shot("“…the account belonging to the vehicle operator was continually streaming a television show between 9:16 p.m. and 9:59 p.m.”",
                               "RECORD", NTSB + " · police: The Voice, on Hulu")
    attentive = ["NTSB/HAR-19/03 · ANALYSIS", "",
                 "…had the vehicle operator been attentive,",
                 "she would likely have had sufficient time to detect and react",
                 "to the crossing pedestrian to avoid the crash or mitigate the impact."]
    shots["S25"] = doc(attentive, size=38, width=1550, font_fn=G.SERIF, highlight=span(attentive, "she would likely have had sufficient time to detect and react"),
                       hi_at=at("S25", "two to four seconds"), footer="Excerpt · recreated")
    shots["S26"] = rows_shot([("AUG 27, 2020", "Indicted · negligent homicide"),
                              ("JULY 28, 2023", "Pleads guilty · endangerment"),
                              ("", "Three years supervised probation")],
                             [at("S26", "In 2020"), at("S26", "In 2023"), at("S26", "three years")],
                             label="RECORD", source="Maricopa County Attorney: indictment (2020), plea agreement (2023)")
    shots["S27"] = G.card_shot("“Regardless of whatever technology might be available to drivers, safety for everyone on the street and in the vehicle must always be a driver's first priority.”",
                               "RECORD", "Rachel Mitchell, Maricopa County Attorney, July 2023")
    shots["S28"] = G.card_shot("“We punish a man for his very ignorance, if he is thought responsible for the ignorance.”",
                               "ARGUMENT", "Aristotle, Nicomachean Ethics, Book III (trans. Ross)")
    shots["S29"] = clock_shot(ctx, "S29")
    shots["S30"] = G.card_shot("“Vigilance requires hard mental work and is stressful.”", "RECORD",
                               "Warm, Parasuraman & Matthews, Human Factors, 2008")
    shots["S31"] = G.card_shot("“…it is impossible for even a highly motivated human being to maintain effective visual attention towards a source of information on which very little happens, for more than about half an hour.”",
                               "RECORD", "Lisanne Bainbridge, “Ironies of Automation,” Automatica, 1983")
    poor = ["NTSB/HAR-19/03 · ANALYSIS", "",
            "When it comes to the human capacity to monitor an",
            "automation system for its failures, research findings",
            "are consistent—humans are very poor at this task."]
    shots["S32"] = doc(poor, size=40, width=1450, font_fn=G.SERIF, highlight=span(poor, "humans are very poor at this task."),
                       hi_at=at("S32", "humans are very poor"), footer="Excerpt · recreated")
    shots["S33"] = E.clip_shot(C("road_push", speed=0.6), overlay=E1.caption_overlay("GOOGLE · 2013 TESTS", 0.8))
    shots["S34"] = G.card_shot("“…the moral crumple zone protects the integrity of the technological system, at the expense of the nearest human operator.”",
                               "ARGUMENT", "Madeleine Clare Elish, Engaging Science, Technology, and Society, 2019")
    shots["S35"] = E.clip_shot(C("scale_swing"), tag=None, overlay=E1.scale_overlay("EVIDENCE · A REAL CHOICE, IN A JOB BUILT TO FAIL"))

    # III. THE COMPANY
    shots["S36"] = G.title_shot("III · THE COMPANY")
    pc = ["NTSB/HAR-19/03 · PROBABLE CAUSE", "",
          "…the failure of the vehicle operator to monitor the driving",
          "environment and the operation of the automated driving system",
          "because she was visually distracted throughout the trip by her",
          "personal cell phone. Contributing to the crash were the Uber",
          "Advanced Technologies Group's (1) inadequate safety risk",
          "assessment procedures, (2) ineffective oversight of vehicle",
          "operators, and (3) lack of adequate mechanisms for addressing",
          "operators' automation complacency—all a consequence of its",
          "inadequate safety culture."]
    t_contrib = at("S37", "Contributing were")
    t_cult = at("S37", "All of it")
    shots["S37"] = G.seq((doc(pc, size=32, width=1500, font_fn=G.SERIF, highlight=span(pc, "the failure of the vehicle operator to monitor the driving"),
                              hi_at=at("S37", "The probable cause"), footer="Excerpt · recreated"), t_cult),
                         (doc(pc, size=32, width=1500, font_fn=G.SERIF, highlight=span(pc, "inadequate safety culture."),
                              hi_at=0.4, footer="Excerpt · recreated", drift=0.0), 1))
    del t_contrib
    t38 = at("S38", "no safety division")
    shots["S38"] = rows_shot([("", "NO SAFETY DIVISION"), ("", "NO DEDICATED SAFETY MANAGER"), ("", "NO FORMAL SAFETY PLAN"),
                              ("", "NO STANDARD OPERATING PROCEDURES")],
                             [t38, at("S38", "no dedicated"), at("S38", "no formal"), at("S38", "no standard")],
                             header="UBER ATG AT THE TIME OF THE CRASH", label="RECORD", source=NTSB)
    shots["S39"] = G.card_shot("“…had the means to retroactively monitor the behavior of vehicle operators and their adherence to operational procedures, it rarely did so.”",
                               "RECORD", NTSB + " · finding 13")
    shots["S40"] = G.card_shot("Uber's cars were struggling to drive 13 miles between human interventions.", "INFERENCE",
                               "The New York Times, March 2018 (as reported)")
    shots["S41"] = G.card_shot("“…no basis for criminal liability for the Uber corporation…”", "INFERENCE",
                               "Yavapai County Attorney Sheila Polk, March 2019 (letter as reported)")
    shots["S42"] = big_words("A company can be charged.", 72, sub="It almost never is.", sub_at=at("S42", "But homicide"))
    shots["S43"] = rows_shot([("1978", "Indiana charges Ford with reckless homicide (Pinto)"), ("1980", "Ford acquitted"),
                              ("2020", "PG&E pleads guilty to 84 counts of manslaughter")],
                             [at("S43", "In 1978"), at("S43", "Ford was acquitted"), at("S43", "And in 2020")],
                             label="INFERENCE", source="Christian Science Monitor 1980 · press reports 2020")
    shots["S44"] = G.card_shot("“…the business friendly and low regulatory environment…”", "RECORD",
                               "Arizona Executive Order 2018-04, March 1, 2018")
    shots["S45"] = E.clip_shot(C("road_median"))
    shots["S46"] = E.clip_shot(C("scale_tip_right"), tag=None, overlay=E1.scale_overlay("EVIDENCE · THE DECISIONS THAT SET IT UP"))

    # IV. NO ONE AT THE WHEEL
    shots["S47"] = G.title_shot("IV · NO ONE AT THE WHEEL")
    shots["S48"] = stat_count_shot(ctx, "S48")
    shots["S49"] = G.card_shot("“…attempted to pull over to the side of the road with the woman underneath it, dragging the woman over 20 feet.”",
                               "RECORD", "U.S. Attorney, N.D. California, November 2024 · Cruise: $500,000 fine")
    shots["S50"] = two_col_shot(ctx, "S50")
    az = ["ARIZONA REVISED STATUTES § 28-9702(E)", "",
          "When engaged, the automated driving system is considered",
          "the driver or operator of the autonomous vehicle for the",
          "purpose of assessing compliance with applicable traffic or",
          "motor vehicle laws."]
    shots["S51"] = doc(az, size=40, width=1500, font_fn=G.SERIF, highlight=span(az, "purpose of assessing compliance with applicable traffic or"),
                       hi_at=at("S51", "But only for traffic"), footer="recreated")
    uk = ["AUTOMATED VEHICLES ACT 2024 (UK)", "",
          "s.47  User-in-charge not liable for manner of driving", "",
          "s.6   Authorised self-driving entity: general responsibility", "",
          "s.25  False or withheld safety information, where an individual",
          "      is killed: imprisonment for a term not exceeding 14 years"]
    t_uk1 = at("S52", "Responsibility moves")
    shots["S52"] = G.seq((doc(uk, size=34, width=1500, highlight=span(uk, "User-in-charge not liable for manner of driving"),
                              hi_at=at("S52", "commits no offence"), footer="Not yet in force · planned 2027 · paraphrased headings"), t_uk1),
                         (doc(uk, size=34, width=1500, highlight=span(uk, "imprisonment for a term not exceeding 14 years"),
                              hi_at=at("S52", "fourteen years", offset=-t_uk1), footer="Not yet in force · planned 2027 · paraphrased headings", drift=0.0), 1))
    shots["S53"] = G.card_shot("“…not one problem but a set of at least four interconnected problems…”", "ARGUMENT",
                               "Santoni de Sio & Mecacci, 2021 · after Matthias, 2004")

    # V. THE VERDICT
    shots["S54"] = G.title_shot("V · THE VERDICT")
    shots["S55"] = E.clip_shot(C("scale_tip_right"), tag=None, overlay=E1.scale_overlay("THE STRONGEST CASE: THE DRIVER IS GUILTY"))
    shots["S56"] = E.clip_shot(C("scale_tip_left"), tag=None, overlay=E1.scale_overlay("THE STRONGEST CASE: THE SYSTEM IS GUILTY"))
    shots["S57"] = G.verdict_shot("The safety driver: responsible, but not the main cause. Endangerment fits. Homicide would not have.", 75,
                                  "Evidence she had been warned the system failed on that stretch of road, and looked away anyway.",
                                  meter_at=at("S57", "Our confidence"), change_at=at("S57", "What would change"), kicker="THE SAFETY DRIVER")
    shots["S58"] = G.verdict_shot("Uber carried the larger share of the blame, and the law had no tool to say so.", 80,
                                  "Evidence those choices were industry standard, signed off by independent safety reviewers.",
                                  meter_at=at("S58", "Our confidence"), change_at=at("S58", "What would change"), kicker="THE COMPANY")
    shots["S59"] = G.verdict_shot("With no one at the wheel, the company running the system stands where the driver stood, answerable in criminal court.", 65,
                                  "Evidence that criminal liability makes companies hide failures instead of fixing them.",
                                  meter_at=at("S59", "Our confidence"), change_at=at("S59", "What would change"), kicker="NO ONE AT THE WHEEL")
    shots["S60"] = E.clip_shot(C("scale_level_loaded", start=4), tag=None, fout=1.5)
    shots["S61"] = E1.stacked_words_shot([("NEXT CASE", G.MONO(30, True), G.RED),
                                          ("THE MIGNONETTE · 1884", G.SANS(58, "SemiBold"), G.INK),
                                          ("Is killing to survive murder?", G.SERIF_I(46), G.DIM)],
                                         [0.3, at("S61", "four men"), at("S61", "Is killing")])
    shots["S62"] = E1.endcard_shot()
    return shots


# ---------------------------------------------------------------- sound

def music(ctx):
    return [("S01", "S09", S.cue_open, 2), ("S10", "S19", S.cue_science, -2), ("S20", "S35", S.cue_patient, 0),
            ("S36", "S46", S.cue_law, -1), ("S47", "S53", S.cue_tower, 0), ("S54", "S62", S.cue_verdict, 0)]


def sfx(ctx):
    at = ctx.at
    ev = [("S01", 0.0, S.hum(ctx.dur["S01"]), -16), ("S04", 0.0, S.hum(ctx.dur["S04"]), -18),
          ("S33", 0.0, S.hum(ctx.dur["S33"]), -20), ("S45", 0.0, S.hum(ctx.dur["S45"]), -20),
          ("S09", 0.2, S.hit(), -3), ("S05", 0.4, S.hit(0.5), -10)]
    for sid in ("S18", "S22", "S24", "S27", "S28", "S30", "S31", "S34", "S39", "S40", "S41", "S44", "S49", "S53"):
        ev.append((sid, 0.0, S.card_drop(), -10))
    for sid in ("S19", "S35", "S46", "S55", "S56"):
        ev.append((sid, 0.3, S.clink(), -11))
    for sid, ph in (("S14", "threw away"), ("S25", "two to four seconds"), ("S32", "humans are very poor"),
                    ("S37", "The probable cause"), ("S51", "But only for traffic"), ("S52", "commits no offence")):
        ev.append((sid, at(sid, ph), S.marker(), -14))
    for sid in ("S02", "S13"):
        ev.append((sid, 0.0, S.hum(ctx.dur[sid], vol=0.025), -18))
    ev.append(("S17", 0.3, S.marker(0.4, vol=0.2), -10))
    for sid in ("S57", "S58", "S59"):
        ev.append((sid, at(sid, "Our confidence"), S.whoosh(1.4), -12))
    for sid in ("S10", "S20", "S36", "S47", "S54"):
        ev.append((sid, 0.1, S.whoosh(1.6), -10))
    return ev


if __name__ == "__main__":
    E.main(sys.modules[__name__])
