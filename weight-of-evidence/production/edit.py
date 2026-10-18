"""Weight of Evidence edit engine: timing, 3D clip playback, shot rendering, mix, mux, captions.

A video module (ep01.py, trailer.py) defines:
  SILENT  {shot_id: seconds}         shots with no narration (titles, end card)
  PAD     {shot_id: seconds}         hold after the narration (default DEFAULT_PAD)
  LEAD    {shot_id: seconds}         lead-in before the narration (default DEFAULT_LEAD)
  FADE_IN / FADE_OUT {shot_id: s}    fades to and from black at act boundaries
  build(ctx) -> {shot_id: frame_fn}  frame_fn(t, dur) -> PIL image
  music(ctx) -> [(first_shot, last_shot, cue_fn, gain_db)]
  sfx(ctx)   -> [(shot_id, when, effect_array, gain_db)]   when: seconds or ctx.at(...)
  OUT_NAME, TITLE

Run:
  python <module>.py <prod_dir> --stills            one frame per shot -> stills/
  python <module>.py <prod_dir> --only S01,S02      render those shots
  python <module>.py <prod_dir> --final [-j 2]      all shots, mix, mux, captions, chapters
<prod_dir> holds narration.json, timing.json, words.json, vo/<id>.wav (from align.py),
anim/<clip>.mp4 (from render_ep01.sh), renders/ (stills), fonts/.
"""

import json
import os
import re
import subprocess
import sys
from multiprocessing import Pool

import numpy as np
from PIL import Image, ImageFilter

import gfx as G
import score as S

DEFAULT_LEAD = 0.25
DEFAULT_PAD = 0.6


def norm(w):
    return re.sub(r"[^a-z0-9']", "", w.lower().replace("’", "'"))


class Ctx:
    """Shot timing for one video. Times returned by at() are relative to the shot start."""

    def __init__(self, prod, mod):
        self.prod = prod
        self.mod = mod
        self.nar = json.load(open(os.path.join(prod, "narration.json")))
        tpath = os.path.join(prod, "timing.json")
        self.vo_dur = json.load(open(tpath)) if os.path.exists(tpath) else {}
        wpath = os.path.join(prod, "words.json")
        self.words = json.load(open(wpath)) if os.path.exists(wpath) else {}
        self.text = {s["id"]: s["text"] for s in self.nar["shots"]}
        prefix = getattr(mod, "SHOT_PREFIX", "")
        self.order = [s["id"] for s in self.nar["shots"] if s["id"].startswith(prefix)]
        self.dur, self.start = {}, {}
        acc = 0.0
        for sid in self.order:
            self.start[sid] = acc
            self.dur[sid] = self.duration(sid)
            acc += self.dur[sid]
        self.total = acc

    def lead(self, sid):
        return 0.0 if sid in self.mod.SILENT else self.mod.LEAD.get(sid, DEFAULT_LEAD)

    def duration(self, sid):
        if sid in self.mod.SILENT:
            return self.mod.SILENT[sid]
        vo = self.vo_dur.get(sid)
        if vo is None:  # no take yet: estimate from text at 155 wpm
            vo = len(self.text.get(sid, "").split()) / 155 * 60 + 0.5
        return self.lead(sid) + vo + self.mod.PAD.get(sid, DEFAULT_PAD)

    def at(self, sid, phrase, offset=0.0, end=False):
        """When the narrator says phrase in shot sid (start of its first word, or the end of
        its last word with end=True), relative to the shot start."""
        toks = [norm(w) for w in phrase.split() if norm(w)]
        ws = self.words.get(sid, [])
        hw = [norm(w[0]) for w in ws]
        for i in range(len(hw) - len(toks) + 1):
            if hw[i:i + len(toks)] == toks:
                t = ws[i + len(toks) - 1][2] if end else ws[i][1]
                return self.lead(sid) + t + offset
        txt = self.text.get(sid, "")
        k = txt.lower().find(phrase.lower())
        frac = (k / max(1, len(txt))) if k >= 0 else 0.5
        vo = self.dur[sid] - self.lead(sid) - self.mod.PAD.get(sid, DEFAULT_PAD)
        return self.lead(sid) + frac * vo + offset


