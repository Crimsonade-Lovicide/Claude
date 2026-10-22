# Case 05: The Golden State Killer

**Question:** Should police be allowed to search your family's DNA?
**Runtime target:** 17–19 min. Narration about 2,700 words.
**Voice:** the same ElevenLabs voice and model as Cases 01–04.

Every factual line traces to `research.md` (IDs in brackets in the picture notes). Picture
notes name the tool that builds each shot:
- `3D:` Blender scene from `production/scenes.py`
- `GFX:` Pillow graphic from `production/gfx.py` / `production/ep05.py`

Narration is the `>` lines only. `production/narration.py` extracts them and applies the
pronunciation table at the bottom.

Care rules for this episode (research §F): the thirteen murdered are named, once each, with place
and year; nothing about how anyone was attacked; survivors stay Jane Does unless they have spoken
publicly under their own names. The perpetrator's name is said **once** (S26), never shown, never
quoted; no photo, no courtroom or jail video of him. **No relative whose DNA was matched is named or
hinted at**: no "Wright" family, no Orange County cousin, no Oregon man's name. Any family tree is
an illustration with blank nodes, tagged `ILLUSTRATION · NOT DATA`. No re-created screens of
GEDmatch, FamilyTreeDNA or MyHeritage. No dark-house re-enactments. Disputed points are said as
disputed: which site broke the case (B8), "the first" (B18), the rape count (A11).

---

## COLD OPEN

### S01 · The handle
**Picture:** `3D: car_lot` One parked car in an almost empty store car park at dusk, sodium light, slow push toward the driver's door. Lower third "Roseville, California · April 18, 2018". Tag RECONSTRUCTION. [B12]
> On April the eighteenth, 2018, in a store car park in Roseville, California, a detective swabbed the door handle of a parked car. Five days later, another detective took a used tissue from a trash can outside the owner's house. Both went to a lab.

### S02 · The match
**Picture:** `GFX: words` "MATCH" in brass; sub "DNA from a double murder · Ventura County · 1980". [B1, B12, A5]
> They matched DNA left at the scene of a double murder in 1980. For thirty-eight years, that DNA had matched no one. The man it came from had never been arrested, so he had never been in any police database.

### S03 · A family tree
**Picture:** `GFX: words` "NOT A POLICE DATABASE" struck through in red; beneath, "A FAMILY TREE". [B5–B8]
> He wasn't found in a police database. He was found through his relatives: cousins who had sent their DNA to genealogy websites to find out where their families came from.

### S04 · Not asked
**Picture:** `GFX: card` INFERENCE: "The relatives whose DNA led to him were never asked, and most have never been named." Source "LA Times, Dec 2020 · AP, 2018". [B5–B8, B3]
> None of them was asked. Most have never been named. And before the search found the right man, it pointed at the wrong one.

### S05 · Thirteen
**Picture:** `GFX: number` "13" in ink; above, mono "MURDERED"; below, "between 1975 and 1986, and dozens more attacked". Source "Joint release of six California DAs, June 29, 2020". [A5, A9]
> The man was the Golden State Killer. Between the mid-1970s and 1986, he murdered thirteen people in California and attacked dozens more. In 2020 he pleaded guilty. He is serving life without parole.

### S06 · Since then
**Picture:** `GFX: number` "1,182" in brass; sub "cases cleared by genetic genealogy, to February 2024 · one researcher's count". Source "T. L. Dowdeswell, 2024". [D18]
> His arrest made the method famous. Since then, police have used it in well over a thousand cases. And you don't have to take a DNA test to be found by it. A cousin is enough.

### S07 · The question
**Picture:** `3D: scale_empty` The Scale, empty and level.
> So, should police be allowed to search your family's DNA? When one person shares their DNA, they share part of their relatives' DNA too. Who gets to say yes for a family? And what should the state be allowed to do with the answer?

### S08 · The promise
**Picture:** `GFX: words` White words, "how sure" in brass.
> We went through the court record, the investigators' own accounts, the science of how far a family tree can reach, and the first laws written to control it. At the end, we'll give you a verdict, and tell you how sure we are.

### S09 · Title
**Picture:** `GFX: title` WEIGHT OF EVIDENCE · CASE 05 / THE GOLDEN STATE KILLER / *Should police search your family's DNA?* No narration; music hit.

---

## I. THE COLD CASE

