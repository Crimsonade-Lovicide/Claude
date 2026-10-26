# Weight of Evidence: YouTube channel setup

One-time setup, then a checklist for every episode. Checked against YouTube Help in October 2026.
YouTube renames menus often, so if a label doesn't match, search for it in YouTube Help.

## 1. Before you click anything

- **Name and handle: Weight of Evidence, `@WeightOfEvidence`.** No channel held the handle on
  12 Oct 2026; confirm in the create screen. If it's blocked, fall back to Due Weight /
  `@DueWeight` rather than a suffixed handle. (The working title, Open Verdict, was dropped:
  @OpenVerdict is a dormant 2007 account, and two unrelated mystery channels launched under
  the name in Sep–Oct 2026.)
- **Pick the account.** Use the same Google account as UNBUILT and create Weight of Evidence as a
  *separate channel* (a Brand Account). Don't open a new Gmail for it. You keep one login, and
  the channel still has its own analytics, audience, monetization and managers. It can also be
  transferred or sold on its own later.
- **Turn on 2-Step Verification** for that Google account if it isn't on already. YPP requires it.

## 2. Create the channel (10 minutes)

1. Sign in to YouTube with the UNBUILT Google account.
2. Go to <https://www.youtube.com/channel_switcher> → **Create a channel**.
   (Not the **+ Create** button in the top bar: that's for uploading, and it only lists the
   channels you already have.)
3. Enter the name and accept or edit the handle. Then choose **Create**.
4. Switch into the new channel (profile picture → *Switch account*) before you change anything
   else, so the settings below don't land on UNBUILT.

## 3. Unlock features, before the first upload

Check **YouTube Studio → Settings → Channel → Feature eligibility**.