# ---------------------------------------------------------------- 3D clips

class Clip:
    """Sequential reader for a rendered clip, trimmed/retimed by ffmpeg to the shot length.
    Holds the last frame if the clip runs out; a labelled placeholder if it's missing."""

    def __init__(self, prod, name, start=0.0, speed=1.0, reverse=False, length=None):
        self.path = os.path.join(prod, "anim", f"{name}.mp4")
        self.name, self.start, self.speed, self.reverse, self.length = name, start, speed, reverse, length
        self.proc, self.last, self.i = None, None, -1

    def _open(self, dur):
        if not os.path.exists(self.path):
            return
        span = dur * self.speed + 0.5 if self.length is None else self.length
        vf = f"trim=start={self.start}:duration={span},setpts=(PTS-STARTPTS)/{self.speed},fps={G.FPS}"
        if self.reverse:
            vf += ",reverse"
        vf += f",scale={G.W}:{G.H}"
        self.proc = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-i", self.path, "-vf", vf,
                                      "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                                     stdout=subprocess.PIPE)

    def frame(self, t, dur):
        idx = int(round(t * G.FPS))
        if self.i < 0:
            self._open(dur)
        if self.proc is None:
            img = G.canvas((20, 22, 26))
            G.centered(img, G.text_layer(f"[{self.name}]", G.MONO(30), fill=G.DIM), G.H // 2)
            return img
        while self.i < idx:
            buf = self.proc.stdout.read(G.W * G.H * 3)
            self.i += 1
            if len(buf) < G.W * G.H * 3:
                break
            self.last = Image.frombuffer("RGB", (G.W, G.H), buf)
        return self.last.copy() if self.last is not None else G.canvas()


def clip_shot(clip, tag="RECONSTRUCTION", overlay=None, fin=0.4, fout=0.4, darken=1.0,
              grade=None):
    """A 3D clip as a shot, with the evidence tag, an optional overlay(img, t, dur) and fades."""
    def frame(t, dur):
        img = clip.frame(t, dur)
        if grade:
            img = grade(img)
        a = G.fade(t, dur, fin, fout) * darken
        if a < 1:
            img = Image.blend(G.canvas(), img, max(0.0, a))
        if overlay:
            overlay(img, t, dur)
        if tag:
            G.recon_tag(img, G.fade(t, dur, 0.6, 0.4), tag)
        return G.finish(img, t, grain=True, vignette=False)
    return frame


def tumor_glow(with_tumor, without, strength=1.6):
    """The two brain passes share a camera, so their difference is the tumor alone. Use it
    as a mask: warm the core and add a soft orange bloom around it."""
    ta = np.asarray(with_tumor.resize((480, 270), Image.BILINEAR)).astype(np.float32)
    tb = np.asarray(without.resize((480, 270), Image.BILINEAR)).astype(np.float32)
    m = np.clip((np.abs(ta - tb).sum(-1) - 18) / 120, 0, 1)
    core = Image.fromarray((m * 255).astype(np.uint8))
    bloom = core.filter(ImageFilter.GaussianBlur(10))
    core = core.resize((G.W, G.H), Image.BILINEAR)
    bloom = bloom.resize((G.W, G.H), Image.BILINEAR)
    c = np.asarray(core).astype(np.float32)[..., None] / 255
    bl = np.asarray(bloom).astype(np.float32)[..., None] / 255
    base = np.asarray(with_tumor).astype(np.float32)
    warm = np.array([255, 105, 35], np.float32)
    c = np.clip(c * 1.6, 0, 1)
    shade = 0.55 + 0.45 * (base.mean(-1, keepdims=True) / 255)  # keep the glass texture
    out = base * (1 - 0.92 * c) + warm * shade * 0.92 * c + warm * bl * 0.55 * strength
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))