### S10 · Act title
**Picture:** `GFX: title` I · THE COLD CASE

### S11 · Across a state
**Picture:** `GFX: timeline` 1974–75 · VISALIA / 1976–79 · SACRAMENTO · EAST BAY / 1979–86 · SANTA BARBARA · VENTURA · ORANGE COUNTY. Source "Sentencing memorandum, People v. DeAngelo, 2020". [A1, A2, A3]
> It began in the mid-1970s in Visalia, in California's Central Valley, with more than a hundred burglaries. Then it moved north, to Sacramento and the East Bay, and then south, to Santa Barbara, Ventura and Orange counties. For years, police thought they were looking for different men.

### S12 · The names
**Picture:** `GFX: words` Stacked mono: VISALIA RANSACKER · EAST AREA RAPIST · ORIGINAL NIGHT STALKER; then "GOLDEN STATE KILLER" in ink, sub "Michelle McNamara · 2013". [A4]
> They gave him different names. The Visalia Ransacker. The East Area Rapist. The Original Night Stalker. DNA showed some of them were the same man. The name most people know came later, in 2013, from the writer Michelle McNamara.

### S13 · The thirteen
**Picture:** `GFX: rows` Thirteen names, each landing as it is said, with place and year in brass mono: CLAUDE SNELLING · VISALIA · 1975, and so on. Label RECORD. Source "People v. DeAngelo, Sacramento Superior Court No. 18FE008017". No photos. [A5, A6]
> The court record names thirteen people he murdered. Claude Snelling, in Visalia, in 1975. Katie and Brian Maggiore, in Rancho Cordova, in 1978. Debra Alexandria Manning and Robert Offerman, in Goleta, in 1979. Charlene and Lyman Smith, in Ventura, in 1980. Keith and Patrice Harrington, in Dana Point, that summer. Manuela Witthuhn, in Irvine, in 1981. Cheri Domingo and Gregory Sanchez, in Goleta, that July. And Janelle Cruz, in Irvine, in 1986. She was eighteen.

### S14 · Who they were
**Picture:** `GFX: card` RECORD: "…never made it to their first wedding anniversary." Orange County DA Todd Spitzer, Aug 21, 2020. Then card RECORD: "Janelle was my big sister. She was one year older than me." Michelle Cruz, victim-impact statement, Aug 2020. [A8, C12, C13]
> Claude Snelling was killed trying to stop a stranger from taking his daughter. Keith and Patrice Harrington never reached their first wedding anniversary. Janelle Cruz hoped to graduate from college. Her sister, Michelle, told the court, "Janelle was my big sister. She was one year older than me."

### S15 · Eighty-seven
**Picture:** `GFX: number` "87" in ink; sub "victims, on 53 occasions, in 11 counties · charged and uncharged, as admitted". Source "People's Sentencing Memorandum, Aug 2020". [A9, A11]
> Many more survived. In the end, prosecutors counted eighty-seven victims, attacked on fifty-three separate occasions, in eleven counties. The prosecutor told the court there had been almost fifty rapes.

### S16 · Why it went cold
**Picture:** `GFX: words` "CODIS · 12 MILLION+ PROFILES (2018)" / sub "it can only match someone already in it". Source "Ram, Guerrini & McGuire, Science 2018". [A16]
> Police had his DNA from the crime scenes. What they didn't have was him. A crime-scene profile can be checked against the national police DNA database, which in 2018 held more than twelve million profiles. But it can only match someone who's already in it, someone who's been arrested or convicted. He never had been.

### S17 · Proposition 69
**Picture:** `GFX: card` INFERENCE: "In 2004, Keith Harrington's brother Bruce sponsored, and largely paid for, Proposition 69, adding every felony arrestee in California to the state's DNA database." Source "California voter guide, 2004 · press". [A17]
> In 2004, Keith Harrington's brother, Bruce, sponsored a ballot measure to add everyone arrested for a felony in California to the state's DNA database, and paid for much of it himself. Voters passed it. It still couldn't find a man who was never arrested.

### S18 · First weight
**Picture:** `3D: scale_tip_left` One pan drops. Lower third "EVIDENCE · THIRTEEN DEAD, AND THE DATABASE COULDN'T FIND HIM". [A5, A16]
> So, the first weight on the scale. Thirteen dead, dozens of survivors, and families who waited four decades for a name. The tool the law had built to find him couldn't, because it only looks where police have already been.

