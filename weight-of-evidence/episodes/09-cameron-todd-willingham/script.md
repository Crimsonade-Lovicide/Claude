# Case 09: Cameron Todd Willingham

**Question:** Should a state execute someone when the evidence is disputed?
**Runtime target:** 17–19 min. Narration about 2,800 words.
**Voice:** the same ElevenLabs voice and model as Cases 01–08.

Every factual line traces to `research.md` (IDs in brackets in the picture notes). Picture
notes name the tool that builds each shot:
- `3D:` Blender scene from `production/scenes.py`
- `GFX:` Pillow graphic from `production/gfx.py` / `production/ep09.py`

Narration is the `>` lines only. `production/narration.py` extracts them and applies the
pronunciation table at the bottom.

Care rules for this episode (research §K):
- **Three young children died.** Amber, Karmon and Kameron are named once, with their ages (S03). No
  images of them, nothing about their injuries or where they were found, no crying or alarm sounds. Webb's
  claim about one of the children is not used.
- **No re-enactment of the fire.** No figures, no "father on the porch", no model of the real house. The only
  fire imagery is an empty, generic test room explaining flashover (S41), tagged `ILLUSTRATION · NOT DATA`.
- **No execution imagery.** The last statement is text only, and ends at "I love you Gabby" (S33).
- **People are never depicted**: not Willingham, Stacy Kuykendall, his parents, Webb, Jackson, Vasquez or Fogg.
- **Our voice never says** "innocent", "exonerated", "cleared" or "wrongfully executed". Willingham said he was
  innocent; others argue it, credited. We say "the arson evidence didn't show arson" and "his conviction
  stands", and keep that apart from whether he set the fire, which no one can now know (S48).
- **Stacy Kuykendall** is the children's mother. Her view is given in her own words, early and with respect
  (S05, S47). That her account changed is said once, attributed, with no motive implied.
- **Webb and Jackson:** Webb's several accounts are reported as his; the prosecutor, John Jackson, was cleared
  by a jury in 2017, and we say so wherever the deal allegation appears (S46).
- **Vasquez is dead and can't answer.** His methods are judged in the reviewers' words, and we say his
  phrasing came from the training of the day (S13).
- **Officials** appear only in their own dated words. "Perry ignored the report" is not established (S31).

---

## COLD OPEN

### S01 · The fax
**Picture:** `3D: fax` An old office fax machine on an empty desk at night, one desk lamp, a page feeding slowly out; slow push. Lower third "Austin, Texas · February 13, 2004". Tag RECONSTRUCTION. [T5, C5, C7]
> It's Friday, February the thirteenth, 2004. A five-page report arrives by fax at the Texas parole board and the governor's office. A fire scientist has read the evidence in a death penalty case, and he is writing to say most of it doesn't hold up. The execution is set for Tuesday.

### S02 · The report
**Picture:** `GFX: card` RECORD: "…most of the conclusions reached by the Fire Marshall would be considered invalid in light of current knowledge." Dr. Gerald Hurst, report for the clemency petition, Feb 13, 2004. [C6, T5]
> The man on death row is Cameron Todd Willingham. Twelve years earlier, a jury found that he set the fire that killed his three daughters. The fire investigators had told the jury the burn marks proved that someone poured a liquid and lit it.

### S03 · The fire
**Picture:** `GFX: rows` DEC 23, 1991 · A house fire in Corsicana, Texas / AUG 1992 · Convicted of capital murder / FEB 17, 2004 · Executed. Label RECORD. Source "Willingham v. State, 1995 · TDCJ". [T1, T2, T4, C11]
> The fire was two days before Christmas, 1991, in Corsicana, Texas. Amber was two. The twins, Karmon and Kameron, were one. Their father got out. They didn't.

### S04 · Fifteen to nothing
**Picture:** `GFX: rows` FEB 13, 2004 · The parole board: 15–0 against clemency / FEB 17, 2004 · No reprieve from the governor; executed. Label RECORD. Source "Board of Pardons and Paroles, Feb 13, 2004 · TDCJ". [C7, C10, C11]
> The parole board voted fifteen to nothing against clemency. The governor didn't grant a thirty-day reprieve. That Tuesday, Texas executed him. His last words were that he was innocent.

