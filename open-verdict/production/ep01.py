"""Open Verdict, Case 01: The Tumor Defense. Shot definitions for edit.py.

    python ep01.py <prod_dir> --stills | --only S04,S28 | --final -j 2

Shot ids, picture notes and research IDs are in episodes/01-the-tumor-defense/script.md.
"""

import json
import math
import os
import random
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import edit as E  # noqa: E402
import gfx as G  # noqa: E402
import score as S  # noqa: E402

OUT_NAME = "open_verdict_case01.mp4"
TITLE = "Open Verdict, Case 01: The Tumor Defense"

SILENT = {"S09": 6.5, "S10": 3.4, "S22": 3.4, "S32": 3.4, "S44": 3.4, "S52": 3.4, "S61": 20.0}
LEAD = {"S01": 1.6, "S11": 0.4, "S23": 0.4, "S33": 1.2, "S45": 0.4, "S53": 0.6, "S60": 0.8}
PAD = {"S04": 1.2, "S06": 1.4, "S07": 1.6, "S08": 1.2, "S18": 1.4, "S19": 1.2, "S21": 2.6,
       "S25": 1.0, "S31": 1.0, "S35": 1.4, "S36": 3.0, "S39": 1.0, "S40": 1.2, "S43": 2.0,
       "S51": 1.8, "S55": 3.0, "S56": 2.0, "S58": 3.0, "S59": 2.0, "S60": 2.4}
FADE_IN = {"S01": 1.2, "S10": 0.6, "S22": 0.6, "S32": 0.6, "S44": 0.6, "S52": 0.6}
FADE_OUT = {"S08": 0.4, "S09": 1.0, "S21": 1.2, "S31": 1.0, "S43": 1.2, "S51": 1.0, "S59": 1.5,
            "S61": 1.5}
CHAPTERS = [("S01", "The night before prison"), ("S10", "I. The patient"), ("S22", "II. The test"),
            ("S32", "III. The tower"), ("S44", "IV. Everyone's brain"), ("S52", "V. The verdict"),
            ("S60", "Next case")]


# ---------------------------------------------------------------- illustrative scan

_scan_cache = {}


def _smooth_noise(shape, scale, seed):
    r = np.random.default_rng(seed)
    small = r.normal(0, 1, (shape[0] // scale + 2, shape[1] // scale + 2))
    img = Image.fromarray(((small - small.min()) / (np.ptp(small) + 1e-9) * 255).astype(np.uint8))
    return np.asarray(img.resize((shape[1], shape[0]), Image.BICUBIC)).astype(np.float32) / 255


def scan_layers(size=900):
    """Procedural axial 'MRI' slice (illustrative): skull, cortex with folds, ventricles,
    and a mass at front right. Radiological convention: patient's right on screen left."""
    if size in _scan_cache:
        return _scan_cache[size]
    n = size
    y, x = np.mgrid[0:n, 0:n].astype(np.float32)
    cx, cy = n / 2, n / 2
    dx, dy = (x - cx) / (n * 0.36), (y - cy) / (n * 0.44)
    r = np.sqrt(dx ** 2 + dy ** 2)
    ang = np.arctan2(dy, dx)
    wob = 0.015 * np.sin(ang * 7) + 0.01 * np.sin(ang * 13 + 1)
    skull = np.exp(-((r - (1.03 + wob)) / 0.025) ** 2)
    inside = (r < 0.99 + wob).astype(np.float32)
    folds = _smooth_noise((n, n), 18, 3)
    gyri = 0.5 + 0.5 * np.sin(folds * 40 + r * 25)
    cortex_band = np.clip((r - 0.62) / 0.3, 0, 1) * inside
    tissue = inside * (0.42 + 0.10 * _smooth_noise((n, n), 60, 4))
    tissue += cortex_band * (gyri - 0.5) * 0.22
    fis = np.exp(-(dx / 0.012) ** 2) * (np.abs(dy) < 0.97)  # midline fissure
    tissue *= 1 - 0.7 * fis
    for s in (-1, 1):  # lateral ventricles, butterfly-shaped dark regions
        vx, vy = (dx - s * 0.13) / 0.08, (dy + 0.02) / 0.32
        tissue *= 1 - 0.85 * np.exp(-(vx ** 2 + vy ** 2) ** 1.5)
    base = np.clip(tissue + skull * 0.95, 0, 1)
    # mass: front (top of image) and patient's right (image left)
    mx, my = (dx + 0.30) / 0.17, (dy + 0.55) / 0.15
    mr = np.sqrt(mx ** 2 + my ** 2)
    mass = np.clip(1.2 - mr, 0, 1) ** 0.6 * inside
    cyst = np.exp(-(((dx + 0.24) / 0.07) ** 2 + ((dy + 0.47) / 0.06) ** 2))
    mass_img = np.clip(mass * 0.75 - cyst * 0.5, 0, 1)
    to8 = lambda a: Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8))
    out = (to8(base), to8(mass_img), (int(cx - 0.30 * n * 0.36), int(cy - 0.55 * n * 0.44)))
    _scan_cache[size] = out
    return out


