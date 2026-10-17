"""Weight of Evidence score and sound effects, synthesized in numpy. No samples, no credits.

Every function returns a mono float32 array at SR. The edit (ep01.py) places cues per act,
ducks them under the narration, and drops effects on narration words.

Cues (each is a pure function of length and seed, so a re-run is identical):
  cue_open     low drone, slow heartbeat pulse, distant high tone        (cold open)
  cue_patient  warm pad, sparse piano-like notes                         (act I)
  cue_law      pad with a soft clock-tick pulse                          (act II)
  cue_tower    dark drone, wind-like noise, very sparse low notes        (act III)
  cue_science  soft plucked arpeggio over a pad                          (act IV)
  cue_verdict  pad that resolves from minor to major at the end          (act V)
Effects: hit, whoosh, card_drop, clink, typing, marker, hum.
"""

import numpy as np

SR = 48000
RNG = np.random.default_rng


def hz(midi):
    return 440.0 * 2 ** ((midi - 69) / 12)


def t_axis(sec):
    return np.arange(int(sec * SR)) / SR


def onepole_lp(x, cutoff):
    """Simple one-pole low-pass, vectorised enough for minutes of audio."""
    a = np.exp(-2 * np.pi * cutoff / SR)
    from scipy.signal import lfilter  # scipy ships with the venv; fall back below
    return lfilter([1 - a], [1, -a], x).astype(np.float32)


try:
    import scipy.signal  # noqa: F401
except Exception:  # pragma: no cover - fallback without scipy
    def onepole_lp(x, cutoff):  # noqa: F811
        a = np.exp(-2 * np.pi * cutoff / SR)
        y = np.empty_like(x)
        acc = 0.0
        for i, v in enumerate(x):
            acc = (1 - a) * v + a * acc
            y[i] = acc
        return y


def bandpass(x, lo, hi):
    return onepole_lp(x, hi) - onepole_lp(x, lo)


def reverb(x, seconds=3.0, wet=0.35, seed=1):
    """Convolution with exponentially decaying stereo-ish noise: a soft hall."""
    n = int(seconds * SR)
    r = RNG(seed)
    ir = r.normal(0, 1, n) * np.exp(-np.arange(n) / (SR * seconds / 6.5))
    ir = onepole_lp(ir.astype(np.float32), 5000)
    ir /= np.sqrt((ir ** 2).sum())
    from numpy.fft import irfft, rfft
    m = len(x) + n
    size = 1 << (m - 1).bit_length()
    y = irfft(rfft(x, size) * rfft(ir, size), size)[: len(x)]
    return ((1 - wet) * x + wet * y * 3).astype(np.float32)


def env_adsr(n, a=0.01, d=0.2, s=0.6, r=0.5):
    na, nd, nr = int(a * SR), int(d * SR), int(r * SR)
    ns = max(0, n - na - nd - nr)
    e = np.concatenate([np.linspace(0, 1, na, endpoint=False), np.linspace(1, s, nd, endpoint=False),
                        np.full(ns, s), np.linspace(s, 0, nr)])
    return e[:n] if len(e) >= n else np.pad(e, (0, n - len(e)))


def pad_voice(freq, sec, detune=0.12, bright=900, seed=0):
    t = t_axis(sec)
    r = RNG(seed)
    y = np.zeros_like(t)
    for k in range(3):  # three detuned saw-ish voices built from a few partials
        f = freq * (1 + (k - 1) * detune / 100)
        ph = r.uniform(0, 2 * np.pi)
        for h in range(1, 7):
            y += np.sin(2 * np.pi * f * h * t + ph * h) / h
    y = onepole_lp(y.astype(np.float32), bright)
    lfo = 0.75 + 0.25 * np.sin(2 * np.pi * 0.07 * t + r.uniform(0, 6))
    return y * lfo / 6


def chord_pad(chords, sec, bright=900, seed=0, vol=0.18):
    """chords: list of lists of MIDI notes; each held for sec/len(chords) with crossfades."""
    seg = sec / len(chords)
    out = np.zeros(int(sec * SR), np.float32)
    for i, ch in enumerate(chords):
        start = int(i * seg * SR)
        length = int(min(seg + 3.0, sec - i * seg) * SR)
        part = np.zeros(length, np.float32)
        for j, m in enumerate(ch):
            v = pad_voice(hz(m), length / SR, bright=bright, seed=seed + 31 * i + j)[:length]
            part[:len(v)] += v  # length/SR can round to one sample short
        e = env_adsr(length, a=2.5, d=0.5, s=1.0, r=3.0)
        out[start:start + length] += (part * e)[: len(out) - start]
    return out * vol