### S05 · Since then
**Picture:** `GFX: card` RECORD: "A finding of arson could not be sustained." Dr. Craig Beyler, for the Texas Forensic Science Commission, 2009. Then card ARGUMENT: "My ex-husband murdered my daughters, and just before he was executed, he told me he did it." Stacy Kuykendall, Oct 6, 2010. [T7, D6, I3]
> Since then, independent fire scientists, including one hired by a Texas commission, have concluded the evidence never showed arson. But no court has overturned his conviction. And the girls' mother, Stacy Kuykendall, says he confessed to her before he died.

### S06 · Not rare
**Picture:** `GFX: number` "4%" in brass; above, mono "DEATH SENTENCES THAT ARE FALSE CONVICTIONS"; below, "at least · a conservative estimate". Source "Gross, O'Brien, Hu & Kennedy, PNAS, 2014". [H5]
> Mistakes in capital cases aren't rare. The most careful estimate is that at least four in every hundred people sentenced to death in America were wrongly convicted.

### S07 · The question
**Picture:** `3D: scale_empty` The Scale, empty and level.
> So, should a state execute someone when the evidence is disputed? Almost every case is disputed by someone. So when is a doubt serious enough to stop?

### S08 · The promise
**Picture:** `GFX: words` White words, "how sure" in brass.
> We went through the court record, the fire reports from 1991 and the reviews that came after, the clemency file, the state commission's findings, and what the law says about innocence after a trial. At the end, we'll give you a verdict, and tell you how sure we are.

### S09 · Title
**Picture:** `GFX: title` WEIGHT OF EVIDENCE · CASE 09 / CAMERON TODD WILLINGHAM / *Should a state execute someone when the evidence is disputed?* No narration; music hit.

---

## I. THE FIRE

### S10 · Act title
**Picture:** `GFX: title` I · THE FIRE

### S11 · The morning
**Picture:** `GFX: rows` ABOUT 9:15 A.M. · Stacy leaves to buy Christmas presents / 10:34 A.M. · The fire is reported / HIS ACCOUNT · Woken by Amber calling; smoke; he couldn't reach the twins. Label INFERENCE. Source "Beyler, 2009 · The New Yorker, 2009". [A1]
> On the morning of December the twenty-third, the girls' mother, Stacy, went out to buy Christmas presents. Willingham, who was out of work, stayed home with the children. His account was that he'd gone back to sleep, and woke to Amber calling him and the house full of smoke. He said he tried to reach the twins' room, his hair caught fire, and he couldn't find them.

### S12 · Outside
**Picture:** `GFX: card` INFERENCE: Neighbors saw smoke at the front door, then flames when the bedroom windows broke; then the room "flashed over". Dr. Craig Beyler's reading of the witness statements, 2009. [A2]
> Neighbors saw smoke pouring from the front door. Flames only appeared when the children's windows broke, and then the whole room went up at once. Willingham was shouting that his babies were burning. Firefighters had to restrain him. He was treated in hospital for burns.

### S13 · The fire tells a story
**Picture:** `GFX: card` RECORD: "The fire tells a story. I am just the interpreter." Deputy State Fire Marshal Manuel Vasquez, trial testimony, 1992, as quoted by the Texas Forensic Science Commission. Then footnote: "The Commission found this phrasing was standard in fire-investigation training of the day." [A3, A5, K]
> Within days, the house was examined by a deputy state fire marshal, Manuel Vasquez, and Corsicana's assistant fire chief, Douglas Fogg. Vasquez had investigated more than a thousand fires. He later told the jury: the fire tells a story; I am just the interpreter. The state commission would later note that phrases like that came straight from the training of the day.

### S14 · The signs
**Picture:** `GFX: rows` POUR PATTERNS · Shapes on the floor, read as poured liquid / LOW BURNS · Floor hotter than ceiling / THREE ORIGINS · Fires started in three places / CRAZED GLASS · Read as a fast, hot fire / THE THRESHOLD · Charring under the front door's metal strip. Label RECORD. Source "Vasquez's testimony, as quoted by the Texas Forensic Science Commission, 2011". [A4, A5]
> What they read in the burned house was a list of signs. Shapes on the floor that looked like puddles of poured liquid. Burning low down, which Vasquez said meant the floor was hotter than the ceiling, and that could only mean an accelerant. Three separate points of origin. Cracked, crazed window glass. And charring under the aluminum strip across the front doorway. Vasquez said the fire had been intentionally set by human hands.

