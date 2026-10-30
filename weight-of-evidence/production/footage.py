"""Footage for every episode: B-roll sequences cut to the narration (our Blender clips first,
Higgsfield clips where only a real-world place will do), and the existing graphics (cards, rows,
numbers) composited over moving, darkened footage instead of black.

    broll(prod, [("clip_a", 4.5), ("clip_b", 5.0, 2.0), "clip_c"])  # (name, secs[, start]); last takes the rest
    over(broll(prod, [...], stamp=False), graphic_fn)            # a graphic over darkened footage

Clips live in <prod>/anim/<name>.mp4. The honesty tag follows the clip on screen (FORMAT.md §2):
generated clips (ai_*) say ILLUSTRATIVE · AI-GENERATED, Blender clips say RECONSTRUCTION, the
Scale carries none; pass tags={name: label} for anything more specific. Generated clips show a
place or an object, never a person involved in the case, and are never passed off as archival.
"""

from PIL import Image, ImageFilter

import edit as E
import gfx as G

TAG = "ILLUSTRATIVE · AI-GENERATED"


def is_generated(name):
    return name.startswith("ai_")


def default_tag(name):
    if is_generated(name):
        return TAG
    return None if name.startswith("scale_") else "RECONSTRUCTION"


def _grade(img, k=1.0):
    """The channel look on footage: slightly crushed, cooled, desaturated."""
    gray = img.convert("L").convert("RGB")
    img = Image.blend(img, gray, 0.22)
    r, g, b = img.split()
    b = b.point(lambda v: min(255, int(v * 1.04 + 3)))
    r = r.point(lambda v: int(v * 0.97))
    img = Image.merge("RGB", (r, g, b))
    return img.point(lambda v: int(max(0, v - 6) * 1.04 * k))