def piano_note(freq, sec=4.0, vel=0.5):
    t = t_axis(sec)
    y = np.zeros_like(t)
    for h, amp in enumerate([1, 0.45, 0.22, 0.12, 0.06], start=1):
        inharm = 1 + 0.0004 * h * h
        y += amp * np.sin(2 * np.pi * freq * h * inharm * t) * np.exp(-t * (1.2 + 0.9 * h))
    y *= np.minimum(1, t / 0.004)
    return (y * vel / 1.8).astype(np.float32)


def place(buf, x, at):
    i = int(at * SR)
    if i >= len(buf):
        return buf
    j = min(len(buf), i + len(x))
    buf[i:j] += x[: j - i]
    return buf


def heartbeat(sec, bpm=56, vol=0.22):
    out = np.zeros(int(sec * SR), np.float32)
    beat = 60 / bpm
    t = t_axis(0.35)
    thump = np.sin(2 * np.pi * (55 - 25 * t) * t) * np.exp(-t * 14)
    k = 0.0
    while k < sec:
        place(out, thump * vol, k)
        place(out, thump * vol * 0.6, k + 0.28)
        k += beat
    return out


def noise_bed(sec, lo=200, hi=900, vol=0.05, seed=3):
    r = RNG(seed)
    n = r.normal(0, 1, int(sec * SR)).astype(np.float32)
    y = bandpass(n, lo, hi)
    t = t_axis(sec)
    swell = 0.6 + 0.4 * np.sin(2 * np.pi * 0.05 * t + 1.3)
    return y * swell * vol * 4


def fades(x, fin=3.0, fout=4.0):
    n = len(x)
    e = np.ones(n, np.float32)
    a, b = int(fin * SR), int(fout * SR)
    e[:a] = np.linspace(0, 1, a)
    e[n - b:] *= np.linspace(1, 0, b)
    return x * e


# D minor world: D2 = 38, D3 = 50, D4 = 62
def cue_open(sec, seed=11):
    drone = chord_pad([[38, 45, 50], [38, 46, 50], [38, 45, 50]], sec, bright=500, seed=seed, vol=0.22)
    hb = heartbeat(sec, 54, 0.20)
    high = pad_voice(hz(81), sec, bright=3000, seed=seed) * 0.025
    return fades(reverb(drone + hb + high, 3.5, 0.3, seed), 2, 3)


def sparse_piano(sec, scale, density, seed, vel=0.35, octave=0):
    r = RNG(seed)
    out = np.zeros(int(sec * SR), np.float32)
    t = r.uniform(1.0, 3.0)
    while t < sec - 2:
        m = r.choice(scale) + octave
        place(out, piano_note(hz(m), 5.0, vel * r.uniform(0.6, 1.0)), t)
        if r.random() < 0.3:  # occasional fifth below
            place(out, piano_note(hz(m - 7), 5.0, vel * 0.5), t + 0.02)
        t += r.exponential(1 / density) + 0.6
    return out


def cue_patient(sec, seed=21):
    pad = chord_pad([[50, 53, 57], [46, 50, 53], [41, 45, 48, 53], [43, 46, 50]], sec, bright=800, seed=seed, vol=0.16)
    pno = sparse_piano(sec, [62, 64, 65, 69, 72, 74], 0.22, seed, 0.30)
    return fades(reverb(pad + pno, 3.0, 0.38, seed))


def cue_law(sec, seed=31):
    pad = chord_pad([[50, 57, 62], [48, 55, 60], [46, 53, 58], [45, 52, 57]], sec, bright=700, seed=seed, vol=0.15)
    tick = np.zeros(int(sec * SR), np.float32)
    tt = t_axis(0.03)
    click = (np.sin(2 * np.pi * 2400 * tt) * np.exp(-tt * 300)).astype(np.float32)
    k = 0.0
    while k < sec:
        place(tick, click * (0.05 if int(k) % 2 else 0.035), k)
        k += 1.0
    pno = sparse_piano(sec, [57, 60, 62, 65], 0.12, seed, 0.22, octave=-12)
    return fades(reverb(pad + tick + pno, 2.5, 0.3, seed))


def cue_tower(sec, seed=41):
    drone = chord_pad([[38, 44, 50], [37, 44, 49]], sec, bright=400, seed=seed, vol=0.2)
    wind = noise_bed(sec, 300, 1400, 0.045, seed)
    low = sparse_piano(sec, [38, 41, 44], 0.07, seed, 0.35)
    return fades(reverb(drone + wind + low, 4.5, 0.4, seed), 3, 4)