---

## II. THE FAMILY TREE

### S19 · Act title
**Picture:** `GFX: title` II · THE FAMILY TREE

### S20 · A different kind of file
**Picture:** `3D: evidence_shelf` Metal shelving of archive boxes in a cold store, one box lit; slow dolly. Lower third "Contra Costa and Ventura counties · 2017". Tag RECONSTRUCTION. [B1, B11]
> In 2017, a team including Paul Holes, a cold-case investigator in Contra Costa County, and the FBI tried something new. They took DNA from the 1980 Smith murders and turned it into the kind of file that hobby genealogists upload to find their cousins.

### S21 · The wrong man
**Picture:** `GFX: card` INFERENCE: "March 2017: a judge ordered a DNA sample from a 73-year-old man in an Oregon nursing home. He was not the killer." Source "AP, Apr 30, 2018". [B2, B3]
> Their first lead was wrong. A partial match on a genealogy site pointed to a seventy-three-year-old man in a nursing home in Oregon. A judge ordered a sample. His daughter says nobody told the family before he was swabbed in his bed. He was only a very distant relative.

### S22 · Three sites
**Picture:** `GFX: rows` FAMILYTREEDNA · "a made-up account, with the company's help" / GEDMATCH · "a free hobby site, never asked" / MYHERITAGE · "uploaded on a personal account, without telling the company". Generic type only, no logos. Source "LA Times, Dec 2020 · AP, 2018". [B5, B6, B7]
> Then they went to the consumer sites. FamilyTreeDNA, a commercial testing company, let them search its customers under a made-up account. GEDmatch, a free site where people upload their DNA files, didn't know it was being used. And in early 2018, the genealogist on the team, Barbara Rae-Venter, uploaded the DNA to MyHeritage on her own account, without telling the company. None of the customers on any of these sites was told.

### S23 · Disputed
**Picture:** `GFX: card` INFERENCE: "Which site gave the decisive matches is disputed: GEDmatch, in 2018 accounts; MyHeritage, in a 2020 LA Times investigation." [B8]
> Which site cracked it is still disputed. The first accounts in 2018 credited GEDmatch. A Los Angeles Times investigation in 2020 found the closer matches came from MyHeritage. Either way, the search ran on the DNA of people who had shared it for a different reason.

### S24 · The tree
**Picture:** `GFX: tree` An animated family tree with blank nodes: two matches at the bottom, lines climbing to shared ancestors, then fanning down to many descendants, which grey out until a handful remain. Tag `ILLUSTRATION · NOT DATA`. [B10]
> A second cousin shares a pair of great-grandparents with you. From matches like that, the team built family trees back to shared ancestors, then worked forward through their descendants, looking for a man of the right age who had been in the right places. At one point the prime suspect was a cousin's brother. She gave her own DNA, and it cleared him. In the end, six men fit. One had blue eyes, which matched the profile.

### S25 · The former officer
**Picture:** `3D: car_lot` Reprise, a different angle, the car alone in the lot. Tag RECONSTRUCTION. [A14, B12]
> He was a former police officer, seventy-two years old, living in Citrus Heights, outside Sacramento. Detectives watched him for about ten days. The swab from his car door matched the 1980 DNA. So did the tissue from his trash.

### S26 · The arrest
**Picture:** `GFX: rows` APR 18, 2018 · Door handle swabbed / APR 23 · Tissue taken from his trash / APR 24 · Arrested at home. Label RECORD. Source "Unsealed warrants, via BuzzFeed News and AP, June 2018". No photo of him. [B12, B13]
> On April the twenty-fourth, 2018, Joseph James DeAngelo was arrested at his home. It's the only time we'll say his name. The Sacramento district attorney, Anne Marie Schubert, told reporters, "We found the needle in the haystack, and it was right here in Sacramento."

### S27 · No trial
**Picture:** `GFX: rows` JUNE 29, 2020 · Pleads guilty: 13 murders, 13 kidnappings / AUG 21, 2020 · 11 consecutive life terms without parole. Label RECORD. Source "Joint releases of six California DAs, 2020". [C2, C4, C5, C7]
> There was no trial. In June 2020, in a university ballroom in Sacramento, he pleaded guilty to thirteen murders and thirteen kidnappings, and admitted dozens of crimes he could no longer be charged with. In return, prosecutors dropped the death penalty. They said they had consulted the victims and their families, and that a trial could have taken ten years. That August, survivors and families spoke in court for three days. He was sentenced to eleven consecutive life terms without parole.