def clip_frame(prod, name, start=0.0, push=None):
    """One clip as a frame function. Generated clips get the channel grade and a slow digital push
    of their own; Blender clips already have both, so they play as rendered."""
    gen = is_generated(name)
    push = (0.04 if gen else 0.0) if push is None else push
    clip = E.Clip(prod, name, start=start)

    def frame(t, dur):
        img = clip.frame(t, dur)
        z = 1.0 + push * (t / max(dur, 0.01))
        if z > 1.0:
            w, h = img.size
            cw, ch = int(w / z), int(h / z)
            img = img.crop(((w - cw) // 2, (h - ch) // 2, (w + cw) // 2, (h + ch) // 2)).resize((w, h), Image.LANCZOS)
        return _grade(img) if gen else img
    return frame


def broll(prod, items, tags=None, stamp=True, fin=0.4, fout=0.4, xfade=0.35, overlay=None):
    """Cut a run of clips under the narration. items: names or (name, seconds); the last item takes
    whatever is left of the shot. Short dissolves between clips, grain and the clip's honesty tag on
    top (stamp=False leaves the tag to over())."""
    parts = [(it, None, 0.0) if isinstance(it, str) else (tuple(it) + (0.0,))[:3] for it in items]
    tags = tags or {}

    def current(t, dur):
        acc = 0.0
        for i, (name, secs, _) in enumerate(parts):
            length = (dur - acc) if i == len(parts) - 1 else secs
            if t < acc + length or i == len(parts) - 1:
                return name
            acc += length

    def tag_at(t, dur):
        name = current(t, dur)
        return tags.get(name, default_tag(name))

    def frame(t, dur):
        acc, cur, nxt, local = 0.0, None, None, 0.0
        for i, (name, secs, start) in enumerate(parts):
            last = i == len(parts) - 1
            length = (dur - acc) if last else secs
            if t < acc + length or last:
                cur, local, seg = (name, i, start), t - acc, max(length, 0.01)
                if not last and length - local < xfade:
                    nxt = (parts[i + 1][0], i + 1, parts[i + 1][2])
                break
            acc += length
        img = _cached(prod, cur)(local, seg + xfade)
        if nxt:
            a = 1 - (seg - local) / xfade
            img = Image.blend(img, _cached(prod, nxt)(0.0, 5.0), max(0.0, min(1.0, a)))
        a = G.fade(t, dur, fin, fout)
        if a < 1:
            img = Image.blend(G.canvas(), img, max(0.0, a))
        if overlay:
            overlay(img, t, dur)
        label = tag_at(t, dur)
        if stamp and label:
            st = G.stamp(label, 18)
            G.paste_alpha(img, st, (G.W - st.width - 60, 52), 0.8 * a)
        return G.finish(img, t)
    frame.tag_at = tag_at
    return frame


_CLIPS = {}


def _cached(prod, key):
    """Each (clip, position in the run) keeps its own reader so frames stream sequentially."""
    name, i, start = key
    k = (prod, name, i)
    if k not in _CLIPS:
        _CLIPS[k] = clip_frame(prod, name, start=start)
    return _CLIPS[k]


def over(footage, graphic, dim=0.38, blur=6, clear_until=0.0, ramp=0.6):
    """A graphic over footage. The footage is blurred and dimmed so type stays readable; the
    graphic's near-black ground drops out, so cards, rows and numbers sit on top. Until
    clear_until (seconds) the footage plays clear, then eases down over ramp seconds as the
    graphic arrives. The honesty tag goes on last so the graphic never covers it."""
    def frame(t, dur):
        k = min(1.0, max(0.0, (t - clear_until) / ramp)) if clear_until > 0 else 1.0
        bg = footage(t, dur)
        if k > 0:
            d = 1 - (1 - dim) * k
            bg = bg.filter(ImageFilter.GaussianBlur(blur * k)).point(lambda v: int(v * d))
        fg = graphic(t, dur)
        # the graphic's near-black ground (and its grain) drops out entirely; type and cards stay
        img = Image.composite(fg, bg, fg.convert("L").point(lambda v: 255 if v > 40 else max(0, (v - 20) * 12)))
        tag = footage.tag_at(t, dur) if hasattr(footage, "tag_at") else None
        if tag:
            st = G.stamp(tag, 18)
            G.paste_alpha(img, st, (G.W - st.width - 60, 52), 0.8 * G.fade(t, dur, 0.4, 0.4))
        return img
    return frame


def delay(graphic, d):
    """A graphic that starts d seconds into the shot (black before), its own timing intact, so the
    footage under it can play clean first."""
    def frame(t, dur):
        if t < d:
            return G.canvas()
        return graphic(t - d, max(0.01, dur - d))
    return frame


# ---------------------------------------------------------------- 9:16 (Shorts)

VW, VH = 1080, 1920


def to_vertical(img, cx=0.5):
    """A 16:9 frame scaled to full 9:16 height and cropped around cx (0..1 across the frame)."""
    w = int(img.width * VH / img.height)
    big = img.resize((w, VH), Image.LANCZOS)
    x = int(min(max(0, cx * w - VW / 2), w - VW))
    return big.crop((x, 0, x + VW, VH))


def over_v(footage, graphic, dim=0.38, blur=8, clear_until=0.0, ramp=0.6, cx=0.5):
    """over() for Shorts: the footage cropped to 9:16 under a vertical graphic, its tag top right
    (below the kicker). dim=1, blur=0 plays the footage clean under captions only."""
    def frame(t, dur):
        k = min(1.0, max(0.0, (t - clear_until) / ramp)) if clear_until > 0 else 1.0
        bg = to_vertical(footage(t, dur), cx)
        if k > 0 and (dim < 1 or blur > 0):
            d = 1 - (1 - dim) * k
            bg = bg.filter(ImageFilter.GaussianBlur(blur * k)).point(lambda v: int(v * d))
        fg = graphic(t, dur)
        img = Image.composite(fg, bg, fg.convert("L").point(lambda v: 255 if v > 40 else max(0, (v - 20) * 12)))
        tag = footage.tag_at(t, dur) if hasattr(footage, "tag_at") else None
        if tag:
            st = G.stamp(tag, 18)
            G.paste_alpha(img, st, (VW - st.width - 40, 196), 0.85 * G.fade(t, dur, 0.3, 0.3))
        return img
    return frame