def cue_science(sec, seed=51):
    pad = chord_pad([[50, 57, 64], [46, 53, 62], [48, 55, 64], [45, 52, 61]], sec, bright=1100, seed=seed, vol=0.13)
    arp = np.zeros(int(sec * SR), np.float32)
    notes = [62, 65, 69, 72, 69, 65]
    step = 60 / 96 / 2
    k, i = 0.5, 0
    t = t_axis(0.6)
    while k < sec:
        f = hz(notes[i % len(notes)] + (0 if (i // 24) % 2 == 0 else -2))
        pl = (np.sin(2 * np.pi * f * t) + 0.3 * np.sin(4 * np.pi * f * t)) * np.exp(-t * 9)
        place(arp, pl.astype(np.float32) * 0.06, k)
        k += step
        i += 1
    return fades(reverb(pad + arp, 2.5, 0.35, seed))


def cue_verdict(sec, seed=61):
    minor = chord_pad([[50, 53, 57], [46, 50, 53], [43, 46, 50], [45, 49, 52]], sec * 0.75, bright=800, seed=seed, vol=0.16)
    major = chord_pad([[50, 54, 57, 62]], sec * 0.25 + 3, bright=1200, seed=seed + 5, vol=0.16)
    out = np.zeros(int(sec * SR), np.float32)
    place(out, minor, 0)
    place(out, major, sec * 0.75 - 3)
    pno = sparse_piano(sec, [62, 65, 69, 74], 0.15, seed, 0.25)
    return fades(reverb(out + pno, 3.5, 0.38, seed), 2, 6)


# ---------------------------------------------------------------- effects

def hit(vol=0.9, seed=5):
    t = t_axis(4.0)
    boom = np.sin(2 * np.pi * (70 * np.exp(-t * 1.5) + 32) * t) * np.exp(-t * 1.4)
    n = RNG(seed).normal(0, 1, len(t)).astype(np.float32)
    crack = onepole_lp(n, 1800) * np.exp(-t * 18) * 0.5
    return reverb((boom + crack).astype(np.float32) * vol, 3.0, 0.3, seed)


def whoosh(sec=1.2, vol=0.35, seed=6):
    n = RNG(seed).normal(0, 1, int(sec * SR)).astype(np.float32)
    t = t_axis(sec)
    e = np.sin(np.pi * t / sec) ** 2
    lo = onepole_lp(n, 600) * (1 - t / sec)
    hi = (onepole_lp(n, 4000) - onepole_lp(n, 1200)) * (t / sec)
    return ((lo + hi) * e * vol * 3).astype(np.float32)


def card_drop(vol=0.5, seed=7):
    t = t_axis(0.5)
    n = RNG(seed).normal(0, 1, len(t)).astype(np.float32)
    slap = (onepole_lp(n, 5000) - onepole_lp(n, 700)) * np.exp(-t * 60)
    thump = np.sin(2 * np.pi * 110 * t) * np.exp(-t * 30) * 0.6
    return ((slap * 1.6 + thump) * vol).astype(np.float32)


def clink(vol=0.25, seed=8):
    t = t_axis(2.5)
    y = np.zeros_like(t)
    for ratio, amp, dec in [(1, 1, 3), (2.76, 0.6, 5), (5.4, 0.35, 8), (8.93, 0.2, 12)]:
        y += amp * np.sin(2 * np.pi * 1180 * ratio * t) * np.exp(-t * dec)
    return reverb((y * vol / 2).astype(np.float32), 1.5, 0.25, seed)


def typing(sec, rate=11, vol=0.18, seed=9):
    r = RNG(seed)
    out = np.zeros(int(sec * SR), np.float32)
    t = t_axis(0.04)
    k = 0.0
    while k < sec:
        n = r.normal(0, 1, len(t)).astype(np.float32)
        c = (onepole_lp(n, 6000) - onepole_lp(n, 1500)) * np.exp(-t * 180)
        thunk = np.sin(2 * np.pi * r.uniform(180, 260) * t) * np.exp(-t * 120) * 0.5
        place(out, (c + thunk) * vol * r.uniform(0.6, 1.0), k)
        k += r.exponential(1 / rate) + 0.03
    return out


def marker(sec=0.8, vol=0.12, seed=10):
    n = RNG(seed).normal(0, 1, int(sec * SR)).astype(np.float32)
    t = t_axis(sec)
    y = (onepole_lp(n, 5000) - onepole_lp(n, 2000)) * np.sin(np.pi * t / sec) ** 0.5
    return (y * vol * 2).astype(np.float32)


def hum(sec, vol=0.035):
    """Fluorescent hum: 120 Hz buzz with harmonics and a little flutter."""
    t = t_axis(sec)
    y = sum(np.sin(2 * np.pi * 120 * k * t) / k for k in (1, 2, 3, 5))
    y *= 0.85 + 0.15 * np.sin(2 * np.pi * 0.3 * t)
    return fades((y * vol).astype(np.float32), 0.5, 0.5)
