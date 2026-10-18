# WEIGHT OF EVIDENCE

A faceless documentary series on YouTube. Each episode takes one hard question, anchored
in one real case, follows the evidence, and ends with a verdict and a stated confidence.

The name is a standard from law and science: the weight of evidence is how much the
evidence counts once it's in, which is what every episode measures before it rules. It
appears only in the title card, the end card, the trailer and the channel art. (Working
title until October 2026: Open Verdict, dropped after two unrelated channels launched
under it.)

**The format and look are locked to Case 02. The spec is in [`FORMAT.md`](FORMAT.md).**

## The promise (one sentence)

> One question nobody has settled. We weigh the evidence. Then we commit to a verdict
> and tell you how sure we are.

## Format rules

1. **One case anchors the question.** Abstract dilemmas only come in after the audience
   cares about a real person.
2. **Steelman before verdict.** Before we rule, each side gets its strongest form, stated
   the way its best defender would put it.
3. **The verdict has three parts**, always in this order, always on the same graphic:
   - **VERDICT:** one sentence, no hedging.
   - **CONFIDENCE:** a percentage, read aloud.
   - **WHAT WOULD CHANGE OUR MIND:** the specific evidence that would flip it.
4. **The case stays open.** If new evidence or a strong viewer argument moves us, we say
   so in a pinned comment or a follow-up video and change the number. New weight on the
   scale moves the verdict.
5. **Evidence labels on screen.** Every claim card carries one of:
   - `RECORD`: in a primary source (court record, paper, official report)
   - `INFERENCE`: our reasoning from the record
   - `ARGUMENT`: a position someone holds (credited by name)
   Any reconstruction (3D scene, recreated document, illustrative scan) carries a small
   `RECONSTRUCTION` tag. We never present a reconstruction as an original.
6. **Victims are people, not plot.** Name them where the record does. Don't linger on
   perpetrators' faces or names. No graphic description of violence.
7. **No hero host.** The narrator is "we," which means the show, not a personality.

## Recurring visual devices

- **The Scale.** A brass balance in an empty black space, built and rendered in Blender.
  Evidence cards drop onto either pan as the episode goes, and the beam tips. It's the
  show's signature shot and the thumbnail motif.
- **The Verdict Meter.** A horizontal bar from 0 to 100% that fills to the confidence
  number at the verdict. Pillow motion graphic.
- **Evidence cards.** Paper cards, typewriter header, the `RECORD / INFERENCE / ARGUMENT`
  stamp in the corner. Pillow.
- **Palette.** Near-black background; paper cream for documents; one warm accent (brass)
  for evidence; one cold accent (clinical cyan) for the brain and medicine.

## Production: programmatic, minimal paid generation

| Need | Tool | Paid generation? |
|---|---|---|
| Narration | ElevenLabs, one voice and one model per episode | Yes (the only one) |
| 3D (brain, the Scale, the tower, corridors) | Blender 5 Python (bpy) + Cycles; Unreal 5 optional for hero shots | No |
| Motion graphics, documents, maps, charts | Python: Pillow, numpy, matplotlib, geopandas, ffmpeg | No |
| Word timing for cuts | faster-whisper (local) | No |
| Edit, mix, captions, chapters | Python + ffmpeg (same approach as the UNBUILT pipeline) | No |
| Music | Licensed library (Epidemic Sound subscription) or numpy-synthesized ambient drones | No per-use credits |
| Sound effects | Licensed library or synthesized (clicks, room tone, heartbeat, paper) | No per-use credits |
| Illustration B-roll | None. Replaced by 3D and typographic scenes. | No |

Higgsfield is not part of the plan. If a shot can't be made programmatically, rewrite the
shot.

## Episodes

| # | Question | Status |
|---|---|---|
| 01 | If a tumor made him do it, is he guilty? | Produced: 19:05, captions, chapters, thumbnails |
| 02 | Who's guilty when the car drives itself? (Tempe, 2018) | Produced: 17:56, captions, chapters, thumbnails. **Format reference** (see `FORMAT.md`). Uploaded private 17 Oct 2026 (`6GP6-C2GuJE`) |
| 03 | Is killing to survive murder? (The Mignonette, 1884) | Research and script drafted; verdicts awaiting sign-off |
| 04 | Should surgeons use the Pernkopf Atlas? | Planned |
