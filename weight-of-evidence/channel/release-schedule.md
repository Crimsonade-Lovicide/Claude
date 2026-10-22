# Release schedule (draft, 22 Oct 2026, for the owner to confirm)

Every episode is uploaded **private**. This schedule puts them out one a week. The order is fixed
because each episode's closing teaser names the next case: 01 → 02 → 03 → 04 → 05 → 06.

## The proposal

**One episode a week, Thursdays at 12:00 US Eastern** (9:00 Pacific; 17:00 UK, or 16:00 on
29 October, when the UK has changed its clocks and the US hasn't yet). The Short follows
on the **Sunday after**, with its Related video set to that week's episode, so each Short sends
viewers to an episode that is already live.

The day and time are an assumption, not a finding. Most of the cases are American, so the
audience is likely to be mostly in the US, and midday Eastern lands in the US morning and the UK
evening. Consistency matters more than the exact slot. After four episodes, YouTube Analytics
("When your viewers are on YouTube") shows the real best time, and we move to it.

| Week | Episode (public, Thu 12:00 ET) | Short (Sun 12:00 ET) | Studio steps done by |
|---|---|---|---|
| Thu 29 Oct | Trailer `eAZXxwX4b2E` + **Case 01** `FC6vrd1cB0o` | Sun 1 Nov · `T5RjIL720gw` | Tue 27 Oct |
| Thu 5 Nov | **Case 02** `6GP6-C2GuJE` | Sun 8 Nov · `glkhjcQDBig` | Tue 3 Nov |
| Thu 12 Nov | **Case 03** `QiPVYrdDzRw` | Sun 15 Nov · `Mj4jkA1-T7s` | Tue 10 Nov |
| Thu 19 Nov | **Case 04** `rF4oExXmaX0` | Sun 22 Nov · `VzoS6sqcGPc` | Tue 17 Nov |
| **Wed** 25 Nov | **Case 05** (after sign-off and upload) | Sun 29 Nov | Mon 23 Nov |
| Thu 3 Dec | **Case 06**, the Central Park Five (in research) | Sun 6 Dec | Tue 1 Dec |

- **Case 05 moves to Wednesday** because Thursday 26 November is Thanksgiving in the US. The
  alternative is Thursday 3 December, with everything after it shifting a week.
- **Case 06 must be produced by about 26 November** for 3 December. Research started 22 October.
  A script for your sign-off by about 28 October leaves ample time.
- **Case 05's teaser** about the Central Park Five is being fact-checked in the Case 06 research.
  If it needs a change, it gets re-recorded before Case 05 is uploaded.

## What has to happen before each date

The Studio steps (`channel/setup.md` §10) are yours; the API can't do them, or was blocked when
we tried:

1. **Captions:** Cases 01 and 02 have them. Cases 03 and 04 still need the `.srt` uploaded.
2. **Test & Compare:** title 2 and thumbnail B, from each `youtube.md`.
3. **End screen:** two video slots on the end card. Point one at the previous case, and once the
   next case is live, update the other slot to it.
4. **After it goes live:** pin the verdict comment from `youtube.md`.
5. **The Short:** set its Related video to the episode before it goes public.

Once a case's Studio steps are done, tell me and I'll set its publish time through the API
(`status.publishAt`, private until then), and its Short's for the Sunday after. You don't need to
be at a keyboard on release day.

## After each release

Per the checklist, 48 hours after each episode goes public, compare its click-through rate and
average view duration with the previous case's first 48 hours, and note them in its `youtube.md`.
The Test & Compare result decides which title and thumbnail style to lead with next time.