def xfade_shot(a, b, at, length=0.8, tag="ILLUSTRATION", overlay=None, hard=False, glow=None):
    """Clip a, then clip b from time `at` (same camera path, so it reads as one shot).
    glow="a" or "b" names the pass that contains the tumor; it gets tumor_glow()."""
    def frame(t, dur):
        fa, fb = a.frame(t, dur), b.frame(t, dur)
        if glow == "a":
            fa = tumor_glow(fa, fb)
        elif glow == "b":
            fb = tumor_glow(fb, fa)
        k = (1.0 if t >= at else 0.0) if hard else G.ease((t - at) / length)
        img = Image.blend(fa, fb, k) if 0 < k < 1 else (fb if k >= 1 else fa)
        f = G.fade(t, dur, 0.4, 0.4)
        if f < 1:
            img = Image.blend(G.canvas(), img, f)
        if overlay:
            overlay(img, t, dur)
        if tag:
            G.recon_tag(img, G.fade(t, dur, 0.6, 0.4), tag)
        return G.finish(img, t, grain=True, vignette=False)
    return frame


# ---------------------------------------------------------------- rendering

def _render_one(args):
    modname, prod, sid, stills = args
    mod = __import__(modname)
    ctx = Ctx(prod, mod)
    fn = mod.build(ctx)[sid]
    dur = ctx.dur[sid]
    fi, fo = mod.FADE_IN.get(sid, 0), mod.FADE_OUT.get(sid, 0)

    def framed(t, d):
        img = fn(t, d)
        k = min(G.clamp(t / fi) if fi else 1.0, G.clamp((d - t) / fo) if fo else 1.0)
        return img if k >= 1 else Image.blend(Image.new("RGB", img.size), img, k)
    if stills:
        os.makedirs(os.path.join(prod, "stills"), exist_ok=True)
        t = min(dur * 0.6, dur - 0.1)
        framed(t, dur).save(os.path.join(prod, "stills", f"{sid}.jpg"), quality=88)
        return sid
    os.makedirs(os.path.join(prod, "shots"), exist_ok=True)
    G.render(framed, dur, os.path.join(prod, "shots", f"{sid}.mp4"))
    return sid


def render_shots(modname, prod, ids, stills=False, jobs=1):
    work = [(modname, prod, sid, stills) for sid in ids]
    if jobs > 1:
        with Pool(jobs) as p:
            for sid in p.imap_unordered(_render_one, work):
                print("shot", sid, flush=True)
    else:
        for w in work:
            print("shot", _render_one(w), flush=True)


# ---------------------------------------------------------------- audio

def load_wav(path):
    out = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", path, "-f", "f32le", "-ac", "1",
                          "-ar", str(S.SR), "-"], capture_output=True, check=True).stdout
    return np.frombuffer(out, np.float32).copy()


def rms_db(x):
    return 20 * np.log10(np.sqrt(np.mean(x.astype(np.float64) ** 2)) + 1e-9)


def gain(x, db):
    return x * (10 ** (db / 20))


def envelope(x, attack=0.03, release=0.6, win=0.05):
    """Smoothed RMS envelope of x (0..1-ish), for ducking."""
    n = int(win * S.SR)
    sq = np.convolve(x ** 2, np.ones(n) / n, mode="same")
    e = np.sqrt(sq)
    a, r = np.exp(-1 / (attack * S.SR / 64)), np.exp(-1 / (release * S.SR / 64))
    ds = e[::64]
    out = np.empty_like(ds)
    acc = 0.0
    for i, v in enumerate(ds):
        acc = a * acc + (1 - a) * v if v > acc else r * acc + (1 - r) * v
        out[i] = acc
    return np.interp(np.arange(len(x)), np.arange(len(out)) * 64, out)


