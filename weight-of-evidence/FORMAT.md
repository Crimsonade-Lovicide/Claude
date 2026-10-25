# Weight of Evidence: the locked format

**Reference episode: Case 02, The Safety Driver** (17:56, approved October 2026).
Every new case copies its structure, look and sound. `README.md` explains *why* the show
works this way; this file is the spec for *how* an episode is built. To change anything
here, change it on purpose: edit this file first, then the shared code, then re-check
the reference episode.

## 1. Running order

| Block | What happens | Length | Reference (Case 02) |
|---|---|---|---|
| Cold open | The moment, told in present tense, with a place/date lower third. Then the person harmed, the question, and the promise ("we'll weigh it and give a verdict"). | ~2:00 | S01–S08 |
| Title card | Series title over the Scale. Silent apart from one hit. | 6.5 s | S09 |
| Acts I–IV | Each opens on a silent act card (`I · THE MACHINE`), 3.4 s, with a whoosh. Each act ends on a **weight beat**: the Scale tips as that act's evidence lands, with a clink. | 2:30–5:30 each | S10–S53 |
| V · The verdict | Steelman each side on the Scale (`THE STRONGEST CASE: …`). Then one verdict card per party or sub-question (Case 02 had three). The Scale comes to rest, loaded. | ~3:00 | S54–S60 |
| Next case | Three stacked lines: `NEXT CASE` (red mono), `NAME · YEAR`, and the question in italics. | ~10 s | S61 |
| End card | 20 s, two video slots at (300,470) and (1020,470), 600×338. | 20 s | S62 |

- **Total runtime:** 17–19 min. **Narration:** about 2,800 words.
- **Chapters:** one per block above, named `<time/place hook>`, `I. …` to `V. The verdict`, then `Next case`. The first chapter is at 0:00.
- **Verdict cards:** always the same three parts on one graphic: **VERDICT** (one sentence, no hedging), **CONFIDENCE** (meter fills to a percentage that is read aloud), and **WHAT WOULD CHANGE OUR MIND** (specific evidence). The kicker above names the party (`THE SAFETY DRIVER`, `THE COMPANY`, …).

## 2. Look

All of this lives in `production/gfx.py`. Episodes don't override it.

- **Frame:** 1920×1080, 24 fps, film grain and vignette on every frame (`G.finish`).
- **Palette:**

  | Token | RGB | Use |
  |---|---|---|
  | `BG` | 8, 9, 12 | near-black ground |
  | `INK` | 234, 230, 220 | main text |
  | `DIM` / `FAINT` | 128,131,140 / 52,55,62 | secondary text / rules |
  | `PAPER` / `PAPER_INK` | 231,224,208 / 34,32,30 | evidence cards, documents |
  | `BRASS` | 201, 162, 92 | evidence, the Scale, `RECORD` |
  | `CYAN` | 96, 200, 214 | science, machines, data, `INFERENCE` |
  | `RED` | 214, 84, 64 | verdict kicker, `NEXT CASE`, warnings only |

- **Type** (IBM Plex + Courier Prime, OFL):
  - Plex Serif for claims and verdict sentences.
  - Plex Serif Italic for the question.
  - Plex Sans SemiBold for titles.
  - Plex Mono for labels, kickers, sources and lower thirds.
  - Courier Prime for typed documents.
- **Evidence cards:** paper card with a drop shadow. The claim is in serif, the source line in mono under a short rule, and a `RECORD` / `INFERENCE` / `ARGUMENT` stamp sits top right.
- **Honesty tags** (corner, mono, dim), each applied to every frame it covers:
  - `RECONSTRUCTION` for any rebuilt scene.
  - `RECONSTRUCTION FROM <SOURCE> DATA` when it's rebuilt from a report's figures.
  - `ILLUSTRATION · NOT DATA` for explanatory diagrams.
  - `ILLUSTRATIVE · NOT THE PATIENT'S SCAN` style tags for anything that could be mistaken for a record.
- **3D:**
  - Blender (Cycles), dark sets, a single key light, brass and cold accents only.
  - Rendered at 960×540 on every second frame, then Lanczos-upscaled and frame-blended to 24 fps.
  - The Scale (`scale_tip_left/right`, `scale_level_loaded`) is reused, never rebuilt.
  - People involved in the case are never depicted.