### S28 · Secrecy
**Picture:** `GFX: card` INFERENCE: "…perpetuates a fraudulent impression." Cheryl Temple, Ventura County prosecutor, letter to the FBI, Jan 2019 (as reported by the LA Times, 2020). [B14, B15]
> For a long time, how he was found stayed secret. At first, prosecutors wouldn't say which sites had been used. In 2019, a prosecutor on the case in Ventura County wrote to the FBI that keeping it quiet perpetuated, in her words, a fraudulent impression. She didn't doubt it was legal. Her objection was the secrecy.

### S29 · Second weight
**Picture:** `3D: scale_tip_right` The other pan drops. Lower third "EVIDENCE · IT WORKED, AND NO ONE WHOSE DNA MADE IT WORK WAS ASKED".
> So, the second weight. It worked. A man who had escaped for forty years was found in months, and the families heard him admit what he did. But the people whose DNA made it work were never asked, the first lead fell on an innocent old man, and for years the public wasn't told how it was done.

---

## III. THE REACH

### S30 · Act title
**Picture:** `GFX: title` III · THE REACH

### S31 · After the arrest
**Picture:** `GFX: number` "13" then "1,182"; sub "cases solved, April–August 2018" then "cases cleared, to February 2024". Sources "Erlich et al., Science 2018 · Dowdeswell, 2024". [D16, D18, D19]
> The arrest opened the door. By one count, at least thirteen more cases were solved the same way in the next four months. By early 2024, a researcher who tracks them, Tracey Leigh Dowdeswell, counted more than eleven hundred. Most involved sexual violence or murder. Some gave names back to the dead.

### S32 · Sixty percent
**Picture:** `GFX: number` "60%" in brass; sub "of searches for people of European descent find a third cousin or closer". Then "2%": "of a population in the database is enough to reach nearly everyone". Source "Erlich, Shor, Pe'er & Carmi, Science 2018". [D20, D21, D22]
> In 2018, a team of scientists, two of them working for MyHeritage, measured how far this reaches. Using more than a million profiles, they estimated that about sixty percent of searches for someone of European descent would turn up a third cousin or closer. That's usually enough to start building a tree. A database covering just two percent of a population, they calculated, could reach nearly anyone in it.

### S33 · Not evenly
**Picture:** `GFX: chart` Two bars: "NORTHERN EUROPEAN BACKGROUND" / "SUB-SAHARAN AFRICAN BACKGROUND", the first 30% longer; label "likelihood of a close match". Source "Erlich et al., Science 2018". Then card ARGUMENT: genealogy databases "might thus begin to redress" the racial skew of police databases. Ram, Guerrini & McGuire, *Science* 2018. [D23, D24]
> The reach isn't even. People of Northern European background were thirty percent more likely to have a close match than people of sub-Saharan African background, because more of their relatives have tested. Police DNA databases skew the other way: Black Americans are over-represented in them. Some scholars argue the genealogy sites might begin to balance that out.

### S34 · The rules move
**Picture:** `GFX: timeline` 2018 · GEDMATCH ALLOWS POLICE SEARCHES FOR MURDER AND RAPE / NOV 2018 · AN EXCEPTION FOR AN ASSAULT IN UTAH / MAY 2019 · USERS MUST OPT IN / JULY 2019 · A FLORIDA JUDGE ORDERS A SEARCH OF EVERYONE / 2019, 2023 · SOLD, THEN SOLD AGAIN. Sources "Salt Lake Tribune 2019 · NBC 2019 · NYT 2019 · QIAGEN 2023". [D2–D5]
> And the rules kept moving. After the arrest, GEDmatch changed its terms to allow police searches for murder and rape. Months later, its founder made an exception for an assault in Utah. After an outcry, in May 2019, users had to opt in. Overnight, the profiles open to police fell to zero. Two months later, a judge in Florida gave a detective a warrant to search the whole database, including the people who had opted out. Then the site was sold to a forensic genetics company, which was itself bought four years later.

### S35 · No genetic information
**Picture:** `GFX: card` INFERENCE: "…a huge game changer… It's a signal that no genetic information can be safe." Erin Murphy, NYU School of Law, 2019 (as quoted in the New York Times). [D4]
> The law professor Erin Murphy said of that warrant that it was a signal that no genetic information can be safe.