def mix(ctx, mod):
    n = int((ctx.total + 1) * S.SR)
    vo = np.zeros(n, np.float32)
    for sid in ctx.order:
        p = os.path.join(ctx.prod, "vo", f"{sid}.wav")
        if sid in mod.SILENT or not os.path.exists(p):
            continue
        S.place(vo, load_wav(p), ctx.start[sid] + ctx.lead(sid))
    vo = gain(vo, -20 - rms_db(vo[np.abs(vo) > 1e-4]))  # speech near -20 dBFS RMS
    music = np.zeros(n, np.float32)
    for first, last, cue, db in mod.music(ctx):
        t0 = ctx.start[first]
        t1 = ctx.start[last] + ctx.dur[last]
        x = cue(t1 - t0 + 2.0)
        x = gain(x, -33 - rms_db(x) + db)  # 13 dB under the voice before ducking
        S.place(music, x[: int((t1 - t0 + 2.0) * S.SR)], t0)
    duck = envelope(vo)
    duck = 1 - 0.45 * np.clip(duck / (duck.max() + 1e-9) * 3, 0, 1)  # up to ~5 dB under speech
    music *= duck.astype(np.float32)
    fx = np.zeros(n, np.float32)
    for sid, when, x, db in mod.sfx(ctx):
        S.place(fx, gain(x / (np.abs(x).max() + 1e-9) * 0.5, db), ctx.start[sid] + when)
    out = vo + music + fx
    out /= max(1.0, np.abs(out).max() / 0.98)
    path = os.path.join(ctx.prod, "mix_" + mod.OUT_NAME.replace(".mp4", ".wav"))
    import wave
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(S.SR)
        w.writeframes((out * 32767).astype(np.int16).tobytes())
    print(f"mix: voice {rms_db(vo):.1f} dB RMS, music {rms_db(music):.1f}, fx peak {np.abs(fx).max():.2f}")
    return path


# ---------------------------------------------------------------- captions and chapters