- **Generated footage** (`production/footage.py`; owner request, October 2026: the
  static-card cut was too slow). Prototype on Case 07's cold open (`ep07v2.py`); once
  it's approved it applies to every case.
  - Higgsfield text-to-video (Kling 3.0 Turbo, 1080p, 5 s) B-roll under the narration,
    a new clip about every 4–5 s, short dissolves, graded to the palette.
  - Places and objects only: buildings, rooms, documents, streets, weather. Never a
    person involved in the case, never faces (hands are fine), never legible fake
    dates or names. Reject any clip that breaks this.
  - Every generated frame carries `ILLUSTRATIVE · AI-GENERATED`. It is never passed off
    as archival.
  - Cards, rows and numbers sit over blurred, darkened footage (`F.over`) instead of black.
    Act cards, verdict cards, the title and the end card stay on black.
- **Motion:** slow pushes and eases (`G.ease`), no snap cuts inside a shot. Cards drop onto the word that introduces them (`ctx.at(shot, "phrase")`).

## 3. Sound

- **Narration:** ElevenLabs `eleven_multilingual_v2`, voice "Verdict – True Crime Narration" (`ZmqEPiBIr4itJeB29TyD`). One take per act, with no regenerations unless a line is wrong.
- **Score:** `production/score.py`, synthesized, one cue per block. The cue set: `cue_open`, `cue_science`, `cue_patient`, `cue_law`, `cue_tower`, `cue_verdict`. Reuse them and pick the cue by mood, not by topic.
- **Sound effects:** `hit` on the title, `whoosh` on act cards and on each verdict's confidence line, `card_drop` on evidence cards, `clink` on weight beats and steelman shots, `marker` on key phrases, `hum` under night or machine scenes, and `sea` (with `rough=1` for storms) under ocean scenes.
- **Mix:** narration at about −20 dBFS RMS. Music sits 13 dB under it and ducks about 5 dB under speech. The master is `loudnorm` to **−14 LUFS integrated, true peak ≤ −1 dBTP**. (Case 02: −14.6 LUFS, −1.2 dBTP.) The master measures the encoded AAC and lowers its limiter ceiling if the true peak lands above −1 dBTP; dense sound like sea wash can cost about 1 LU (Case 03 Short: −15.3 LUFS, −1.5 dBTP).

## 4. Deliverables per case

| File | Spec |
|---|---|
| `weight_of_evidence_caseNN.mp4` | H.264 CRF 21, max 16 Mbps, yuv420p, faststart, AAC 256k / 48 kHz |
| `.srt` | from the script text, timed to the aligned narration (not auto-captions) |
| `_chapters.txt` | pasted into the description |
| `thumb_a.jpg`, `thumb_b.jpg` | Cycles hero still + Pillow type; A/B in YouTube Test & Compare |
| `episodes/NN-slug/youtube.md` | 2 titles, description (content note, reconstruction note, chapters, sources), tags, pinned verdict comment |
| review copies | 720p, split at chapter breaks, for review in the Claude app |
| `weight_of_evidence_caseNN_short.mp4` | 1080×1920 Short cut from the cold open (`production/short02.py`): the episode's own narration and shots, reframed, with a place/date kicker, three-word captions and a "full episode" end card. Related video: the full episode |

Upload goes out as **Private** through the Make scenario "WEIGHT OF EVIDENCE · YouTube API (uploads)". After that, follow the checklist in `channel/setup.md` §10.

**Archive (owner's rule, Oct 2026):** every master, Short, caption file, chapter list, thumbnail
and `youtube.md` also goes to the owner's **AIE drive**, an external drive on their Mac, not
Google Drive. The production machine can't reach it, so files travel through a temporary Google
Drive transit folder: upload them one by one (no zip), the owner copies them across, and once
they confirm, trash the folder **and** the files in it. The files belong to the account the Make
scenario uploads as, so trashing the folder alone leaves them taking up storage.

## 5. Starting a new case

1. `episodes/NN-slug/research.md`: the claims table, where every number carries a source.
2. `episodes/NN-slug/script.md`: copy the Case 02 headings. Shot ids run S01…, and every shot has a picture note naming its tool (`3D:` / `GFX:`).
3. `production/epNN.py`: copy `ep02.py`, keep `CHAPTERS`, the silent cards, the verdict and end-card shots, `music()` and the `sfx()` patterns, then replace the case-specific shots.
4. Run `--stills` and check one frame per shot before running `--final`.
5. Check the master: loudness, captions, chapters and a contact sheet. Then send the 720p review parts.