### S36 · Promises
**Picture:** `GFX: timeline` 23ANDME · "resists requests from law enforcement"; 0 customers' data produced / 2023 · ABOUT 14,000 ACCOUNTS BREACHED · 6.9 MILLION RELATIVES' PROFILES EXPOSED / 2025 · BANKRUPT; COMPANY AND DATA SOLD. Sources "23andMe transparency report, 2026 · SEC filing, 2023 · AP, 2025". [D10, D11, D12, D13]
> Other companies promise more. Ancestry says it insists on a warrant or court order. 23andMe says it has never handed any customer's data to police. But promises depend on the company. In 2023, hackers got into about fourteen thousand 23andMe accounts and, through a feature that links relatives, exposed the profiles of six point nine million people. In 2025, the company went bankrupt and was sold, genetic data and all.

### S37 · Third weight
**Picture:** `3D: scale_tip_right` The pan sinks further. Lower third "EVIDENCE · YOU CAN BE FOUND WITHOUT EVER TAKING A TEST". [D20, D21]
> So, the third weight. You don't have to take a test to be found. If enough of your cousins have, you already can be. And the rules on when police may look have been written, and rewritten, by whoever happens to own the data.

---

## IV. THE RULES

### S38 · Act title
**Picture:** `GFX: title` IV · THE RULES

### S39 · One murder, both edges
**Picture:** `GFX: timeline` 1996 · ANGIE DODGE MURDERED, IDAHO FALLS / 1998 · CHRISTOPHER TAPP CONVICTED ON A FALSE CONFESSION / 2014 · A FAMILY SEARCH POINTS TO MICHAEL USRY; CLEARED / 2019 · GENEALOGY FINDS THE KILLER; TAPP EXONERATED. Source "National Registry of Exonerations · EFF, 2015". [D26, D27, D28]
> One case shows both edges. In 1996, Angie Dodge was murdered in Idaho Falls. A young man, Christopher Tapp, was convicted after a false confession. In 2014, police searched a genealogy database owned by Ancestry, without a warrant, and found a near match: the father of a filmmaker named Michael Usry. Usry was swabbed and waited a month before he was cleared. Angie's mother, Carol, kept pushing. In 2019, genetic genealogy found the real killer, and Tapp's conviction was thrown out. It's believed to be the first exoneration by genetic genealogy.

### S40 · Close relatives
**Picture:** `GFX: rows` 2008 · CALIFORNIA ALLOWS FAMILIAL SEARCHES OF ITS OWN DATABASE / 2010 · THE GRIM SLEEPER, FOUND THROUGH HIS SON / MARYLAND · BANS THEM. Label RECORD. Source "California Attorney General, 2008, 2010 · Maryland v. King, 2013". [D25, D29, D30, D31]
> Searching for relatives wasn't new. Since 2008, California has let its lab look for partial matches in the state's own police database, pointing to a close relative of an offender. That's how police found the serial killer known as the Grim Sleeper in 2010, through his son. Maryland bans that kind of search. But a police database only reaches close relatives of people already in the system. Genealogy sites reach third cousins who have never met a police officer.

### S41 · The Justice Department
**Picture:** `GFX: rows` numbered: 1 · HOMICIDES AND SEX CRIMES / 2 · THE POLICE DATABASE FIRST / 3 · INVESTIGATORS IDENTIFY THEMSELVES / 4 · ONLY SITES THAT WARN THEIR USERS / 5 · NO ARREST ON A GENETIC LINK ALONE. Label RECORD. Source "U.S. DOJ Interim Policy, effective Nov 1, 2019". [D32, D33, D35]
> In 2019, the Justice Department wrote rules for federal investigators. Genetic genealogy mainly for homicides and sex crimes, and only after the police database has failed. Investigators must identify themselves, and may only use sites that warn their users. No one may be arrested on a genetic link alone. Going by the Los Angeles Times account, the search that found the Golden State Killer would have broken those rules.

