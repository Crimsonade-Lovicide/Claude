"""Generated footage for every episode: B-roll sequences cut to the narration, and the existing
graphics (cards, rows, numbers) composited over moving, darkened footage instead of black.

    broll(prod, [("clip_a", 4.5), ("clip_b", 5.0), "clip_c"])   # the last clip takes the remainder
    over(broll_fn, graphic_fn)                                   # a graphic over darkened footage

Clips live in <prod>/anim/<name>.mp4 like the 3D clips. Every generated clip is tagged
ILLUSTRATIVE · AI-GENERATED on screen (FORMAT.md §2): it shows a place or an object, never a
person involved in the case, and is never passed off as archival.
"""

from PIL import Image, ImageFilter

import edit as E
import gfx as G

TAG = "ILLUSTRATIVE · AI-GENERATED"


def _grade(img, k=1.0):
    """The channel look on footage: slightly crushed, cooled, desaturated."""
    gray = img.convert("L").convert("RGB")
    img = Image.blend(img, gray, 0.22)
    r, g, b = img.split()
    b = b.point(lambda v: min(255, int(v * 1.04 + 3)))
    r = r.point(lambda v: int(v * 0.97))
    img = Image.merge("RGB", (r, g, b))
    return img.point(lambda v: int(max(0, v - 6) * 1.04 * k))


def clip_frame(prod, name, start=0.0, push=0.04):
    """One generated clip as a frame function, graded, with a slow digital push of its own."""
    clip = E.Clip(prod, name, start=start)

    def frame(t, dur):
        img = clip.frame(t, dur)
        z = 1.0 + push * (t / max(dur, 0.01))
        if z > 1.0:
            w, h = img.size
            cw, ch = int(w / z), int(h / z)
            img = img.crop(((w - cw) // 2, (h - ch) // 2, (w + cw) // 2, (h + ch) // 2)).resize((w, h), Image.LANCZOS)
        return _grade(img)
    return frame


def broll(prod, items, tag=TAG, fin=0.4, fout=0.4, xfade=0.35, overlay=None):
    """Cut a run of clips under the narration. items: names or (name, seconds); the last item takes
    whatever is left of the shot. Short dissolves between clips, grain and the honesty tag on top."""
    parts = [(it, None) if isinstance(it, str) else it for it in items]

    def frame(t, dur):
        acc, cur, nxt, local = 0.0, None, None, 0.0
        for i, (name, secs) in enumerate(parts):
            last = i == len(parts) - 1
            length = (dur - acc) if last else secs
            if t < acc + length or last:
                cur, local, seg = (name, i), t - acc, max(length, 0.01)
                if not last and length - local < xfade:
                    nxt = (parts[i + 1][0], i + 1)
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
        if tag:
            st = G.stamp(tag, 18)
            G.paste_alpha(img, st, (G.W - st.width - 60, 52), 0.8 * a)
        return G.finish(img, t)
    return frame


_CLIPS = {}


def _cached(prod, key):
    """Each (clip, position in the run) keeps its own reader so frames stream sequentially."""
    name, i = key
    k = (prod, name, i)
    if k not in _CLIPS:
        _CLIPS[k] = clip_frame(prod, name)
    return _CLIPS[k]


def over(footage, graphic, dim=0.38, blur=6, tag=TAG):
    """A graphic over footage. The footage is blurred and dimmed so type stays readable; the
    graphic's near-black ground drops out, so cards, rows and numbers sit on top. The honesty
    tag goes on last so the graphic never covers it."""
    def frame(t, dur):
        bg = footage(t, dur).filter(ImageFilter.GaussianBlur(blur)).point(lambda v: int(v * dim))
        fg = graphic(t, dur)
        img = Image.composite(fg, bg, fg.convert("L").point(lambda v: 255 if v > 40 else int(v * 6)))
        if tag:
            st = G.stamp(tag, 18)
            G.paste_alpha(img, st, (G.W - st.width - 60, 52), 0.8 * G.fade(t, dur, 0.4, 0.4))
        return img
    return frame