### S15 · The lab
**Picture:** `GFX: rows` SAMPLES SENT · An unknown number / POSITIVE · One: at the front-door threshold / FOUND · Charcoal lighter fluid; a grill had stood on the porch. Label RECORD. Source "Texas Forensic Science Commission, 2011 · Beyler, 2009". [A6]
> Samples went to the lab. One came back positive: the one from the front doorway, with a residue consistent with charcoal lighter fluid. A barbecue grill had stood on that porch, with bottles of lighter fluid, and was moved while the fire was being fought. Nothing from the bedroom or the hallway, where the pour patterns were, tested positive.

### S16 · His feet
**Picture:** `GFX: card` RECORD: "…entirely consistent with being exposed to a room fire environment." Dr. Craig Beyler, on Willingham's injuries, 2009. [A8]
> Vasquez also said that if the hallway floor had been burning, Willingham couldn't have run out barefoot without burning his feet, so his story was a fabrication. A fire scientist later found his injuries entirely consistent with being caught in a burning room. One thing in his story did change. He later told his parents he had never actually crawled into the girls' room. He said he didn't want people to think he was a coward.

### S17 · The arrest
**Picture:** `GFX: rows` JAN 8, 1992 · Arrested, sixteen days after the fire / MOTIVE · None ever established. Label RECORD. Source "Willingham v. State, 1995 · The New Yorker, 2009". [A10]
> Sixteen days after the fire, Willingham was arrested and charged with murder. The district attorney suggested on television that the children had been getting in the way of his beer drinking and dart throwing. No motive was ever established.

### S18 · First weight
**Picture:** `3D: scale_tip_left` One pan drops. Lower third "EVIDENCE · A FIRE MARSHAL WHO READ ARSON IN THE FLOOR". [A1–A10]
> So, the first weight on the scale. A fire that killed three children. A father whose story had a hole in it. And an investigator who looked at the burned floor and saw a crime.

---

## II. THE TRIAL

### S19 · Act title
**Picture:** `GFX: title` II · THE TRIAL

### S20 · The offer
**Picture:** `3D: courtroom_push` (Case 07 clip) The empty courtroom, slow push. Lower third "Corsicana, Texas · August 1992". Tag RECONSTRUCTION. [B1]
> Before the trial, the prosecutor, John Jackson, offered Willingham a life sentence if he pleaded guilty. His own lawyers urged him to take it. He refused. He said he wasn't going to plead to something he didn't do, especially killing his own kids.

### S21 · Hotter than the ceiling
**Picture:** `GFX: card` RECORD: "So when I found that the floor is hotter than the ceiling, that's backwards, upside down … The only reason that the floor is hotter is because there was an accelerant." Manuel Vasquez, trial testimony, 1992. [A5]
> The trial took two days. At its center was the fire marshal. When the floor is hotter than the ceiling, he told the jury, that's backwards, upside down. The only reason is an accelerant.

### S22 · The informant
**Picture:** `GFX: card` RECORD: "…appellant openly admitted to a fellow inmate that he purposely started this fire…" Texas Court of Criminal Appeals, summarizing the trial evidence, 1995. [B4]
> The jury also heard from Johnny Webb, a man in the county jail on a robbery charge. Webb testified that Willingham had confessed to him. Asked about a deal, Webb said he'd been told no one could do anything for him.

### S23 · The defense
**Picture:** `GFX: rows` DEFENSE FIRE EXPERT · Agreed it was arson; didn't testify / DEFENSE WITNESSES · One: the babysitter / THE JURY · Out about an hour. Label INFERENCE. Source "The New Yorker, 2009 · AP, 2010". [B3]
> His court-appointed lawyers hired their own fire expert, who agreed it was arson, so he never testified. They called one witness, the babysitter. The jury deliberated for about an hour, and on August the twenty-first, 1992, convicted him of capital murder.