### S42 · The first laws
**Picture:** `GFX: rows` MARYLAND · 2021 · A JUDGE APPROVES EACH SEARCH; RELATIVES CAN REFUSE / MONTANA · 2021 · A WARRANT / UTAH · 2023 · VIOLENT FELONIES AND MISSING PERSONS ONLY. Label RECORD. Sources "Md. Laws 2021 ch. 681 · Mont. Code § 44-6-104 · Utah S.B. 156". [D36, D38, D39]
> Then came the first state laws. Maryland, in 2021: a judge must approve every search, police may only use sites that ask their users' consent, and if a relative refuses to give a sample, police can't secretly take one. Montana, the same year: a warrant or a court order. Utah, in 2023: only for violent felonies and missing or unidentified people.

### S43 · The courts
**Picture:** `GFX: card` RECORD: "There is no privacy interest in commonly held DNA that a relative voluntarily uploads to a public database." State v. Hartman, Washington Court of Appeals, 2023. Then rows: 1988 · *California v. Greenwood* · trash needs no warrant / 2018 · *Carpenter v. United States* · phone location records do. [D42, D44, D45, D46]
> The courts have mostly let it stand. In 2023, an appeals court in Washington State put it bluntly: there is no privacy interest in DNA you share with a relative who uploads it voluntarily. The Supreme Court hasn't ruled on it. Its closest decision, two months after the arrest, said police need a warrant for months of your phone's location records. It didn't mention DNA. And taking his trash needed no warrant at all. The court decided that in 1988.

### S44 · The public
**Picture:** `GFX: chart` Two bars: "VIOLENT CRIMES · 80% SUPPORT" / "NONVIOLENT CRIMES · 39%". Source "Guerrini et al., PLoS Biology 2018 · online survey, May 2018". [D41]
> Most people accept the narrow version. In a 2018 survey, eighty percent supported police using these sites for violent crimes. For nonviolent crimes, thirty-nine percent.

### S45 · Fourth weight
**Picture:** `3D: scale_tip_left` The first pan recovers ground. Lower third "EVIDENCE · EVERY RULE DRAWS THE SAME THREE LINES". [D32–D41]
> So, the fourth weight. Every rule we found, from the Justice Department, from Maryland, Montana and Utah, even from the companies, draws its lines in the same three places: which crimes, who has to agree, and whether a judge signs off. The real argument isn't whether to do this. It's where those lines go.

---

## V. THE VERDICT

### S46 · Act title
**Picture:** `GFX: title` V · THE VERDICT

### S47 · The case for searching
**Picture:** `3D: scale_tip_left` Lower third "THE STRONGEST CASE: LET THEM SEARCH". [E1–E7]
> First, the strongest case for letting police search. Thirteen people were murdered and dozens attacked, and for forty years the law had nothing. This found him, and it has solved more than a thousand cases since. It has freed an innocent man and given names back to the dead. The people who uploaded weren't forced: they chose to share, and now they have to opt in. A cousin can already tell the police about you. Why should a cousin's DNA be different?

### S48 · The case against
**Picture:** `3D: scale_tip_right` Lower third "THE STRONGEST CASE: NOT WITHOUT YOUR CONSENT". [E8–E15]
> Now the strongest case against. You can't opt out of your relatives. When a cousin uploads, part of your genome goes with it, and you were never asked. The rules have changed again and again after people uploaded. The data has been breached and sold, and one warrant overrode a whole database's privacy settings. The method has already fallen on innocent men. And once police can search for murder, the pressure is always to search for less. A power like this is easier to keep narrow before it spreads than after.

### S49 · Verdict one
**Picture:** `GFX: verdict` Kicker THE GOLDEN STATE KILLER. VERDICT: "Catching him this way was right. Doing it in secret, on sites that hadn't warned their users, was not." CONFIDENCE 80%. WHAT WOULD CHANGE OUR MIND: "Evidence that being open about the search at the time would have let him escape."
> Here's our verdict. On the Golden State Killer: catching him this way was right. Doing it in secret, on sites that hadn't warned their users, was not. Thirteen murders justify the search. They don't justify hiding it. Our confidence is eighty percent. What would change our mind: evidence that being open about the search at the time would have let him escape.

### S50 · Verdict two
**Picture:** `GFX: verdict` Kicker THE POLICE. VERDICT: "Yes, but only for murder and rape, with a judge's approval each time, on sites that ask their users first." CONFIDENCE 75%. WHAT WOULD CHANGE OUR MIND: "Evidence that limits like these don't hold: that searches still spread to lesser crimes, or keep falling on innocent relatives."
> On the police: yes, they should be allowed, but only for murder and rape, with a judge's approval each time, and only on sites that ask their users first. Our confidence is seventy-five percent. What would change our mind: evidence that limits like these don't hold in practice, that the searches still spread to lesser crimes or keep falling on innocent relatives.

