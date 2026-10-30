# Weight of Evidence: instructions for Claude

The format and look are **locked** to Case 02 (The Safety Driver). Before writing a
script, building shots or changing the shared code, read `FORMAT.md`. It is the spec.
`README.md` covers the editorial rules, and `production/README.md` covers the pipeline.

- New episodes copy `production/ep02.py` and the Case 02 script structure. Keep the
  running order, the act and verdict cards, the end card, the palette, the type, the
  Scale, the honesty tags, the voice and the mix targets.
- Visual changes go in the shared kit (`gfx.py`, `edit.py`, `score.py`, `scenes.py`) so
  they apply to every episode. Never override the look inside one episode.
- If the owner asks for a change to the format, update `FORMAT.md` in the same commit.
- Media lives outside git, in the production directory (`$P`). Commit code, scripts and
  the small deliverables (captions, chapters, thumbnails) only.