### S24 · What the jury heard about him
**Picture:** `GFX: rows` HIS RECORD · Burglary, theft and other offenses in Oklahoma / WITNESSES · Said he had beaten Stacy, including while she was pregnant / STACY · Testified for him at sentencing. Label RECORD. Source "Willingham v. State, 1995 · AP, 2009". [B6]
> To decide on a death sentence, the jury heard about his past. He had a record for burglary and theft. Witnesses said he had beaten Stacy, including while she was pregnant. Stacy herself testified for him, and denied that he'd hurt her.

### S25 · Never examined
**Picture:** `GFX: card` RECORD: "…fits the profile of an extremely severe sociopath…" Dr. James Grigson's testimony, as summarized by the Texas Court of Criminal Appeals, 1995. Then footnote: "Neither expert had examined him. The American Psychiatric Association expelled Grigson in 1995." [B5]
> Then the State called two experts. One, a psychiatrist named James Grigson, testified that Willingham was an extremely severe sociopath who could not be rehabilitated. The other pointed to the heavy-metal posters on his walls. Neither of them had ever examined him. Three years later, the American Psychiatric Association expelled Grigson for diagnosing people he hadn't examined.

### S26 · The sentence
**Picture:** `GFX: words` "DEATH" in ink, held. [B3, B5]
> The jury sentenced him to death.

### S27 · Second weight
**Picture:** `3D: scale_tip_right` The other pan drops. Lower third "EVIDENCE · THE FIRE MARSHAL, AN INFORMANT, AND EXPERTS WHO NEVER MET HIM". [A5, B1–B6]
> So, the second weight. The core of the case was the fire marshal's reading of the burn marks. Around it, a jailhouse informant, a violent record, and experts who called him a sociopath without ever meeting him.

---

## III. THE LAST FOUR DAYS

### S28 · Act title
**Picture:** `GFX: title` III · THE LAST FOUR DAYS

### S29 · The appeals
**Picture:** `GFX: card` RECORD: "…a claim of 'actual innocence' is not itself a constitutional claim…" Herrera v. Collins, U.S. Supreme Court, 1993. Then card RECORD: "Executive clemency has provided the 'fail safe' in our criminal justice system." Chief Justice Rehnquist, same case. [C1–C3, G1, G2]
> For eleven years, his appeals went through the state and federal courts. None of them challenged the fire science; no one had yet. And the Supreme Court, in a Texas case in 1993, had said that a claim of innocence after a fair trial isn't, on its own, a constitutional claim at all. The safety net, it said, was clemency: the fail-safe in a system run by fallible human beings.

### S30 · The chemist
**Picture:** `GFX: rows` "CRAZED GLASS" · "an 'Old Wives Tale'" / "THE THRESHOLD" · liquid can't burn under it, "any more than … grease burn in a skillet" with a lid / "POUR PATTERNS" · can't be told apart after a room flashes over. Label RECORD. Source "Dr. Gerald Hurst, report, Feb 13, 2004". [C5, C6]
> In early 2004, his lawyer sent the file to Gerald Hurst, a chemist with a doctorate from Cambridge who had spent his career on fire and explosives. Hurst worked for free, and fast. Crazed glass, he wrote, was an old wives' tale. A liquid can no more burn under a metal threshold than grease can burn in a skillet with a lid on. And once a room flashes over, the whole floor burns, and so-called pour patterns can't be told apart from ordinary fire.

### S31 · February 13
**Picture:** `GFX: rows` FEB 3, 2004 · Clemency petition filed / FEB 13 · Hurst's report faxed to the Board and the governor's office / FEB 10–13 · The Board votes 15–0; four votes cast before the report was signed. Label RECORD. Source "Texas Forensic Science Commission, 2011 · Board of Pardons and Paroles, Feb 13, 2004". [C5, C7, C8]
> On February the thirteenth, the report was faxed to the parole board and the governor's office. The board voted fifteen to nothing against clemency. Four of those votes had been cast before Hurst's report was even signed. The board didn't hold a hearing. One of its members later said: we get all kinds of reports, but we don't have the mechanisms to vet them.