### S51 · Verdict three
**Picture:** `GFX: verdict` Kicker THE BIGGER QUESTION. VERDICT: "No one can fully consent for a family, so the limits should be set by law, not by whoever owns the database." CONFIDENCE 70%. WHAT WOULD CHANGE OUR MIND: "Evidence that company rules have held steadier, and protected people better, than the laws written to replace them."
> And the bigger question. When one person shares their DNA, who consents for the family? Our verdict: no one can, fully. So the limits shouldn't be left to whoever owns the database this year. They should be set by law. Our confidence is seventy percent, lower, because laws can be weak, and some companies have protected their users better than any statute. What would change our mind: evidence that company rules have held steadier, and protected people better, than the laws written to replace them.

### S52 · The case stays open
**Picture:** `3D: scale_level_loaded` Level, slow orbit, fade toward black.
> That's our verdict. It's open, which means it can change. If you think we got it wrong, make your case in the comments. We'll answer the strongest one in the next episode.

### S53 · Next case
**Picture:** `GFX: words` "NEXT CASE" over black: "THE CENTRAL PARK FIVE · 1989" / *Should police be allowed to lie to suspects?*
> Next case: in 1989, five teenagers in New York confessed on video to an attack in Central Park. Thirteen years later, DNA and another man's confession cleared them. Should police be allowed to lie to the people they question?

### S54 · End card
**Picture:** `GFX: endcard` Title, subscribe area, two end-screen slots. Sources link. No narration.

---

## Pronunciation (applied to narration text only)

Model: eleven_multilingual_v2. Numbers are written out in the narration where the voice could
misread them. Our best guesses, to confirm by ear in the review copy: Maggiore, Witthuhn, Usry
(families' own pronunciations) and GEDmatch ("Jed-match" is how genealogists say it).

| Written | Spoken as |
|---|---|
| DeAngelo | Dee-Ann-jeh-low |
| Maggiore | Muh-jor-ee |
| Witthuhn | Wit-hoon |
| Visalia | Vy-sail-yuh |
| Goleta | Go-lee-tuh |
| Rae-Venter | Ray-Venter |
| Usry | Uss-ree |
| Schubert | Shoo-bert |
| GEDmatch | Jed-match |
| 23andMe | Twenty-three and Me |
| FamilyTreeDNA | Family Tree D N A |

## Sources on screen (description box)

See `research.md`. Every RECORD card carries its citation on screen; the full list goes in the
description, led by the court record (People's Sentencing Memorandum, joint DA releases), Erlich
et al. (*Science* 2018), the DOJ interim policy and the Maryland, Montana and Utah statutes.

## Before recording (from research §G)

- **S22–S24:** read Rae-Venter's *I Know Who You Are* (2023) and Holes's *Unmasked* (2022) for
  their own accounts of which site gave which match; the narration says the point is disputed.
- **S15:** "almost fifty rapes" is the prosecutor's figure in court (via NBC); get the June 29,
  2020 transcript if possible. Patrice Harrington's age (27 vs 28) is not said.
- **S27:** the plea reasons quoted are from the joint release; the transcript pp. 14–15 would add
  detail. We say "dropped the death penalty", not why California wasn't executing anyone.
- **S28:** Temple's letter is known only through the LA Times; keep it attributed.
- **S36:** check the 23andMe transparency report on the day of recording; we say only that it
  "has never handed any customer's data to police", which is its cumulative figure.
- **S41:** check justice.gov for whether the DOJ policy is still interim.
- **S42:** Montana's "or a court order" is the 2025 amendment (investigative subpoena).
- **S06, S31:** "1,182" is Dowdeswell's count to Feb 2024; pull her Dec 2025 dataset for a newer
  dated total if one exists.
- **S53 (next case, chosen 21 Oct 2026):** the Central Park Five. Before recording, check against
  Case 06 research: five teenagers; videotaped statements in 1989; convictions vacated in 2002 after
  Matias Reyes's confession and a DNA match ("thirteen years later"). The teaser says only that.
- **3D:** `car_lot` and `evidence_shelf` are new scenes for `scenes.py` (generic car, no badge or
  plate; plain archive boxes, no case numbers). The Scale clips are reused from Case 01.