| Tier | How to get it | What Weight of Evidence needs from it |
|---|---|---|
| Intermediate | Phone verification (<https://www.youtube.com/verify>) | Uploads over 15 minutes (Case 01 runs 19:05) and custom thumbnails |
| Advanced | Channel history, or **ID or video verification** | Clickable source links in the description, chapters, pinning the verdict comment, linking the vertical Short to the full episode, A/B testing title and thumbnail, applying for YPP |

A new channel has no history. If Advanced isn't on, do the ID or video verification right away;
otherwise Case 01 goes out without working source links, chapters or the pinned verdict.

## 4. Branding (Studio → Customization)

| Slot | File | Spec |
|---|---|---|
| Picture | `deliverables/channel/avatar_800.png` | 800×800, shown as a 98 px circle |
| Banner image | `deliverables/channel/banner_2048.jpg` | 2048×1152. Text sits inside the 1235×338 area every device shows (see `banner_check.png`) |
| Video watermark | `deliverables/channel/watermark_150.png` | 150×150 transparent. Display time: *Entire video* (it sits bottom-right; the RECONSTRUCTION tags are top-right, so they don't collide) |

To regenerate the art after a rename, change the strings in `production/channel_art.py`, then run
`python channel_art.py <prod> <out>`.

**Basic info**

- Description (first 150 characters show in search):
  > One hard question per episode: ethical, historical or legal. We go through the record,
  > separate what's documented from what's argued, and end with a verdict and how sure we are.
  > Every reconstruction is labelled. Think we got it wrong? Make your case in the comments.
- Links: leave empty until there's a site or newsletter. Don't link UNBUILT here (see §8).
- Contact email: a business address, not your personal Gmail.

**Layout**

- Channel trailer for people who haven't subscribed: `weight_of_evidence_trailer.mp4` (it has to be
  uploaded first; public or unlisted both work).
- Featured video for returning subscribers: the latest case.

## 5. Channel-wide defaults (Studio → Settings)

- **Channel → Advanced settings → Audience:** "No, set this channel as not made for kids."
- **Channel → Basic info:** country (needed for YPP), keywords (weight of evidence, insanity defense,
  ethics, law, history, neuroscience).
- **Upload defaults → Basic info:**
  - Category: Education.
  - Language and caption language: English.
  - License: Standard YouTube License.
  - Description template: the footer below.

  ```
  Every 3D scene, scan and recreated document in this video is a reconstruction or
  illustration and is labelled on screen.

  Think we got the verdict wrong? Make your case in the comments. We'll answer the strongest
  argument in the next episode.
  ```
- **Upload defaults → Advanced:** allow all comments but hold potentially inappropriate ones for
  review, and leave sorting on Top. The comment section is part of the format, so moderate
  rather than restrict.
- **Community → Blocked words:** add the names of Case 01's victims' families if trolling starts.
  The topics (child abuse, a mass shooting) attract it.

## 6. AI and synthetic-content disclosure

When you upload, Studio asks whether the video has *altered or synthetic content*. YouTube
requires a "Yes" when realistic content could be mistaken for real: a real person shown saying or
doing something they didn't, real footage altered, or a realistic scene that never happened.
Examples that don't need it: production help, special effects, clearly unrealistic or animated
content, and cloning **your own** voice. The help page has no example for a stock AI narrator
voice. ([YouTube Help](https://support.google.com/youtube/answer/14328491))

- **Case 01: answer No (judgment call, not stated policy).** Every 3D scene is stylised and
  labelled RECONSTRUCTION/ILLUSTRATION. Nothing shows a real person saying or doing anything.
  The narrator is an ElevenLabs stock voice that doesn't imitate anyone real, and quotes are
  read as quotes.
- **Answer Yes in future** if a case uses a photoreal recreation of a real event or place (a
  realistic Tempe crash scene, say) or a voice that sounds like a real person.
- **From Case 07 on: answer Yes** (owner's decision, 26 Oct 2026). The hybrid look (FORMAT.md §2)
  uses photoreal Higgsfield clips of real places (the Capitol, the Supreme Court, Westminster). They
  show no people and are tagged ILLUSTRATIVE · AI-GENERATED on screen, but a viewer could take them
  for real footage. Cases 01–06 stay No: they have no generated footage.

## 7. Monetization (what's verified and what isn't)

**Verified, from YouTube Help (Oct 2026).** These are the YPP requirements:
- 1,000 subscribers, **and** either 4,000 public watch hours in the last 12 months or 10M Shorts
  views in the last 90 days.
- 2-Step Verification.
- Advanced features.
- AdSense.
- No active strikes.

The YPP terms change on 1 Feb 2027. Monetized channels must accept them in Studio by
31 Jan 2027. ([YouTube Help](https://support.google.com/youtube/answer/72851))

**Unverified.** One outlet reports the threshold for new applicants rises to 8,000 watch hours
from Feb 2027. Check the Studio notice when it arrives.

**The real risk is the inauthentic-content rule** (renamed from "repetitious content" in July
2025). Faceless channels with synthetic narration get the closest review, because mass-produced
AI channels look like that. What protects Weight of Evidence:
- original research with cited sources;
- original visuals built for each case;
- a different question every episode.

What would hurt it:
- episodes that feel templated (same visual beats, only the nouns change);
- thin descriptions.

The verdict format is fine; matching the visuals and structure one-to-one isn't.

Cheapest insurance: **narrate in your own voice**, or clone it in ElevenLabs. The pipeline is
unchanged (`align.py` doesn't care whose voice it is), the voice is distinctive, and a clone of
your own voice is explicitly exempt from disclosure.

## 8. UNBUILT and Weight of Evidence

Keep the brands separate: no shared art, no "from the makers of UNBUILT", and no channel link in
either About section. Cross-promotion is a separate decision. One UNBUILT community post at
launch is the cheapest audience you'll get. Its downside: YouTube may seed Weight of Evidence to
UNBUILT's audience at first, which skews early analytics. Recommendation: do one post at launch
and nothing structural.

## 9. Uploads through the API (optional, recommended)

UNBUILT already uploads through the Make scenario **"UNBUILT · YouTube API (uploads)"**. It is a
YouTube *universal* module that starts resumable uploads, and its connection is authorised for
the UNBUILT channel only. For Weight of Evidence:

1. In Make → Connections, **add a new YouTube connection**. On Google's account picker, choose
   the **Weight of Evidence** channel, not UNBUILT.
2. Claude clones the scenario as "Weight of Evidence · YouTube API (uploads)" on that connection.

After that, Claude can upload straight from the production container:
- the **full-quality master** (2.28 GB). The browser-link copy had to be squeezed to 476 MB.
  YouTube re-encodes whatever it gets, and dark gradients like ours band badly from a
  low-bitrate source.
- the thumbnail, the `.srt` captions, the playlist placement and a scheduled publish time.

## 10. Per-episode publish checklist

- [ ] Video uploaded (master file), privacy **Private** until the checks below are done.
- [ ] Title from `youtube.md` (option 1); Test & Compare with option 2 (Advanced feature).
- [ ] Thumbnail A, with B in the same Test & Compare.
- [ ] Description from `youtube.md`: content note, reconstruction note, chapters (first one
      0:00), sources.
- [ ] Captions: upload the `.srt` (Subtitles → Add language → English → Upload file → *With
      timing*). It's script-accurate, unlike auto-captions (which spell M'Naghten wrong).
- [ ] Altered/synthetic content: answer per §6.
- [ ] Audience: not made for kids. Age restriction: none.
- [ ] Tags from `youtube.md`. Category: Education.
- [ ] End screen: two video elements on the end-card slots (300,470) and (1020,470), 600×338.
      Before Case 02 exists, use one slot for "Subscribe" and one for "Best for viewer".
- [ ] Playlist: "Cases".
- [ ] Publish (or schedule). Then **pin the verdict comment** from `youtube.md`.
- [ ] Vertical cut as a Short, with **Related video** set to the full episode.
- [ ] 48 hours later: compare click-through and average view duration against the first 48
      hours of the previous case. Note the result in the episode's `youtube.md`.