### S32 · Simply an opinion
**Picture:** `GFX: card` INFERENCE: The courts "agreed that the new opinion by Gerald Hurst was simply an opinion and did not merit reopening the case." Lucy Nashed, spokeswoman for Gov. Rick Perry, 2011. [C4, C10]
> His lawyers also filed the report with Texas's highest criminal court, which ruled it didn't meet the legal test for new evidence of innocence. The governor, Rick Perry, could have granted a thirty-day reprieve on his own. He didn't. His office later said he'd been briefed on the report, and that the courts had found it was simply an opinion.

### S33 · February 17
**Picture:** `GFX: card` RECORD, typed: "Yeah. The only statement I want to make is that I am an innocent man - convicted of a crime I did not commit. I have been persecuted for 12 years for something I did not do. From God's dust I came and to dust I will return - so the earth shall become my throne. I gotta go, road dog. I love you Gabby." Last statement, Feb 17, 2004. Texas Department of Criminal Justice. Tag RECONSTRUCTION. No image of the chamber. [C11]
> On Tuesday, February the seventeenth, 2004, Texas executed Cameron Todd Willingham. His last statement began: I am an innocent man, convicted of a crime I did not commit.

### S34 · Third weight
**Picture:** `3D: scale_tip_right` The pan sinks further. Lower third "EVIDENCE · A WARNING IN TIME, AND NO ONE REQUIRED TO TEST IT". [C1–C11]
> So, the third weight. A scientist's warning reached the people with the power to stop the execution, four days before it. The law didn't require anyone to test it. There's no record that anyone did.

---

## IV. THE SCIENCE

### S35 · Act title
**Picture:** `GFX: title` IV · THE SCIENCE

### S36 · Lime Street
**Picture:** `3D: fireroom` An empty test room, a single couch, the floor darkening in patches as the room reaches flashover; slow push. Lower third "A TEST BURN · NO ACCELERANT". Tag ILLUSTRATION · NOT DATA. [F2, F4]
> The science had been changing since 1990. That year in Jacksonville, Florida, investigators were sure a fatal fire had been set with a liquid. To check, they burned the empty house next door, with nothing but a couch to start it. In a few minutes the room flashed over: everything in it caught at once. Afterwards, the floor showed the same pour patterns, without a drop of accelerant. The charges in that case were dropped.

### S37 · Then and now
**Picture:** `GFX: rows` header "WHAT THE SIGNS MEAN NOW": POUR PATTERNS · Made by flashover and melting materials / LOW BURNS · Radiant heat; floors aren't hotter than ceilings / THREE ORIGINS · Burning debris dropping, separate patches / CRAZED GLASS · Water on hot glass; "no longer has any value" / THE THRESHOLD · Heat at doorways. Label RECORD. Source "Texas Forensic Science Commission, 2011 · Hurst, 2004". [F3]
> In 1992, the year of the trial, fire investigators got their first national guide built on the science, and over the next decade the old signs fell one by one. The patterns could come from flashover. Low burns, from the heat radiating down. Separate patches, from burning debris falling. Crazed glass, it turned out, came from the water sprayed on hot glass. A Texas commission later said it no longer had any value as a sign of anything.

### S38 · The twin case
**Picture:** `GFX: rows` 1986 · A fire in West Texas kills two women / 1987 · Ernest Ray Willis sentenced to death on "pour patterns" / OCT 2004 · A new prosecutor has the science reviewed; Willis freed. Label RECORD. Source "National Registry of Exonerations · Texas Forensic Science Commission, 2011". [H1, H2, D2]
> Eight months after Willingham's execution, Texas freed another man. Ernest Ray Willis had been sentenced to death for a fire on the same kinds of signs. A new prosecutor had the evidence reviewed, by experts including Gerald Hurst. They found no evidence of arson, and Willis walked out of prison. Same science, same scientist. Willis had a prosecutor willing to look.

### S39 · The reviews
**Picture:** `GFX: card` RECORD: "…each and every one of the indicators relied upon have since been scientifically proven to be invalid." Arson Review Committee, 2006. Then card RECORD: "…more characteristic of mystics or psychics." Dr. Craig Beyler, on the fire marshal's statements, for the Texas Forensic Science Commission, 2009. [D3, D5, D6]
> In 2006, a five-member review panel, led by fire experts, looked at the case for the Innocence Project and found every sign the investigators relied on had been shown to be invalid. Texas had just created a Forensic Science Commission, and it hired its own expert, Craig Beyler. His report was blunter still. Vasquez's statements, he wrote, were more characteristic of mystics or psychics than of fire science. A finding of arson, he concluded, could not be sustained, by the standards of 2009 or of 1991.

