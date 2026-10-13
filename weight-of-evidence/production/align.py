"""Word timings and per-shot narration clips from act-length takes.

    python align.py <prod_dir>

<prod_dir> holds narration.json (from narration.py) and vo_acts/act<N>.mp3, one take per
act in narration.json order. Writes:
  words.json      {shot_id: [[word, start, end], ...]}  (times relative to the shot clip)
  vo/<shot>.wav   the shot's narration, cut at the middle of the pause between shots
  timing.json     {shot_id: duration_seconds}
  align_report.txt  words the recogniser heard differently from the script (for a listen)
Needs faster-whisper. Re-run whenever a take changes.
"""

import difflib
import json
import os
import re
import subprocess
import sys

from faster_whisper import WhisperModel


def norm(w):
    return re.sub(r"[^a-z0-9']", "", w.lower().replace("’", "'"))


def main(prod):
    nar = json.load(open(os.path.join(prod, "narration.json")))
    model = WhisperModel("base.en", device="cpu", compute_type="int8", cpu_threads=2)
    os.makedirs(os.path.join(prod, "vo"), exist_ok=True)
    words_out, timing, report = {}, {}, []
    for ai, act in enumerate(nar["acts"]):
        src = os.path.join(prod, "vo_acts", f"act{ai}.mp3")
        if not os.path.exists(src):  # take not recorded yet: the edit estimates these shots
            print(f"act{ai}: no take, skipped", flush=True)
            continue
        segs, info = model.transcribe(src, word_timestamps=True, beam_size=5)
        heard = [(w.word.strip(), w.start, w.end) for s in segs for w in s.words]
        total = info.duration
        shots = [s for s in nar["shots"] if s["id"] in act["ids"]]
        script_words, owner = [], []
        for s in shots:
            for w in s["spoken"].split():
                if norm(w):
                    script_words.append(norm(w))
                    owner.append(s["id"])
        hw = [norm(h[0]) for h in heard]
        sm = difflib.SequenceMatcher(a=script_words, b=hw, autojunk=False)
        # map each script word to a heard word index where they match
        mapped = [None] * len(script_words)
        for blk in sm.get_matching_blocks():
            for k in range(blk.size):
                mapped[blk.a + k] = blk.b + k
        for op, a0, a1, b0, b1 in sm.get_opcodes():
            if op != "equal":
                report.append(f"act{ai} {op}: script '{' '.join(script_words[a0:a1])}' / heard '{' '.join(hw[b0:b1])}'")
        # first and last heard index per shot
        span = {}
        for i, sid in enumerate(owner):
            if mapped[i] is None:
                continue
            lo, hi = span.get(sid, (mapped[i], mapped[i]))
            span[sid] = (min(lo, mapped[i]), max(hi, mapped[i]))
        ids = [s["id"] for s in shots]
        starts, ends = [], []
        for sid in ids:
            lo, hi = span[sid]
            starts.append(heard[lo][1])
            ends.append(heard[hi][2])
        # cut points: middle of the gap between one shot's last word and the next shot's first
        cuts = [0.0]
        for k in range(1, len(ids)):
            cuts.append(round((ends[k - 1] + starts[k]) / 2, 3))
        cuts.append(total)
        for k, sid in enumerate(ids):
            t0, t1 = cuts[k], cuts[k + 1]
            out = os.path.join(prod, "vo", f"{sid}.wav")
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-ss", f"{t0:.3f}",
                            "-to", f"{t1:.3f}", "-ar", "48000", "-ac", "1", out], check=True)
            lo, hi = span[sid]
            words_out[sid] = [[heard[j][0], round(heard[j][1] - t0, 3), round(heard[j][2] - t0, 3)]
                              for j in range(lo, hi + 1)]
            timing[sid] = round(t1 - t0, 3)
        print(f"act{ai}: {len(ids)} shots, {total:.1f}s", flush=True)
    json.dump(words_out, open(os.path.join(prod, "words.json"), "w"), indent=0)
    json.dump(timing, open(os.path.join(prod, "timing.json"), "w"), indent=1)
    open(os.path.join(prod, "align_report.txt"), "w").write("\n".join(report) + "\n")
    print(f"{len(report)} differences -> align_report.txt")


if __name__ == "__main__":
    main(sys.argv[1])
