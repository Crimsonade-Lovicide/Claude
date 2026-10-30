# Weight of Evidence production pipeline

Everything on screen is built by code. ElevenLabs is used only for narration. There's no
image or video generation, no stock footage and no music licence.

| Step | Tool | Script |
|---|---|---|
| Narration text + pronunciation | script.md → JSON | `narration.py` |
| Narration audio | ElevenLabs `eleven_multilingual_v2`, voice "Verdict – True Crime Narration" (`ZmqEPiBIr4itJeB29TyD`), one take per act, `generations_count=1` | (MCP tool) |
| Word timings + per-shot clips | faster-whisper `base.en`, aligned to script words | `align.py` |
| 3D (the Scale, glass brain, tower, corridor) | Blender 5 as a Python module (`pip install bpy`), Cycles CPU + denoise | `scenes.py`, `render_ep01.sh` |
| Graphics, documents, map, charts | Pillow + numpy; map via geopandas/matplotlib (US Census boundaries, public domain) | `gfx.py`, `ep01.py` |
| Score + sound effects | synthesized in numpy (pads, piano-like notes, pulses, foley) | `score.py` |
| Edit, mix, captions, chapters | Pillow → ffmpeg; mix in numpy; `loudnorm` to −14 LUFS | `edit.py` |
| Trailer + 30 s vertical cut | same engine, Case 01 assets only | `trailer.py` |
| Thumbnails | Cycles hero still + Pillow type | `thumbs.py` |
| Channel art (profile picture, banner, watermark) | same Scale render + Pillow | `channel_art.py` |

Cost of Case 01 + trailer: about 16,600 ElevenLabs credits (≈ $3.00). Nothing else is paid.

## Run

```bash
python3.11 -m venv ~/.woeenv && ~/.woeenv/bin/pip install bpy faster-whisper geopandas matplotlib scipy pillow numpy
export WOE_PY=~/.woeenv/bin/python WOE_FONTS=<prod>/fonts   # IBM Plex + Courier Prime (OFL, google/fonts)
P=<prod>   # media dir outside git: vo_acts/, anim/, renders/, src/, fonts/

python narration.py ../episodes/01-the-tumor-defense/script.md $P/narration.json
#   record one ElevenLabs take per act → $P/vo_acts/act0.mp3 … act5.mp3
$WOE_PY align.py $P                       # vo/<shot>.wav, words.json, timing.json, align_report.txt
./render_ep01.sh $P                      # 3D clips → anim/*.mp4 (~3 h on 4 CPU cores)
$WOE_PY ep01.py $P --prepare              # Whitman brain still + map layers
$WOE_PY ep01.py $P --stills               # one review frame per shot → stills/
$WOE_PY ep01.py $P --final -j 2           # shots → mix → weight_of_evidence_case01.mp4 + .srt + chapters
$WOE_PY thumbs.py $P
$WOE_PY channel_art.py $P <out>          # avatar_800.png, banner_2048.jpg, watermark_150.png
# trailer: own prod dir with the trailer narration, anim/ linked to Case 01's
$WOE_PY trailer.py $T --final ; $WOE_PY trailer.py $T --final --vertical
```

## How the edit holds together

- A shot is `frame(t, dur) -> PIL.Image`. Durations come from the narration: lead-in +
  that shot's narration + a hold (`LEAD`, `PAD`), so re-recording a line re-times the cut.
- `ctx.at(shot, "phrase")` returns when the narrator says the phrase (from the aligned
  word timings). Highlights, card drops, map layers and sound effects all hang off it.
- 3D clips render at 960×540, every second frame, then ffmpeg upscales (Lanczos) and blends
  to 24 fps. The tumor fading in and out is a crossfade between two orbit passes
  (`brain_clean`, `brain_tumor`) on an identical camera path.
- A missing clip or still renders as a labelled placeholder, so the edit always builds.
- Every reconstruction carries a corner tag (`RECONSTRUCTION`, `ILLUSTRATION`,
  `ILLUSTRATIVE · NOT THE PATIENT'S SCAN`). Evidence cards carry `RECORD / INFERENCE /
  ARGUMENT`.
- Mix: narration to about −20 dBFS RMS; music placed 13 dB under and ducked about 5 dB
  under speech; effects peak-normalised and placed by word; master `loudnorm` −14 LUFS.