### S40 · Two days before
**Picture:** `GFX: rows` SEPT 30, 2009 · The governor replaces the commission's chair and members / OCT 2, 2009 · The hearing on Beyler's report is cancelled. Label INFERENCE. Source "Dallas Morning News, via DPIC · CNN, 2011". Then card ARGUMENT: "Willingham was a monster." Gov. Rick Perry, Oct 14, 2009. Then card ARGUMENT: "…this kind of endless drumbeat of strategies and actions to stop this investigation." Sam Bassett, former commission chair, 2011. [D7–D9]
> Two days before the commission was to hear Beyler, Governor Perry replaced its chair and other members. The new chair cancelled the hearing. Perry said their terms had expired, and that it was business as usual. He called Willingham a monster, and said witness after witness had testified to the facts of the case. The chair he replaced later described an endless drumbeat of efforts to stop the investigation.

### S41 · Untenable
**Picture:** `GFX: card` RECORD: "In reviewing documents and standards in place then and now, we stand by the original investigator's report and conclusions." State Fire Marshal's Office, Aug 20, 2010. Then card RECORD: "…an untenable position in light of advances in fire science." Texas Forensic Science Commission, April 15, 2011. [D10, D11]
> The State Fire Marshal's Office said it stood by the original findings. In 2011, the commission called that position untenable in light of the science. It found that the key signs had lost their value, and that nobody had told the courts or prosecutors that the standards had changed. But it made no finding of negligence, and said plainly that it was making no comment on anyone's guilt or innocence. The Attorney General then ruled that it had no power to look at evidence from before 2005 at all.

### S42 · Webb
**Picture:** `GFX: rows` 1992 · Testifies Willingham confessed / 2000 · Tries to recant; withdraws it / 2014 · Says he lied in exchange for help / 2017 · The prosecutor is cleared by a jury, 11–1. Label INFERENCE. Source "CNN, 2014 · The Intercept, 2017 · Marshall Project, 2017". [E1–E8]
> The informant changed his story too. Johnny Webb tried to recant in 2000, then withdrew it. In 2014 he said he'd lied in exchange for help. Letters showed the prosecutor, John Jackson, had written on Webb's behalf after the trial, and an unsigned note in the prosecutor's file tied Webb's reduced charge to his cooperation in the case. Jackson denied any deal, and in 2017, a jury in the State Bar's case against him found, eleven to one, that he had not committed misconduct.

### S43 · The pardon
**Picture:** `GFX: rows` 2010 · A court of inquiry is stopped before any ruling / APR 3, 2014 · The parole board declines a posthumous pardon. Label INFERENCE. Source "Texas Tribune, 2014". [G9, T8]
> His family asked for a court to declare him wrongly convicted. That inquiry was stopped before it ruled. In 2014, they asked for a posthumous pardon. The parole board said no. His conviction stands.

### S44 · The rules now
**Picture:** `GFX: rows` 2011 · Fire investigators must reopen old cases when the science changes (recommendation) / 2013 · Texas lets courts overturn convictions built on discredited science / 1965 · England abolishes the death penalty for murder. Label RECORD. Source "Texas Forensic Science Commission, 2011 · Tex. Code Crim. Proc. art. 11.073 · Murder (Abolition of Death Penalty) Act 1965". [D12, G7, H6]
> Texas has since changed some rules. The commission recommended that when the science changes, investigators have a duty to tell the people affected. In 2013, Texas let courts overturn a conviction if new science shows the person likely wouldn't have been convicted. It came nine years too late for Willingham. England took a different road long before: it abolished the death penalty for murder in 1965.

### S45 · Fourth weight
**Picture:** `3D: scale_tip_left` The first pan recovers ground. Lower third "EVIDENCE · THE SCIENCE CHANGED. THE CONVICTION DIDN'T." [D1–G10]
> So, the fourth weight. Every independent review found the fire evidence didn't show arson. The State has never said it was wrong. And the system that might have tested that, before the execution, didn't exist yet.

---

## V. THE VERDICT