def srt_time(t):
    h, m = int(t // 3600), int(t % 3600 // 60)
    s = t % 60
    return f"{h:02d}:{m:02d}:{int(s):02d},{int(round((s % 1) * 1000)):03d}"


def captions(ctx, mod, path):
    """Script text (not recogniser text), chunked to two short lines, timed by word index."""
    cues = []
    for sid in ctx.order:
        if sid in mod.SILENT:
            continue
        words = ctx.text[sid].split()
        ws = ctx.words.get(sid, [])
        if not words or not ws:
            continue
        base = ctx.start[sid] + ctx.lead(sid)
        chunks, cur = [], []
        for w in words:
            cur.append(w)
            if len(" ".join(cur)) > 64 or w.endswith((".", "?", "!")) and len(" ".join(cur)) > 18:
                chunks.append(cur)
                cur = []
        if cur:
            chunks.append(cur)
        i = 0
        for ch in chunks:
            j = i + len(ch)
            a = ws[min(len(ws) - 1, round(i * len(ws) / len(words)))][1]
            b = ws[min(len(ws) - 1, round((j - 1) * len(ws) / len(words)))][2]
            line = " ".join(ch)
            if len(line) > 38:  # split into two lines near the middle
                mid = len(line) // 2
                cut = line.rfind(" ", 0, mid + 6)
                line = line[:cut] + "\n" + line[cut + 1:]
            cues.append([base + a, base + b + 0.15, line])
            i = j
    for c, nxt in zip(cues, cues[1:]):  # never overlap the next cue
        c[1] = min(c[1], nxt[0] - 0.02)
    out = [f"{k}\n{srt_time(a)} --> {srt_time(b)}\n{line}\n" for k, (a, b, line) in enumerate(cues, 1)]
    open(path, "w").write("\n".join(out))


def chapters(ctx, mod, path):
    lines = []
    for sid, title in mod.CHAPTERS:
        t = int(ctx.start[sid])
        lines.append(f"{t // 60}:{t % 60:02d} {title}")
    open(path, "w").write("\n".join(lines) + "\n")


# ---------------------------------------------------------------- final

# Gentle bus compression and a limiter tame the effect hits so normalisation can reach target.
MASTER_PRE = "acompressor=threshold=-20dB:ratio=2.5:attack=8:release=250:makeup=2,alimiter=limit=0.7:attack=3:release=60"


def loudnorm_filter(audio, target=-14.0, ceiling_db=-1.5):
    """Measure the integrated loudness after MASTER_PRE, then apply the exact gain to reach
    target and catch the peaks with a final limiter at the ceiling. The limiter runs at 4x
    the sample rate so it also catches inter-sample (true) peaks, which AAC would otherwise
    push past -1 dBTP on broadband sounds like sea wash."""
    out = subprocess.run(["ffmpeg", "-hide_banner", "-i", audio, "-af",
                          f"{MASTER_PRE},loudnorm=print_format=json", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    m = json.loads(out[out.rindex("{"):out.rindex("}") + 1])
    gain_db = target - float(m["input_i"])
    limit = 10 ** (ceiling_db / 20)
    return (f"{MASTER_PRE},volume={gain_db:.2f}dB,aresample=192000,"
            f"alimiter=limit={limit:.3f}:attack=2:release=50:level=false,aresample=48000")


def true_peak(path):
    """True peak (dBTP) of a file's audio, as ffmpeg's ebur128 measures it."""
    err = subprocess.run(["ffmpeg", "-nostats", "-i", path, "-af", "ebur128=peak=true", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    return float(err[err.rindex("True peak:"):].split("Peak:")[1].split()[0])


def master_audio(audio, out):
    """Loudness-normalised AAC. AAC can overshoot the limiter by a dB or more on dense sounds
    (sea wash), so measure the encoded file and lower the ceiling until it holds -1 dBTP."""
    for ceiling in (-1.5, -2.5, -3.5):
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", audio, "-af", loudnorm_filter(audio, ceiling_db=ceiling),
                        "-ar", "48000", "-c:a", "aac", "-b:a", "256k", out], check=True)
        tp = true_peak(out)
        print(f"master: ceiling {ceiling} dB -> true peak {tp} dBTP", flush=True)
        if tp <= -1.0:
            break
    return out


def final(ctx, mod, jobs, render=True):
    if render:
        render_shots(mod.__name__, ctx.prod, ctx.order, jobs=jobs)
    tag = "_" + mod.OUT_NAME.replace(".mp4", "")
    lst = os.path.join(ctx.prod, f"shots{tag}.txt")
    open(lst, "w").write("".join(f"file 'shots/{sid}.mp4'\n" for sid in ctx.order))
    video = os.path.join(ctx.prod, f"video{tag}.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst,
                    "-c", "copy", video], check=True, cwd=ctx.prod)
    audio = mix(ctx, mod)
    out = os.path.join(ctx.prod, mod.OUT_NAME)
    aac = master_audio(audio, os.path.join(ctx.prod, f"master{tag}.m4a"))
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", video, "-i", aac, "-map", "0:v", "-map", "1:a",
                    # delivery encode: grain makes the CRF 18 intermediates ~30 Mbps; cap for upload
                    "-c:v", "libx264", "-preset", "medium", "-crf", "21", "-maxrate", "16M",
                    "-bufsize", "32M", "-pix_fmt", "yuv420p", "-movflags", "+faststart",
                    "-c:a", "copy", "-shortest",
                    "-metadata", f"title={mod.TITLE}", out], check=True)
    captions(ctx, mod, out.replace(".mp4", ".srt"))
    if getattr(mod, "CHAPTERS", None):
        chapters(ctx, mod, out.replace(".mp4", "_chapters.txt"))
    print("wrote", out, f"{ctx.total / 60:.1f} min")


def main(mod):
    prod = sys.argv[1]
    os.environ.setdefault("WOE_FONTS", os.path.join(prod, "fonts"))
    G.FONT_DIR = os.environ["WOE_FONTS"]
    ctx = Ctx(prod, mod)
    argv = sys.argv[2:]
    jobs = int(argv[argv.index("-j") + 1]) if "-j" in argv else 1
    if "--only" in argv:
        ids = argv[argv.index("--only") + 1].split(",")
        render_shots(mod.__name__, prod, ids, stills="--stills" in argv, jobs=jobs)
    elif "--stills" in argv:
        render_shots(mod.__name__, prod, ctx.order, stills=True, jobs=jobs)
    elif "--mix" in argv:
        mix(ctx, mod)
    elif "--final" in argv:
        final(ctx, mod, jobs)
    elif "--remux" in argv:  # shots already rendered: concat, mix, mux only
        final(ctx, mod, jobs, render=False)
    print(f"total {ctx.total / 60:.2f} min")