def scan_shot(ctx, sid, mass_at, outline_at=None, label=None):
    base, mass, (mx, my) = scan_layers()
    size = base.width

    def frame(t, dur):
        img = G.canvas((4, 5, 7))
        sweep = G.clamp(t / 2.2)
        k = G.ease((t - mass_at) / 1.2) if mass_at is not None else 0
        a = np.asarray(base).astype(np.float32) + np.asarray(mass).astype(np.float32) * k
        rows = int(size * sweep)
        a[rows:] *= 0.0
        if 0 < rows < size:  # bright scan line
            a[max(0, rows - 3):rows] = np.maximum(a[max(0, rows - 3):rows], 140)
        tint = np.stack([a * 0.92, a * 0.97, a], -1)
        sl = Image.fromarray(np.clip(tint, 0, 255).astype(np.uint8))
        z = 1.0 + 0.04 * G.ease(t / max(dur, 0.01))
        sl = sl.resize((int(size * z), int(size * z)), Image.LANCZOS)
        ox, oy = (G.W - sl.width) // 2, (G.H - sl.height) // 2
        img.paste(sl, (ox, oy))
        d = ImageDraw.Draw(img)
        d.text((ox - 70, G.H // 2 - 20), "R", font=G.MONO(34, True), fill=G.DIM)
        d.text((ox + sl.width + 40, G.H // 2 - 20), "L", font=G.MONO(34, True), fill=G.DIM)
        d.text((120, G.H - 120), "AXIAL · T1 + CONTRAST", font=G.MONO(24), fill=G.DIM)
        if outline_at is not None and t > outline_at:
            o = G.ease((t - outline_at) / 0.8)
            px, py = ox + mx * z, oy + my * z
            rad = 90 * z
            d.arc([px - rad, py - rad, px + rad, py + rad], -90, -90 + 360 * o, fill=G.CYAN, width=4)
            if label and o > 0.6:
                la = G.clamp((o - 0.6) / 0.4)
                d.line([px - rad, py, px - 260, py + 150], fill=G.CYAN, width=2)
                lay = G.text_layer(label, G.MONO(28, True), fill=G.CYAN, spacing=0.12)
                G.paste_alpha(img, lay, (px - 270 - lay.width, py + 130), la)
        G.recon_tag(img, G.fade(t, dur, 0.6, 0.4), "ILLUSTRATIVE · NOT THE PATIENT'S SCAN")
        f = G.fade(t, dur, 0.3, 0.4)
        if f < 1:
            img = Image.blend(G.canvas(), img, f)
        return G.finish(img, t)
    return frame


# ---------------------------------------------------------------- timeline (Virginia case)

T0, T1 = 2000.0, 2002.5  # years on the axis
EVENTS = [  # (key, year, label, row, placement)  row 0 behavior, 1 legal, 2 tumor
    # placement: "a" above / "b" below, then "l" label starts at the dot / "r" label ends at it
    ("collect", 2000.05, "Collecting; massage parlors; hides it", 0, "al"),
    ("removed", 2000.55, "Removed from home · found guilty", 1, "ar"),
    ("choice", 2000.72, "Treatment or jail", 1, "br"),
    ("expelled", 2000.86, "Expelled from program", 1, "al"),
    ("er", 2000.93, "Night before sentencing: ER", 2, "ar"),
    ("surg1", 2000.97, "Dec 2000: tumor removed", 2, "bl"),
    ("home", 2001.55, "Judged no threat · home", 1, "bl"),
    ("relapse", 2001.78, "Oct 2001: headache, collecting again", 0, "ar"),
    ("surg2", 2002.09, "Feb 2002: removed again", 2, "bl"),
]
ROWS = ["BEHAVIOR", "LEGAL", "TUMOR"]
ROW_COL = [G.BRASS, G.INK, G.CYAN]


def timeline_shot(ctx, sid, shown, reveal):
    """shown: event keys already visible; reveal: {key: time} for events that animate in."""
    x0, x1 = 300, G.W - 160
    ys = [430, 560, 690]

    def X(yr):
        return x0 + (x1 - x0) * (yr - T0) / (T1 - T0)

    def frame(t, dur):
        img = G.canvas()
        a = G.fade(t, dur, 0.4, 0.4)
        d = ImageDraw.Draw(img)
        col = lambda c, k=1.0: tuple(int(G.BG[i] + (c[i] - G.BG[i]) * a * k) for i in range(3))
        for i, name in enumerate(ROWS):
            d.text((120, ys[i] - 14), name, font=G.MONO(22, True), fill=col(G.DIM))
            d.line([x0, ys[i], x1, ys[i]], fill=col(G.FAINT), width=2)
        for yr in (2000, 2001, 2002):
            d.line([X(yr), 330, X(yr), 760], fill=col(G.FAINT), width=1)
            d.text((X(yr) + 8, 790), str(yr), font=G.MONO(26), fill=col(G.DIM))
        # behavior band (2000 → Dec 2000), (Oct 2001 → Feb 2002)
        bands = [("collect", 2000.05, 2000.97), ("relapse", 2001.78, 2002.09)]
        for key, b0, b1 in bands:
            if key in shown or key in reveal:
                k = 1.0 if key in shown else G.ease((t - reveal[key]) / 1.2)
                if k > 0:
                    xe = X(b0) + (X(b1) - X(b0)) * k
                    d.rectangle([X(b0), ys[0] - 9, xe, ys[0] + 9], fill=col(G.BRASS, 0.85))
        # tumor present: until surgery 1, then from relapse to surgery 2
        for key, b0, b1 in [("er", 2000.0, 2000.97), ("relapse", 2001.78, 2002.09)]:
            if key in shown or key in reveal:
                k = 1.0 if key in shown else G.ease((t - reveal[key]) / 1.0)
                if k > 0:
                    d.rectangle([X(b0), ys[2] - 6, X(b0) + (X(b1) - X(b0)) * k, ys[2] + 6],
                                fill=col(G.CYAN, 0.55))
        for key, yr, label, row, place in EVENTS:
            if key in shown:
                k = 1.0
            elif key in reveal:
                k = G.ease((t - reveal[key]) / 0.6)
            else:
                continue
            if k <= 0:
                continue
            x = X(yr)
            r = 9
            d.ellipse([x - r, ys[row] - r, x + r, ys[row] + r], fill=col(ROW_COL[row], k))
            lay = G.text_layer(label, G.SANS(26, "Medium"), fill=ROW_COL[row])
            ly = ys[row] - 58 if place[0] == "a" else ys[row] + 22
            lx = x - 10 if place[1] == "l" else x + 10 - lay.width
            lx = max(x0 - 40, min(lx, x1 - lay.width))
            G.paste_alpha(img, lay, (lx, ly), a * k)
        hdr = G.text_layer("THE VIRGINIA CASE · AS RECORDED", G.MONO(24), fill=G.DIM, spacing=0.25)
        G.paste_alpha(img, hdr, (120, 200), a)
        src = G.text_layer("Burns & Swerdlow, Arch Neurol 2003 · press accounts for 2002 outcome",
                           G.MONO(20), fill=G.FAINT)
        G.paste_alpha(img, src, (120, G.H - 110), a)
        return G.finish(img, t)
    return frame


# ---------------------------------------------------------------- on / off / on

def abab_shot(ctx, sid):
    t_on = ctx.at(sid, "tumor present")
    t_off = ctx.at(sid, "tumor gone")
    t_back = ctx.at(sid, "tumor back")
    t_quote = ctx.at(sid, "Swerdlow's own")
    phases = [(t_on, True), (t_off, False), (t_back, True)]
    x0, x1 = 360, G.W - 360
    seg = (x1 - x0) / 4

    def frame(t, dur):
        img = G.canvas()
        a = G.fade(t, dur, 0.4, 0.4)
        d = ImageDraw.Draw(img)
        q = G.ease((t - t_quote) / 0.6)
        lift = int(-150 * q)
        for row, (name, col, y) in enumerate([("TUMOR", G.CYAN, 420), ("BEHAVIOR", G.BRASS, 560)]):
            y += lift
            d.text((x0 - 230, y - 18), name, font=G.MONO(30, True), fill=tuple(int(c * a) for c in G.DIM))
            for i, (ts, on) in enumerate(phases):
                k = G.ease((t - ts) / 0.5)
                if k <= 0:
                    continue
                xs = x0 + i * seg
                c = col if on else G.FAINT
                c = tuple(int(G.BG[j] + (c[j] - G.BG[j]) * k * a) for j in range(3))
                d.rounded_rectangle([xs + 6, y - 34, xs + seg - 6, y + 34], radius=8, fill=c)
                lab = ("ON" if on else "OFF")
                lay = G.text_layer(lab, G.MONO(26, True), fill=G.BG if on else G.DIM)
                G.paste_alpha(img, lay, (xs + seg / 2 - lay.width / 2, y - lay.height / 2), k * a)
            # fourth phase: second surgery (press accounts)
            k4 = G.ease((t - t_back - 1.6) / 0.6)
            if k4 > 0:
                xs = x0 + 3 * seg
                d.rounded_rectangle([xs + 6, y - 34, xs + seg - 6, y + 34], radius=8,
                                    outline=tuple(int(c * k4 * a) for c in G.FAINT), width=2)
        if t > t_on:
            st = G.stamp("RECORD", 22)
            G.paste_alpha(img, st, (x1 - st.width, 250 + lift), a * G.ease((t - t_on) / 0.5))
        if q > 0:
            lines = G.wrap("“What he needed was an operation, not incarceration.”", G.SERIF_I(54), 1300)
            for i, ln in enumerate(lines):
                lay = G.text_layer(ln, G.SERIF_I(54), fill=G.INK)
                G.centered(img, lay, 720 + i * 70, a * q)
            s = G.text_layer("Russell Swerdlow, to Media General News Service, 2003", G.MONO(24), fill=G.DIM)
            G.centered(img, s, 720 + len(lines) * 70 + 30, a * q)
        return G.finish(img, t)
    return frame


# ---------------------------------------------------------------- the map

MAP_CONTROL = ["Georgia", "New Mexico", "Virginia", "Arkansas", "Connecticut", "Hawaii", "Kentucky",
               "Maryland", "Michigan", "North Dakota", "Oregon", "Rhode Island", "Vermont",
               "West Virginia", "Wisconsin", "Wyoming", "District of Columbia"]
MAP_ABOLISHED = ["Kansas", "Idaho", "Montana", "Utah"]


def build_map(prod):
    """Render map layers once with geopandas: base, control fill, abolished outline, Virginia."""
    out = os.path.join(prod, "renders", "map")
    meta_path = os.path.join(out, "meta.json")
    if os.path.exists(meta_path):
        return out, json.load(open(meta_path))
    import geopandas as gpd
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from shapely import affinity
    os.makedirs(out, exist_ok=True)
    shp = os.path.join(prod, "src", "states", "cb_2018_us_state_20m.shp")
    gdf = gpd.read_file(shp)
    gdf = gdf[~gdf.NAME.isin(["Puerto Rico"])].to_crs(5070)
    # insets: Alaska scaled and moved, Hawaii moved, both to lower left
    def move(name, fx, xoff, yoff):
        g = gdf.loc[gdf.NAME == name, "geometry"].iloc[0]
        c = g.centroid
        g = affinity.scale(g, fx, fx, origin=c)
        g = affinity.translate(g, xoff - c.x, yoff - c.y)
        gdf.loc[gdf.NAME == name, "geometry"] = gpd.GeoSeries([g], crs=gdf.crs).values
    move("Alaska", 0.35, -1.75e6, 0.45e6)
    move("Hawaii", 1.0, -0.85e6, 0.35e6)
    minx, miny, maxx, maxy = gdf.total_bounds
    W, H = 1920, 1080
    dpi = 100

    def layer(name, colors, edge, lw, alpha=True):
        fig = plt.figure(figsize=(W / dpi, H / dpi), dpi=dpi)
        ax = fig.add_axes([0.08, 0.14, 0.84, 0.74])
        ax.set_axis_off()
        ax.set_xlim(minx, maxx)
        ax.set_ylim(miny, maxy)
        ax.set_aspect("equal")
        for _, row in gdf.iterrows():
            fc = colors(row.NAME)
            ec = edge(row.NAME)
            if fc is None and ec is None:
                continue
            gpd.GeoSeries([row.geometry]).plot(ax=ax, facecolor=fc or "none", edgecolor=ec or "none",
                                                linewidth=lw)
        fig.savefig(os.path.join(out, f"{name}.png"), transparent=True, dpi=dpi)
        # pixel transform for later zooms
        tr = ax.transData
        plt.close(fig)
        return tr

    hexc = lambda c: "#%02x%02x%02x" % c
    layer("base", lambda n: hexc((38, 41, 48)), lambda n: hexc((70, 74, 82)), 0.6)
    layer("control", lambda n: hexc(G.BRASS) if n in MAP_CONTROL else None,
          lambda n: hexc((120, 96, 56)) if n in MAP_CONTROL else None, 0.6)
    layer("abolished", lambda n: None, lambda n: hexc(G.RED) if n in MAP_ABOLISHED else None, 2.4)
    layer("virginia", lambda n: hexc((246, 214, 150)) if n == "Virginia" else None,
          lambda n: hexc(G.INK) if n == "Virginia" else None, 1.6)
    # Virginia's pixel centre, from the same axes geometry
    va = gdf.loc[gdf.NAME == "Virginia", "geometry"].iloc[0].centroid
    fx = 0.08 + 0.84 * (va.x - minx) / (maxx - minx)
    fy = 0.14 + 0.74 * (va.y - miny) / (maxy - miny)
    # equal aspect: matplotlib centres the data box inside the axes; recompute exactly
    ax_w, ax_h = 0.84 * W, 0.74 * H
    sx = ax_w / (maxx - minx)
    sy = ax_h / (maxy - miny)
    s = min(sx, sy)
    ox = 0.08 * W + (ax_w - s * (maxx - minx)) / 2
    oy = 0.14 * H + (ax_h - s * (maxy - miny)) / 2
    vx = ox + s * (va.x - minx)
    vy = H - (oy + s * (va.y - miny))
    meta = {"va": [vx, vy]}
    json.dump(meta, open(meta_path, "w"))
    return out, meta


def map_shot(ctx, sid, zoom_va=False):
    folder, meta = build_map(ctx.prod)
    L = {k: Image.open(os.path.join(folder, f"{k}.png")).convert("RGBA")
         for k in ("base", "control", "abolished", "virginia")}
    if zoom_va:
        t_ctrl = t_abol = 0.0
        t_va = ctx.at(sid, "Virginia is one")
    else:
        t_ctrl = ctx.at(sid, "sixteen states")
        t_abol = ctx.at(sid, "four states")
        t_va = None

    def frame(t, dur):
        img = G.canvas().convert("RGBA")
        a = G.fade(t, dur, 0.4, 0.4)
        G.paste_alpha(img, L["base"], (0, 0), a)
        G.paste_alpha(img, L["control"], (0, 0), a * G.ease((t - t_ctrl) / 1.0))
        G.paste_alpha(img, L["abolished"], (0, 0), a * G.ease((t - t_abol) / 0.8))
        if t_va is not None:
            G.paste_alpha(img, L["virginia"], (0, 0), a * G.ease((t - t_va) / 0.6))
        img = img.convert("RGB")
        if zoom_va:
            z = 1 + 1.6 * G.ease((t - 0.2) / 3.0)
            vx, vy = meta["va"]
            cx = G.W / 2 + (vx - G.W / 2) * (1 - 1 / z) * 1.0
            cy = G.H / 2 + (vy - G.H / 2) * (1 - 1 / z) * 1.0
            cw, ch = G.W / z, G.H / z
            img = img.resize((G.W, G.H), Image.BICUBIC, box=(cx - cw / 2, cy - ch / 2, cx + cw / 2, cy + ch / 2))
            if t_va is not None and t > t_va:
                lab = G.text_layer("VIRGINIA · M'NAGHTEN + IRRESISTIBLE IMPULSE", G.MONO(26, True),
                                   fill=G.INK, spacing=0.1)
                G.paste_alpha(img, lab, (G.W // 2 - lab.width // 2, G.H - 200), a * G.ease((t - t_va) / 0.6))
        else:
            d = ImageDraw.Draw(img)
            ka, kb = G.ease((t - t_ctrl) / 1.0) * a, G.ease((t - t_abol) / 0.8) * a
            y = G.H - 120
            if ka > 0:
                d.rectangle([140, y, 170, y + 30], fill=tuple(int(c * ka) for c in G.BRASS))
                G.paste_alpha(img, G.text_layer("Asks whether the defendant could control himself (16 states + DC)",
                                                G.SANS(26), fill=G.INK), (185, y - 4), ka)
            if kb > 0:
                d.rectangle([140, y + 44, 170, y + 74], outline=tuple(int(c * kb) for c in G.RED), width=3)
                G.paste_alpha(img, G.text_layer("Traditional insanity defense abolished",
                                                G.SANS(26), fill=G.INK), (185, y + 40), kb)
        cap = G.text_layer("AS OF 2020 · JUSTICE BREYER'S COUNT, KAHLER v. KANSAS", G.MONO(22),
                           fill=G.DIM, spacing=0.15)
        G.paste_alpha(img, cap, (140, 110), a)
        return G.finish(img, t)
    return frame


# ---------------------------------------------------------------- other graphics

def stat_shot(ctx, sid):
    t1 = ctx.at(sid, "under one percent")
    t2 = ctx.at(sid, "about a quarter")

    def frame(t, dur):
        img = G.canvas()
        a = G.fade(t, dur, 0.4, 0.4)
        for i, (num, lab, ts) in enumerate([("< 1 in 100", "felony cases where the insanity defense is raised", t1),
                                            ("≈ 1 in 4", "of those pleas that succeed", t2)]):
            k = G.ease((t - ts) / 0.6) * a
            n = G.text_layer(num, G.SANS(120, "SemiBold"), fill=G.BRASS if i == 0 else G.INK)
            G.paste_alpha(img, n, (260 + i * 760, 360), k)
            l = G.wrap(lab, G.SANS(34), 560)
            for j, ln in enumerate(l):
                G.paste_alpha(img, G.text_layer(ln, G.SANS(34), fill=G.DIM), (265 + i * 760, 540 + j * 46), k)
        src = G.text_layer("Callahan et al., Bull Am Acad Psychiatry Law 1991 · eight states, data c. 1976–87",
                           G.MONO(22), fill=G.FAINT)
        G.paste_alpha(img, src, (260, G.H - 140), a)
        st = G.stamp("RECORD", 20)
        G.paste_alpha(img, st, (G.W - 260 - st.width, 250), a)
        return G.finish(img, t)
    return frame


VICTIMS = ["Margaret Whitman", "Kathleen Leissner Whitman", "Edna Townsley", "Mark Gabour",
           "Marguerite Lamport", "Thomas Eckman", "Baby Boy Wilson", "Robert Boyer", "Thomas Ashton",
           "Thomas Karr", "Karen Griffith", "Claudia Rutt", "Paul Sonntag", "Harry Walchuk",
           "Billy Paul Speed", "Roy Dell Schmidt", "David Gunby"]


def names_shot(ctx, sid):
    t0 = ctx.at(sid, "By today's count")
    step = 0.55

    def frame(t, dur):
        img = G.canvas()
        a = G.fade(t, dur, 0.6, 0.8)
        hdr = G.text_layer("THOSE KILLED", G.MONO(26, True), fill=G.DIM, spacing=0.4)
        G.centered(img, hdr, 170, a * G.ease(t / 1.0))
        cols = 3
        for i, name in enumerate(VICTIMS):
            k = G.ease((t - t0 - i * step) / 0.8) * a
            if k <= 0:
                continue
            c, r = i % cols, i // cols
            lay = G.text_layer(name, G.SERIF(38), fill=G.INK)
            x = G.W // 2 + (c - 1) * 560 - lay.width // 2
            G.paste_alpha(img, lay, (x, 270 + r * 92), k)
        k = G.ease((t - t0 - len(VICTIMS) * step) / 0.8) * a
        foot = G.text_layer("17 killed, by today's count, including an unborn child and David Gunby (died 2001) · 31 wounded",
                            G.SANS(28), fill=G.DIM)
        G.centered(img, foot, G.H - 150, k)
        return G.finish(img, t)
    return frame


def compare_shot(ctx, sid):
    rows = [("Neurological signs", "Yes: gait, bladder, drawing", "None reported"),
            ("Behavior tracks the tumor", "Twice: on, off, on", "No data"),
            ("Planning", "No", "Months"),
            ("Pathologist's view", "Tumor caused it (authors)", "“No correlation”")]
    t0 = ctx.at(sid, "Put the two")
    t_aus = ctx.at(sid, "In Austin")

    def frame(t, dur):
        img = G.canvas()
        a = G.fade(t, dur, 0.4, 0.4)
        d = ImageDraw.Draw(img)
        xs = [160, 820, 1380]
        G.paste_alpha(img, G.text_layer("VIRGINIA, 2000", G.MONO(30, True), fill=G.CYAN, spacing=0.15), (xs[1], 230), a)
        G.paste_alpha(img, G.text_layer("AUSTIN, 1966", G.MONO(30, True), fill=G.BRASS, spacing=0.15), (xs[2], 230), a)
        for i, (lab, va, au) in enumerate(rows):
            y = 340 + i * 130
            k1 = G.ease((t - t0 - 0.6 * i) / 0.6) * a
            k2 = G.ease((t - t_aus - 0.6 * i) / 0.6) * a
            d.line([xs[0], y - 30, G.W - 160, y - 30], fill=tuple(int(c * a) for c in G.FAINT), width=1)
            G.paste_alpha(img, G.text_layer(lab, G.SANS(32, "Medium"), fill=G.DIM), (xs[0], y), k1)
            G.paste_alpha(img, G.text_layer(va, G.SERIF(36), fill=G.INK), (xs[1], y), k1)
            G.paste_alpha(img, G.text_layer(au, G.SERIF(36), fill=G.INK), (xs[2], y), k2)
        st = G.stamp("INFERENCE", 20)
        G.paste_alpha(img, st, (G.W - 160 - st.width, 140), a)
        return G.finish(img, t)
    return frame


def brain_outline(cx, cy, s):
    """Lateral brain silhouette as a polygon (front faces left)."""
    pts = []
    for k in range(200):
        th = 2 * math.pi * k / 200
        r = 1 + 0.06 * math.sin(3 * th) + 0.03 * math.sin(7 * th)
        x = math.cos(th) * 1.25 * r
        y = math.sin(th) * 0.85 * r
        if y > 0.35:  # flatten the underside, notch for the temporal lobe
            y = 0.35 + (y - 0.35) * 0.5
        pts.append((cx + x * s, cy + y * s))
    return pts


def network_shot(ctx, sid):
    t_dots = ctx.at(sid, "seventeen cases")
    t_wire = ctx.at(sid, "when the team mapped")
    t_warn = ctx.at(sid, "The authors added")
    cx, cy, s = G.W / 2, G.H / 2 - 20, 330
    rng = random.Random(17)
    dots = []
    while len(dots) < 17:
        x, y = rng.uniform(-1.1, 1.1), rng.uniform(-0.75, 0.5)
        if (x / 1.15) ** 2 + (y / 0.8) ** 2 < 0.85:
            dots.append((cx + x * s, cy + y * s))
    hubs = [(cx - 0.95 * s, cy + 0.22 * s), (cx - 0.35 * s, cy + 0.42 * s), (cx - 0.7 * s, cy - 0.05 * s)]
    outline = brain_outline(cx, cy, s)

    def frame(t, dur):
        img = G.canvas()
        a = G.fade(t, dur, 0.4, 0.4)
        d = ImageDraw.Draw(img, "RGBA")
        d.line(outline + [outline[0]], fill=G.CYAN + (int(140 * a),), width=3)
        hub_k = G.ease((t - t_wire - 1.2) / 1.0) * a
        for hx, hy in hubs:
            for rr, al in ((48, 40), (30, 80), (16, 220)):
                d.ellipse([hx - rr, hy - rr, hx + rr, hy + rr], fill=G.BRASS + (int(al * hub_k),))
        for i, (x, y) in enumerate(dots):
            k = G.ease((t - t_dots - 0.08 * i) / 0.4) * a
            if k <= 0:
                continue
            w = G.ease((t - t_wire - 0.05 * i) / 0.9) * a
            if w > 0:
                hx, hy = hubs[i % len(hubs)]
                d.line([x, y, x + (hx - x) * w, y + (hy - y) * w], fill=G.BRASS + (int(120 * w),), width=2)
            d.ellipse([x - 9, y - 9, x + 9, y + 9], fill=G.RED + (int(255 * k),))
        lab = G.text_layer("17 LESIONS · DIFFERENT PLACES · ONE NETWORK", G.MONO(24, True), fill=G.DIM, spacing=0.15)
        G.centered(img, lab, 150, a * G.ease((t - t_dots) / 0.6))
        if t > t_warn:
            k = G.ease((t - t_warn) / 0.6) * a
            w = G.text_layer("Most people with damage in this network never commit a crime.", G.SERIF_I(38), fill=G.INK)
            G.centered(img, w, G.H - 170, k)
        src = G.text_layer("Darby, Horn, Cushman & Fox, PNAS 2018 · schematic", G.MONO(20), fill=G.FAINT)
        G.paste_alpha(img, src, (120, G.H - 90), a)
        return G.finish(img, t)
    return frame


def bars_shot(ctx, sid):
    t1 = ctx.at(sid, "more than a third")
    t2 = ctx.at(sid, "Among Alzheimer's")
    bars = [("Behavioral-variant frontotemporal dementia", 37.4, G.BRASS, t1),
            ("Alzheimer's disease", 7.7, G.DIM, t2)]

    def frame(t, dur):
        img = G.canvas()
        a = G.fade(t, dur, 0.4, 0.4)
        d = ImageDraw.Draw(img)
        x0, full = 260, 1300
        G.paste_alpha(img, G.text_layer("NEW CRIMINAL BEHAVIOR DURING ILLNESS", G.MONO(26, True), fill=G.DIM, spacing=0.2), (x0, 250), a)
        for i, (lab, v, c, ts) in enumerate(bars):
            y = 400 + i * 220
            k = G.ease((t - ts) / 1.2) * a
            G.paste_alpha(img, G.text_layer(lab, G.SANS(34), fill=G.INK), (x0, y - 60), a * G.ease((t - ts) / 0.4))
            d.rectangle([x0, y, x0 + full, y + 60], fill=tuple(int(cc * a) for cc in (18, 20, 24)))
            if k > 0:
                d.rectangle([x0, y, x0 + full * v / 100 * k, y + 60], fill=tuple(int(cc * a) for cc in c))
                G.paste_alpha(img, G.text_layer(f"{v * min(1, k / max(k, 1e-6)):.1f}%", G.SANS(48, "SemiBold"), fill=G.INK),
                              (x0 + full * v / 100 * k + 24, y), k)
        src = G.text_layer("Liljegren et al., JAMA Neurology 2015 · UCSF, 2,397 patients", G.MONO(22), fill=G.FAINT)
        G.paste_alpha(img, src, (x0, G.H - 140), a)
        return G.finish(img, t)
    return frame


def stacked_words_shot(lines, times):
    """Lines of type appearing one under another at given times."""
    def frame(t, dur):
        img = G.canvas()
        a = G.fade(t, dur, 0.4, 0.5)
        for i, ((text, fnt, col), ts) in enumerate(zip(lines, times)):
            lay = G.text_layer(text, fnt, fill=col, spacing=0.08)
            G.centered(img, lay, 380 + i * 150, a * G.ease((t - ts) / 0.6))
        return G.finish(img, t)
    return frame


def endcard_shot():
    def frame(t, dur):
        img = G.canvas()
        a = G.fade(t, dur, 1.0, 1.5)
        G.centered(img, G.text_layer("OPEN VERDICT", G.SANS(84, "SemiBold"), fill=G.INK, spacing=0.12), 230, a)
        G.centered(img, G.text_layer("One question. The evidence. A verdict.", G.SERIF_I(40), fill=G.DIM), 320, a)
        d = ImageDraw.Draw(img)
        for x in (300, 1020):  # end-screen slots
            d.rounded_rectangle([x, 470, x + 600, 808], radius=10, outline=tuple(int(c * a) for c in G.FAINT), width=2)
        G.centered(img, G.text_layer("Sources for every claim are in the description.", G.MONO(24), fill=G.DIM), 900, a)
        return G.finish(img, t)
    return frame


def scale_overlay(text):
    def ov(img, t, dur):
        G.lower_third(img, text, None, G.ramp(t, 0.4, 0.5) * G.fade(t, dur, 0.01, 0.4))
    return ov


def caption_overlay(text, at=0.3):
    def ov(img, t, dur):
        lay = G.text_layer(text, G.MONO(26, True), fill=G.INK, spacing=0.15)
        G.paste_alpha(img, lay, (120, G.H - 150), G.ramp(t, at, 0.5) * G.fade(t, dur, 0.01, 0.4))
    return ov


# ---------------------------------------------------------------- the shots

def span(lines, sub):
    """(line, start, end) of the first line containing sub, for document highlights."""
    for i, ln in enumerate(lines):
        k = ln.find(sub)
        if k >= 0:
            return (i, k, k + len(sub))
    raise ValueError(sub)


def build(ctx):
    P = ctx.prod
    C = lambda name, **kw: E.Clip(P, name, **kw)
    at = ctx.at
    doc = G.document_shot
    shots = {}

    shots["S01"] = E.clip_shot(C("corridor"), overlay=lambda img, t, d: G.lower_third(
        img, "University of Virginia Hospital", "CHARLOTTESVILLE · 2000", G.ramp(t, 2.0, 0.8) * G.fade(t, d, 0.01, 0.6)))
    shots["S02"] = G.card_shot("“The evening before his prison sentencing, he came to the University of Virginia Hospital…”",
                               "RECORD", "Burns & Swerdlow, Archives of Neurology, 2003")
    shots["S03"] = E.clip_shot(C("brain_clean"), tag="ILLUSTRATION")
    shots["S04"] = scan_shot(ctx, "S04", mass_at=at("S04", "a tumor"))
    shots["S05"] = E.xfade_shot(C("brain_tumor", start=6), C("brain_clean", start=6), at("S05", "removed it"), 1.6, glow="a")
    shots["S06"] = E.xfade_shot(C("brain_clean", start=9), C("brain_tumor", start=9), at("S06", "grown back"), hard=True, glow="b")
    shots["S07"] = E.clip_shot(C("scale_empty"), tag=None)
    shots["S08"] = G.words_shot("Hold on to your answer. The same logic, followed all the way down, could set almost everyone free.",
                                size=62, emphasis={"almost", "everyone"}, per_word=0.32, start=at("S08", "Hold on"))
    shots["S09"] = G.title_shot("THE TUMOR DEFENSE", "If a tumor made him do it, is he guilty?", "OPEN VERDICT · CASE 01")
    shots["S10"] = G.title_shot("I · THE PATIENT")
    shots["S11"] = doc(["ARCHIVES OF NEUROLOGY · VOL. 60 · MARCH 2003", "",
                        "Right Orbitofrontal Tumor With Pedophilia", "Symptom and Constructional Apraxia Sign", "",
                        "Jeffrey M. Burns, MD; Russell H. Swerdlow, MD", "University of Virginia, Charlottesville"],
                       font_fn=G.SERIF, size=46, header="CASE REPORT", footer="Title block recreated; text as published")
    shots["S12"] = timeline_shot(ctx, "S12", set(), {"collect": at("S12", "In 2000")})
    shots["S13"] = timeline_shot(ctx, "S13", {"collect"}, {"removed": at("S13", "removed from the home"),
                                                           "choice": at("S13", "A judge"), "expelled": at("S13", "expelled")})
    shots["S14"] = E.clip_shot(C("corridor", start=1, speed=0.75))
    shots["S15"] = scan_shot(ctx, "S15", mass_at=0.0, outline_at=at("S15", "pushing into"), label="RIGHT ORBITOFRONTAL CORTEX")
    shots["S16"] = E.xfade_shot(C("brain_tumor", start=2, speed=0.7), C("brain_clean", start=2, speed=0.7),
                                at("S16", "removed in December"), 1.6, glow="a",
                                overlay=caption_overlay("DECEMBER 2000 · REMOVED", at("S16", "removed in December")))
    shots["S17"] = timeline_shot(ctx, "S17", {"collect", "removed", "choice", "expelled", "er", "surg1", "home"},
                                 {"relapse": at("S17", "In October"), "surg2": at("S17", "removed again")})
    shots["S18"] = abab_shot(ctx, "S18")
    shots["S19"] = E.clip_shot(C("scale_tip_left"), tag=None, overlay=scale_overlay("EVIDENCE · THE TUMOR TRACKED THE BEHAVIOR"))
    shots["S20"] = G.card_shot("The tumor likely made an existing interest worse. It did not create one from nothing.",
                               "INFERENCE", "Burns & Swerdlow 2003; Joyal 2023 (64 cases)")
    shots["S21"] = G.words_shot("A child was harmed.", size=84, per_word=0.4, start=at("S21", "A child"))
    shots["S22"] = G.title_shot("II · THE TEST")
    mnag = ["M'NAGHTEN'S CASE · HOUSE OF LORDS · 1843", "",
            "…it must be clearly proved that, at the time of",
            "the committing of the act, the party accused was",
            "labouring under such a defect of reason, from",
            "disease of the mind, as not to know the nature and",
            "quality of the act he was doing; or, if he did know",
            "it, that he did not know he was doing what was wrong."]
    shots["S23"] = doc(mnag, font_fn=G.SERIF, size=40, footer="10 Cl. & F. 200 · recreated")
    shots["S24"] = doc(mnag, font_fn=G.SERIF, size=40, footer="10 Cl. & F. 200 · recreated",
                       highlight=span(mnag, "that he did not know he was doing what was wrong"), hi_at=at("S24", "know that it was wrong"))
    shots["S25"] = E.clip_shot(C("scale_swing"), tag=None, overlay=scale_overlay("EVIDENCE · HE KNEW IT WAS WRONG"))
    mpc = ["MODEL PENAL CODE § 4.01 · AMERICAN LAW INSTITUTE · 1962", "",
           "A person is not responsible for criminal conduct if at",
           "the time of such conduct as a result of mental disease",
           "or defect he lacks substantial capacity either to",
           "appreciate the criminality [wrongfulness] of his conduct",
           "or to conform his conduct to the requirements of law."]
    shots["S26"] = doc(mpc, font_fn=G.SERIF, size=40, footer="recreated", highlight=span(mpc, "or to conform his conduct to the requirements of law"),
                       hi_at=at("S26", "Or could he"))
    shots["S27"] = stacked_words_shot(
        [("JUNE 21, 1982", G.MONO(40, True), G.DIM), ("NOT GUILTY BY REASON OF INSANITY", G.SANS(58, "SemiBold"), G.INK),
         ("1984 · INSANITY DEFENSE REFORM ACT", G.MONO(40, True), G.BRASS)],
        [at("S27", "in 1982"), at("S27", "not guilty"), at("S27", "Two years later")])
    shots["S28"] = map_shot(ctx, "S28")
    shots["S29"] = map_shot(ctx, "S29", zoom_va=True)
    shots["S30"] = stat_shot(ctx, "S30")
    shots["S31"] = E.clip_shot(C("scale_swing", start=3), tag=None)
    shots["S32"] = G.title_shot("III · THE TOWER")
    shots["S33"] = E.clip_shot(C("tower_push"), overlay=lambda img, t, d: G.lower_third(
        img, "Austin, Texas", "JULY 31, 1966", G.ramp(t, 1.5, 0.8) * G.fade(t, d, 0.01, 0.6)))
    note = ["Sunday July 31, 1966  6:45 P.M.", "",
            "I don't quite understand what it is that compels me to",
            "type this letter. Perhaps it is to leave some vague reason",
            "for the actions I have recently performed. I don't really",
            "understand myself these days. I am supposed to be an",
            "average reasonable and intelligent young man. However,",
            "lately (I can't recall when it started) I have been a",
            "victim of many unusual and irrational thoughts."]
    shots["S34"] = doc(note, header="TYPED NOTE · AUSTIN HISTORY CENTER", type_secs=at("S34", "However", end=True) + 1.5,
                       size=36, footer="Excerpt, original spelling · recreated")
    note2 = ["After my death I wish that an autopsy would be performed", "on me to see if there is any visible physical disorder.",
             "I have had some tremendous headaches in the past and have", "consumed two large bottles of Excedrin in the past three months."]
    shots["S35"] = doc(note2, header="TYPED NOTE · CONTINUED", size=36, highlight=span(note2, "visible physical disorder"),
                       hi_at=at("S35", "visible physical disorder"), footer="Excerpt · recreated")
    shots["S36"] = names_shot(ctx, "S36")
    autopsy = ["AUTOPSY PROTOCOL · AUGUST 2, 1966", "",
               "In the middle part of the brain, above the red nucleus,",
               "in the white matter below the gray center thalamus, is",
               "a fairly well outlined tumor about 2x1.5x1 cm in dimensions."]
    shots["S37"] = doc(autopsy, size=38, highlight=span(autopsy, "a fairly well outlined tumor about 2x1.5x1 cm"), hi_at=at("S37", "a tumor"), footer="Excerpt · recreated")
    shots["S38"] = G.still_shot(os.path.join(P, "renders", "brain_deep.png"), zoom=(1.0, 1.1), tag="ILLUSTRATION",
                                overlay=caption_overlay("THE STORY YOU'VE HEARD", 0.8))
    autopsy2 = ["AUTOPSY PROTOCOL · DIAGNOSIS", "",
                "Additional finding: a small brain tumor in the white matter",
                "above the brain stem ... (Astrocytoma).",
                "No correlation to psychosis or permanent pains."]
    limits = ["REPORT TO THE GOVERNOR · SEPTEMBER 8, 1966", "",
              "1. The autopsy was not performed until approximately 24 hours after death.",
              "2. The body had received arterial and trochar embalming.",
              "3. Many parts of the brain were damaged by penetrating fragments of bone.",
              "4. All of the pieces of the brain were not recovered.",
              "5. The brain had been sectioned at the time of the autopsy."]
    t_panel = at("S39", "A panel")
    shots["S39"] = G.seq((doc(autopsy2, size=38, highlight=span(autopsy2, "No correlation to psychosis or permanent pains."), hi_at=at("S39", "No correlation"), footer="Excerpt · recreated"), t_panel),
                         (doc(limits, size=30, width=1600, font_fn=G.SERIF, footer="Excerpt, abridged · recreated"), 1))
    panel = ["REPORT TO THE GOVERNOR · CONCLUSIONS", "",
             "…the highly malignant brain tumor conceivably could have",
             "contributed to his inability to control his emotions and actions.", "",
             "…the application of existing knowledge of organic brain function",
             "does not enable us to explain the actions of Whitman on August first."]
    t_but = at("S40", "But they also")
    shots["S40"] = G.seq((doc(panel, size=34, width=1600, font_fn=G.SERIF, highlight=span(panel, "conceivably could have"), hi_at=at("S40", "conceivably"), footer="recreated"), t_but),
                         (doc(panel, size=34, width=1600, font_fn=G.SERIF, highlight=span(panel, "does not enable us to explain"), hi_at=0.2, footer="recreated", drift=0.0), 1))
    shots["S41"] = E.clip_shot(C("scale_tip_right", speed=0.5), tag=None, overlay=scale_overlay("EVIDENCE · MONTHS OF PLANNING"))
    shots["S42"] = compare_shot(ctx, "S42")
    shots["S43"] = E.clip_shot(C("tower_push", reverse=True))
    shots["S44"] = G.title_shot("IV · EVERYONE'S BRAIN")
    shots["S45"] = network_shot(ctx, "S45")
    shots["S46"] = bars_shot(ctx, "S46")
    shots["S47"] = E.clip_shot(C("scale_bottom_left", speed=0.5), tag=None)
    shots["S48"] = G.card_shot("Everything we do comes down to the luck of our biology and our environment, and we control neither.",
                               "ARGUMENT", "Robert Sapolsky, Determined (2023), paraphrased")
    shots["S49"] = G.card_shot("“Brains do not commit crimes; people commit crimes.”", "ARGUMENT",
                               "Stephen J. Morse, Ohio State Journal of Criminal Law, 2006")
    shots["S50"] = G.card_shot("“…a shift away from punishment aimed at retribution in favour of a more progressive, consequentialist approach.”",
                               "ARGUMENT", "Greene & Cohen, Phil. Trans. R. Soc. B, 2004")
    shots["S51"] = E.clip_shot(C("scale_level_loaded"), tag=None)
    shots["S52"] = G.title_shot("V · THE VERDICT")
    shots["S53"] = E.clip_shot(C("scale_tip_right"), tag=None, overlay=scale_overlay("THE STRONGEST CASE: GUILTY"))
    shots["S54"] = E.clip_shot(C("scale_tip_left"), tag=None, overlay=scale_overlay("THE STRONGEST CASE: NOT GUILTY"))
    shots["S55"] = G.verdict_shot("Responsible, but far less so. He needed surgery and supervision, not prison.", 70,
                                  "Evidence he had acted on a sexual interest in children before the tumor.",
                                  meter_at=at("S55", "Our confidence"), change_at=at("S55", "What would change"))
    shots["S56"] = G.verdict_shot("The man in the tower: the tumor deserves a footnote, not an acquittal.", 85,
                                  meter_at=at("S56", "Our confidence"), kicker="ON THE TOWER")
    t57 = at("S57", "Our verdict is no")
    shots["S57"] = G.verdict_shot("No. A cause is not an excuse. What excuses is losing the ability to respond to reasons.", 60,
                                  meter_at=999, kicker="DOES NEUROSCIENCE EXCUSE EVERYONE?")
    shots["S58"] = G.verdict_shot("No. A cause is not an excuse. What excuses is losing the ability to respond to reasons.", 60,
                                  "Proof that ordinary offenders' self-control is impaired almost as badly as his.",
                                  meter_at=at("S58", "sixty percent") + 3.0, change_at=at("S58", "What would change") + 3.0,
                                  offset=3.0, kicker="DOES NEUROSCIENCE EXCUSE EVERYONE?")
    shots["S59"] = E.clip_shot(C("scale_level_loaded", start=4), tag=None, fout=1.5)
    shots["S60"] = stacked_words_shot([("NEXT CASE", G.MONO(30, True), G.RED),
                                       ("TEMPE, ARIZONA · MARCH 18, 2018", G.SANS(58, "SemiBold"), G.INK),
                                       ("When the machine kills, who's guilty?", G.SERIF_I(46), G.DIM)],
                                      [0.3, at("S60", "Tempe"), at("S60", "When the machine")])
    shots["S61"] = endcard_shot()
    del t57
    return shots


# ---------------------------------------------------------------- sound

def music(ctx):
    return [("S01", "S09", S.cue_open, 2), ("S10", "S21", S.cue_patient, 0), ("S22", "S31", S.cue_law, -1),
            ("S32", "S43", S.cue_tower, 1), ("S44", "S51", S.cue_science, -2), ("S52", "S61", S.cue_verdict, 0)]


def sfx(ctx):
    at = ctx.at
    ev = [("S01", 0.0, S.hum(ctx.dur["S01"]), -16), ("S14", 0.0, S.hum(ctx.dur["S14"]), -18),
          ("S02", 0.0, S.card_drop(), -10), ("S20", 0.0, S.card_drop(), -10),
          ("S48", 0.0, S.card_drop(), -10), ("S49", 0.0, S.card_drop(), -10), ("S50", 0.0, S.card_drop(), -10),
          ("S06", at("S06", "grown back"), S.hit(0.6), -6),
          ("S09", 0.2, S.hit(), -3),
          ("S19", 0.3, S.clink(), -10), ("S25", 0.3, S.clink(), -12), ("S41", 0.3, S.clink(), -10),
          ("S47", 0.3, S.clink(), -10), ("S53", 0.3, S.clink(), -12), ("S54", 0.3, S.clink(), -12),
          ("S24", at("S24", "know that it was wrong"), S.marker(), -14),
          ("S26", at("S26", "Or could he"), S.marker(), -14),
          ("S35", at("S35", "visible physical disorder"), S.marker(), -14),
          ("S37", at("S37", "a tumor"), S.marker(), -14),
          ("S39", at("S39", "No correlation"), S.marker(), -14),
          ("S40", at("S40", "conceivably"), S.marker(), -14),
          ("S34", 0.3, S.typing(min(ctx.dur["S34"] - 1, at("S34", "However", end=True) + 1.2)), -16),
          ("S55", at("S55", "Our confidence"), S.whoosh(1.4), -12),
          ("S58", at("S58", "sixty percent"), S.whoosh(1.4), -12)]
    for sid in ("S10", "S22", "S32", "S44", "S52"):
        ev.append((sid, 0.1, S.whoosh(1.6), -10))
    return ev


def prepare(prod):
    """One-off stills: the Whitman brain with a deep-centre mass (scenes.py, Cycles)."""
    out = os.path.join(prod, "renders", "brain_deep.png")
    if os.path.exists(out):
        return
    import subprocess
    tmp = os.path.join(prod, "renders", "tmp")
    py = os.environ.get("OV_PY", sys.executable)
    subprocess.run([py, os.path.join(HERE, "scenes.py"), "brain", tmp, "--res", "1920x1080", "--samples", "24",
                    "tumor=0.55", "site=deep", "view=side", "orbit=0", "name=brain_deep"], check=True,
                   stdout=subprocess.DEVNULL)
    os.replace(os.path.join(tmp, "brain_deep_0000.png"), out)


if __name__ == "__main__":
    if "--prepare" in sys.argv:
        prepare(sys.argv[1])
        build_map(sys.argv[1])
    else:
        E.main(sys.modules[__name__])