### S46 · Act title
**Picture:** `GFX: title` V · THE VERDICT

### S47 · The case for the State
**Picture:** `3D: scale_tip_left` Lower third "THE STRONGEST CASE: THE VERDICT STOOD ON MORE THAN FIRE". Then card ARGUMENT: "My ex-husband murdered my daughters, and just before he was executed, he told me he did it." Stacy Kuykendall, 2010. [I1–I6, I13]
> First, the strongest case for the State. The conviction never rested on the fire science alone, its defenders say: there was the informant, the neighbors' accounts, and a man with a violent past. His conviction was reviewed by court after court for eleven years. Fire investigators in 1991 did what they'd been trained to do, and his own lawyers couldn't find an expert to say otherwise. And the person who knew him best, the girls' mother, says he confessed to her. In 1992 and again in 1999 she had said she didn't believe he did it; she says now that he told her the truth on her last visit.

### S48 · The case against
**Picture:** `3D: scale_tip_right` Lower third "THE STRONGEST CASE: DEATH CAN'T BE CORRECTED". Then card RECORD: "The execution of a person who can show that he is innocent comes perilously close to simple murder." Justice Blackmun, dissenting, Herrera v. Collins, 1993. [I7–I12, I13]
> Now the strongest case against. The only physical evidence that a crime happened at all didn't show arson. What remained was an informant who has told at least four versions of his story, and experts who diagnosed a man they'd never met. A credible scientist warned the people who could stop the execution, four days ahead, and nothing required them to test what he said. Whether Willingham set the fire, no one can now prove either way. But that's the point: the State executed him on evidence it can no longer stand behind.

### S49 · Verdict one
**Picture:** `GFX: verdict` Kicker THE FIRE EVIDENCE. VERDICT: "The signs the jury heard were not evidence of arson, by today's science or by the best fire science of 1991." CONFIDENCE 90%. WHAT WOULD CHANGE OUR MIND: "An independent fire scientist defending those signs on modern science, or lab results showing accelerant where the patterns were."
> Here's our verdict. On the fire evidence: the signs the jury heard were not evidence of arson, by today's science or by the best fire science of 1991. Our confidence is ninety percent. What would change our mind: an independent fire scientist defending those signs on modern science, or lab results showing accelerant where the patterns were.

### S50 · Verdict two
**Picture:** `GFX: verdict` Kicker FEBRUARY 17, 2004. VERDICT: "Texas should not have carried out the execution that day. With a credible scientific challenge to its only physical evidence, it should have used the 30-day reprieve to test it." CONFIDENCE 85%. WHAT WOULD CHANGE OUR MIND: "Records showing a qualified fire scientist reviewed Hurst's report for the State before the execution, and found it wrong on the merits."
> On February the seventeenth, 2004: Texas should not have carried out the execution that day. With a credible scientific challenge to its only physical evidence on the table, it should have used the thirty-day reprieve to test it. Our confidence is eighty-five percent. What would change our mind: records showing a qualified fire scientist reviewed Hurst's report for the State before the execution, and found it wrong on the merits.

### S51 · Verdict three
**Picture:** `GFX: verdict` Kicker THE QUESTION. VERDICT: "No state should carry out an execution while a credible, specific challenge to the evidence that convicted the person has not been heard by someone competent to judge it." CONFIDENCE 80%. WHAT WOULD CHANGE OUR MIND: "Evidence that such a rule is routinely used to delay executions without finding real errors."
> And on the question: no state should carry out an execution while a credible, specific challenge to the evidence that convicted the person hasn't been heard by someone competent to judge it. Our confidence is eighty percent. What would change our mind: evidence that a rule like that is routinely used to delay executions without finding real errors. As for whether he set the fire: we can't know, and nobody can now prove it either way.

### S52 · The case stays open
**Picture:** `3D: scale_level_loaded` Level, slow orbit, fade toward black.
> That's our verdict. It's open, which means it can change. If you think we got it wrong, make your case in the comments. We'll answer the strongest one in the next episode.

### S53 · Next case
**Picture:** `GFX: words` "NEXT CASE" over black: "TARASOFF · 1969" / *Should a therapist break a patient's
confidence to warn someone in danger?*
> Next case: Berkeley, 1969. A graduate student tells his university therapist he intends to kill a young woman. The therapist asks the campus police to detain him. They hold him briefly, and let him go. No one warns her family. That October, he kills her. Her parents sue, and California's Supreme Court rules that a therapist can owe a duty to protect the person a patient threatens. Should a therapist break a patient's confidence to warn someone in danger?

### S54 · End card
**Picture:** `GFX: endcard` Title, subscribe area, two end-screen slots. Sources link. No narration.

---

## Pronunciation (applied to narration text only)

Model: eleven_multilingual_v2. Numbers are written out in the narration where the voice could
misread them. Our best guesses, to confirm by ear in the review copy (research §M): Corsicana, Kuykendall
and Beyler.

| Written | Spoken as |
|---|---|
| Corsicana | Kor-sih-kan-uh |
| Kuykendall | Kirk-en-doll |
| Vasquez | Vas-kez |
| Beyler | By-ler |
| Karmon | Kar-mun |
| Grigson | Grig-sun |

## Sources on screen (description box)

See `research.md`. Every RECORD card carries its citation on screen; the full list goes in the
description, led by *Willingham v. State* (1995), Gerald Hurst's report (2004), the Board of Pardons and
Paroles' letter and voting sheet (2004), the Arson Review Committee report (2006), Craig Beyler's report
(2009), the Texas Forensic Science Commission's final report and addendum (2011), the Attorney General's
opinion GA-0866 (2011), *Herrera v. Collins* (1993), TDCJ's last-statement record, Gross et al. (2014),
the National Registry of Exonerations on Ernest Ray Willis, and David Grann, "Trial by Fire" (2009).

## Before recording (from research §N and our own checks)

- **Quotes via Grann, CNN, AP and the Intercept (S11, S12, S20, S31, S32, S40, S42, S47):** spot-check each
  against the page; items marked "via fetch" in the research must be re-read.
- **S01:** "Austin" is where the governor's office and the Board's fax were; the Board's members voted from
  several cities. If in doubt, make the lower third "Texas · February 13, 2004".
- **S03, S11:** confirm the children's names and ages against the CCA opinion (done: RECORD) and keep to
  first names.
- **S06:** "at least four in every hundred" rounds Gross et al.'s 4.1%.
- **S13:** Vasquez's thousand-plus fires is from his testimony as the TFSC and Grann report it.
- **S16:** "never actually crawled into the girls' room" is from Grann's interviews with his family.
- **S23:** "about an hour" is Grann's "barely an hour".
- **S25:** confirm the APA's 1995 statement on Grigson; "heavy-metal posters" describes the Iron Maiden and
  Led Zeppelin images without naming them.
- **S31:** the four early votes are Feb 10–12; the narration says "before Hurst's report was even signed",
  per research C8. Don't strengthen it.
- **S36:** Lime Street is known through Grann and Hurst's citation; read the 1992 paper if possible. The 3D
  test room is generic and tagged as an illustration.
- **S37:** NFPA 921 was first published in 1992; "first national guide built on the science" paraphrases it.
- **S38:** Willis's release: October 2004 (sources differ on the day).
- **S40:** the number of members replaced differs between sources (research D7); the narration says "its chair
  and other members".
- **S42:** the file note reads "based on coop in Willingham" (via fetch); the narration paraphrases it. Confirm
  before it goes on screen.
- **S44:** Art. 11.073 must be quoted from the official text; the narration paraphrases. "A man it had hanged"
  was cut; England's 1965 Act is quoted from legislation.gov.uk (research H6).
- **S47:** Stacy Kuykendall's earlier accounts (1992 investigators, 1999 tape) are from Grann; confirm.
- **S53:** Case 10 is Tarasoff (owner's choice, 26 Oct 2026); every line checked in `10-tarasoff/research.md` §0.
  "No one warns her family", not "her" (the 1976 opinion: "No one warned plaintiffs"), and "That October", not
  "two months later" (the court's two opinions disagree on the date of the threat).
- **3D:** `fax` (an office fax machine on an empty desk at night) and `fireroom` (an empty test room with a
  couch reaching flashover, floor patterns forming) are new scenes for `scenes.py`. The courtroom clip is
  reused from Case 07, the Scale clips from Case 01.
