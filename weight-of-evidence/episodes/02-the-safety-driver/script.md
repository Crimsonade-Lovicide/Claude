# Case 02: The Safety Driver

**Question:** When a car that drives itself kills someone, who's guilty?
**Runtime target:** 17–19 min. Narration about 2,800 words.
**Voice:** the same ElevenLabs voice and model as Case 01.

Every factual line traces to `research.md` (IDs in brackets in the picture notes). Picture
notes name the tool that builds each shot:
- `3D:` Blender scene from `production/scenes.py`
- `GFX:` Pillow graphic from `production/gfx.py` / `production/ep02.py`

Narration is the `>` lines only. `production/narration.py` extracts them and applies the
pronunciation table at the bottom.

Care rules for this episode: no depiction of Elaine Herzberg, of Rafaela Vasquez, or of the
impact. The road is a simplified reconstruction; the SUV is generic; the sensor diagram is
rebuilt from the NTSB's table and tagged that way.

---

## COLD OPEN

### S01 · Mill Avenue
**Picture:** `3D: road_push` Driver's-eye push up the right lane at night. Lower third "Tempe, Arizona · MARCH 18, 2018 · 9:58 P.M." Tag RECONSTRUCTION. [A1, A4]
> A little before ten on a Sunday night in March 2018, an SUV was driving north on Mill Avenue in Tempe, Arizona, at about forty-four miles an hour.
> Nobody was steering it. The car was driving itself.

### S02 · Something in the road
**Picture:** `GFX: sensor` Top-down diagram: lanes, the car, a box appearing ahead; label flips VEHICLE → OTHER → VEHICLE → BICYCLE in time with the words. Clock counts from −5.6 s. Tag RECONSTRUCTION FROM NTSB DATA. [B1–B4]
> Five point six seconds before the crash, its radar picked up something in the road ahead. The computer decided it was a vehicle. Then, something else. Then a vehicle again. Then a bicycle.

### S03 · Her
**Picture:** `GFX: words` "Elaine Herzberg, 49." on black. [A7, A1]
> It was a woman. Elaine Herzberg, forty-nine, walking a bicycle across the road.

### S04 · The seat
**Picture:** `3D: road_push` (later section) Hood and pillars in silhouette. [C4]
> In the driver's seat sat a woman paid to watch the road and take over if anything went wrong. For the last six seconds, she was looking down, toward her phone.

### S05 · Thirty-nine
**Picture:** `GFX: words` "39 mph" then black. No sound but a low tone. [A4, A8]
> The car hit Elaine Herzberg at thirty-nine miles an hour. She died at the scene.

### S06 · Who answered
**Picture:** `GFX: timeline` Three entries drop in: MARCH 2018 · UBER SETTLES WITH FAMILY / MARCH 2019 · NO CHARGES FOR UBER / AUGUST 2020 · SAFETY DRIVER CHARGED. [D13, D14, D15]
> Ten days later, Uber settled with her family. A year later, a prosecutor decided there was no basis to charge Uber with a crime. Two years after that, the woman in the driver's seat was charged with negligent homicide.

### S07 · The question
**Picture:** `3D: scale` The Scale, empty and level.
> So when a car is driving itself, who's guilty? The person who was supposed to be watching? The company that built the system and put her there? Or, as cars lose their drivers altogether, no one at all?

### S08 · The promise
**Picture:** `GFX: words` White words, "how sure" in brass.
> We went through the federal crash investigation, the court records, and the research on what happens to human attention when a machine does the driving. At the end, we'll give you a verdict, and tell you how sure we are.

### S09 · Title
**Picture:** `GFX: title` WEIGHT OF EVIDENCE · CASE 02 / THE SAFETY DRIVER / *When the machine kills, who's guilty?* No narration; music hit.

---

## I. THE MACHINE

### S10 · Act title
**Picture:** `GFX: title` I · THE MACHINE

### S11 · The test car
**Picture:** `3D: car_orbit` Generic SUV, slow orbit, roof lidar spinning. Tag "GENERIC VEHICLE · SIMPLIFIED". [A1, B16, C9]
> The car was a Volvo XC ninety that Uber's self-driving unit, the Advanced Technologies Group, had fitted with its own computers, cameras, radar, and a spinning laser scanner on the roof. It was testing on public roads, at night, with one person inside.

### S12 · The record
**Picture:** `GFX: document` NTSB title block: "Collision Between Vehicle Controlled by Developmental Automated Driving System and Pedestrian · Tempe, Arizona · March 18, 2018 · NTSB/HAR-19/03". [NTSB]
> The National Transportation Safety Board spent twenty months on this crash. Its report is the closest thing we have to a full record of what the car knew, and when it knew it.

### S13 · What it saw
**Picture:** `GFX: sensor` Full diagram with the table building alongside: −5.6 VEHICLE · −5.2 OTHER · −4.2 VEHICLE · −2.6 BICYCLE · −1.5 OTHER · −1.2 BICYCLE. Predicted path arrows point along the lanes, never across. [B1–B6]
> Here's what the record shows. At five point six seconds out, the car detected her, about three hundred and fifty feet ahead, and called her a vehicle. Then, other. Then vehicle, other, vehicle again. At two point six seconds, a bicycle. At one point five, other. At one point two, a bicycle again, now in the car's lane.

### S14 · Why it never understood
**Picture:** `GFX: document` NTSB excerpt, three highlighted lines: "…it no longer considered the tracking history of that object…" / "…were not assigned goals." / "Pedestrians outside the vicinity of a crosswalk were also not assigned an explicit goal." [B9]
> Every time the label changed, the system threw away what it had learned about where she was going. And it gave no predicted goal to objects labelled other, or to pedestrians away from a crosswalk. So it never worked out that she was crossing the road.

### S15 · Saw, not understood
**Picture:** `GFX: words` "It saw her for 5.6 seconds. / It never understood what it was seeing." [B11]
> It saw her for five point six seconds. It never understood what it was seeing.

### S16 · One second
**Picture:** `GFX: sensor` Clock reaches −1.2 s; the word ACTION SUPPRESSION fills the frame edge in red; a one-second bar fills; no alert icon lights. [B6]
> At one point two seconds, the system finally recognised an emergency. Then it did something on purpose. It waited. For one full second it held back from braking, a feature Uber called action suppression, meant to avoid false alarms. It didn't warn the driver.

### S17 · Two tenths
**Picture:** `GFX: sensor` Clock at −0.2 s: ALERT lights; the car's speed readout barely moves. [B7]
> With two tenths of a second left, it sounded an alert and began to slow down, gently. It wasn't designed to brake hard just to make a crash less severe.

### S18 · The brake that was switched off
**Picture:** `GFX: card` RECORD: "In Volvo's simulations, its own emergency braking avoided the collision in 17 of 20 variations." Source: NTSB/HAR-19/03, Volvo simulation. [B12, B13]
> The Volvo came with its own emergency braking, the kind sold on the showroom floor. Uber switched it off whenever its own system was driving, because the two systems could interfere with each other. When Volvo later simulated that night, its braking alone avoided the crash in seventeen of twenty versions.

### S19 · First weight
**Picture:** `3D: scale_tip_left` One pan drops. Lower third "EVIDENCE · THE SYSTEM SAW HER AND DID NOT UNDERSTAND".
> So, the first weight on the scale. A system that saw a person and didn't understand her. A design that waited before braking, without a word to the driver. And a safety net that had been taken out.

---

## II. THE SAFETY DRIVER

### S20 · Act title
**Picture:** `GFX: title` II · THE SAFETY DRIVER

### S21 · Seventy-three times
**Picture:** `3D: road_push` Slower section. Caption "ROUTE DRIVEN 73 TIMES IN AUTONOMOUS MODE". [C1]
> The person in the driver's seat was Rafaela Vasquez, forty-four. She had worked for Uber's testing program since June 2017, and she had driven this exact route in autonomous mode seventy-three times.

### S22 · Two became one
**Picture:** `GFX: card` RECORD: "During September–October 2017, ATG consolidated the responsibilities of two vehicle operators into that of a single operator." Source NTSB. [C9]
> When she started, Uber's test cars carried two people. In the fall of 2017, Uber merged the two jobs into one. The safety board notes it let the company put more cars on the road.

### S23 · Looking down
**Picture:** `GFX: gaze` A 31.5-minute strip; 34% of it shaded "LOOKING DOWN"; markers for the longest look (26.5 s) and the 23 glances in the last three minutes. [C2, C3]
> The car had a camera pointed at her. Over thirty-one and a half minutes of driving, she spent about a third of the time looking down toward the bottom of the center console, where her phone was. Her longest look lasted twenty-six and a half seconds. In the final three minutes, she looked down twenty-three times.

### S24 · The show
**Picture:** `GFX: card` RECORD: "…the account belonging to the vehicle operator was continually streaming a television show between 9:16 p.m. and 9:59 p.m." Source NTSB. Small INFERENCE line: "Police: The Voice, on Hulu." [C5, C6, C7]
> Records showed her account streaming a television show for the entire trip. Police said it was The Voice, on Hulu. She told investigators she had been looking at Uber's tablet. The tablet's data showed no activity near the crash.

### S25 · Time enough
**Picture:** `GFX: document` NTSB excerpt with highlight on "she would likely have had sufficient time to detect and react". [C8]
> The safety board's conclusion was blunt. If she had been watching, she would have had two to four seconds, likely enough to avoid the crash, or soften it.

### S26 · The charge
**Picture:** `GFX: timeline` AUGUST 27, 2020 · INDICTED · NEGLIGENT HOMICIDE / JULY 28, 2023 · PLEADS GUILTY · ENDANGERMENT · 3 YEARS PROBATION. [D15, D16]
> In 2020, a grand jury indicted her for negligent homicide. In 2023, she pleaded guilty to a lesser charge, endangerment, and was sentenced to three years of supervised probation.

### S27 · The prosecutor
**Picture:** `GFX: card` RECORD: "Regardless of whatever technology might be available to drivers, safety for everyone on the street and in the vehicle must always be a driver's first priority." Rachel Mitchell, Maricopa County Attorney, 2023. [D17]
> The county attorney put it this way. Whatever technology is in the car, safety has to be the driver's first priority.

### S28 · The case against her
**Picture:** `GFX: card` ARGUMENT: "We punish a man for his very ignorance, if he is thought responsible for the ignorance." Aristotle, Nicomachean Ethics, Book III. [E11]
> And that looks simple. She had one job. Her employer banned phones. She chose to watch a show, at night, at forty miles an hour. Aristotle drew this line twenty-four centuries ago. We excuse what's done in ignorance, unless you're responsible for the ignorance. A drunk driver isn't excused for what he didn't notice. Neither is someone looking at a phone.

### S29 · The clock test
**Picture:** `GFX: clock` A clock face whose hand steps once a second, occasionally jumping double; a tally of misses grows as the minutes pass. Tag ILLUSTRATION. [E1]
> Except there's a problem with the job itself. In 1948, a British psychologist, Norman Mackworth, sat people in front of a clock whose hand ticked forward once a second, and now and then jumped twice. Their job was to catch the double jumps. Within half an hour, they were missing more of them.

### S30 · Hard work
**Picture:** `GFX: card` RECORD: "vigilance requires hard mental work and is stressful." Warm, Parasuraman & Matthews, Human Factors, 2008. [E4]
> It isn't laziness. Later research found that watching for something rare is hard, stressful work, and attention drains away under it, even in people who are trying.

### S31 · The irony
**Picture:** `GFX: card` RECORD: "…it is impossible for even a highly motivated human being to maintain effective visual attention towards a source of information on which very little happens, for more than about half an hour." Lisanne Bainbridge, "Ironies of Automation," 1983. [E2]
> In 1983, the psychologist Lisanne Bainbridge called this one of the ironies of automation. It's impossible, she wrote, for even a highly motivated person to keep watching something where very little happens, for more than about half an hour.

### S32 · The board knew
**Picture:** `GFX: document` NTSB excerpt: "When it comes to the human capacity to monitor an automation system for its failures, research findings are consistent—humans are very poor at this task." [D6]
> The safety board knew this too. In the same report that named her distraction as the probable cause, it wrote that research findings are consistent: humans are very poor at this task.

### S33 · Google saw it first
**Picture:** `3D: road_push` from the start, slower. Caption "GOOGLE · 2013 TESTS". [E7]
> Google learned the same thing in 2013, filming its own employees in early self-driving tests. Some napped. Some put on makeup at highway speed. Google concluded that handing control back to a human was the weak point, and set out to build cars with no driver at all.

### S34 · The crumple zone
**Picture:** `GFX: card` ARGUMENT: "…the moral crumple zone protects the integrity of the technological system, at the expense of the nearest human operator." Madeleine Clare Elish, 2019. [E8]
> The researcher Madeleine Clare Elish has a name for what happens next. A moral crumple zone. A car's crumple zone takes the force of a crash to protect the people inside. A moral crumple zone is a person who takes the blame to protect the system.

### S35 · Second weight
**Picture:** `3D: scale_swing` The pans see-saw. Lower third "EVIDENCE · A REAL CHOICE, IN A JOB BUILT TO FAIL".
> So, the second weight. She made a real choice, and it was the wrong one. But she made it in a job that people are known to fail, alone, in a car whose makers had taken away her partner and her warning.

---

## III. THE COMPANY

### S36 · Act title
**Picture:** `GFX: title` III · THE COMPANY

### S37 · Probable cause
**Picture:** `GFX: document` NTSB probable cause paragraph; highlight moves from "the failure of the vehicle operator" to "all a consequence of its inadequate safety culture." [D1, D2]
> Here's the safety board's formal finding. The probable cause was the operator's failure to monitor the road, because she was distracted by her phone. Contributing were Uber's inadequate safety risk assessment, its ineffective oversight of operators, and its lack of any adequate way to deal with automation complacency. All of it, the board wrote, a consequence of its inadequate safety culture.

### S38 · What wasn't there
**Picture:** `GFX: list` Five lines strike in: NO SAFETY DIVISION / NO DEDICATED SAFETY MANAGER / NO FORMAL SAFETY PLAN / NO STANDARD OPERATING PROCEDURES / NO FATIGUE POLICY. Source NTSB. [D5]
> At the time of the crash, Uber's testing unit had no safety division, no dedicated safety manager, no formal safety plan, and no standard operating procedures.

### S39 · The footage
**Picture:** `GFX: card` RECORD: "…had the means to retroactively monitor the behavior of vehicle operators and their adherence to operational procedures, it rarely did so." NTSB finding 13. [C10, C11]
> It had a camera on every operator, and in the ten months before the crash it had caught eighteen of them using their phones. But it rarely looked at the footage. There's no evidence anyone reviewed hers.

### S40 · Thirteen miles
**Picture:** `GFX: card` INFERENCE: "Uber's cars were struggling to drive 13 miles between human interventions." Source: The New York Times, March 2018. [B18]
> And according to reporting at the time, in the weeks before the crash its cars were struggling to drive thirteen miles without a human stepping in.

### S41 · No basis
**Picture:** `GFX: card` INFERENCE (letter as reported): "…no basis for criminal liability for the Uber corporation…" Yavapai County Attorney Sheila Polk, March 2019. [D14]
> None of that became a criminal case. In March 2019, the prosecutor reviewing it wrote that there was no basis for criminal liability for the Uber corporation.

### S42 · Why companies aren't charged
**Picture:** `GFX: words` "A company can be charged. It almost never is." [F11]
> That's less strange than it sounds. An American company can be charged with a crime; that's been settled since 1909. But homicide usually needs a guilty mind, a recklessness you can pin on someone. A design decision spread across a hundred engineers is hard to pin on anyone. And the only punishment a court can give a company is a fine.

### S43 · It has been tried
**Picture:** `GFX: timeline` 1978 · INDIANA CHARGES FORD (PINTO) · 1980 · ACQUITTED / 2020 · PG&E PLEADS GUILTY · 84 COUNTS OF MANSLAUGHTER. [F12, F13]
> It has been tried. In 1978, Indiana charged Ford with reckless homicide over the Pinto, the first time a carmaker was prosecuted over crash deaths. Ford was acquitted in 1980. And in 2020, the California utility P G and E pleaded guilty to eighty-four counts of manslaughter over a wildfire. So it's possible. It just almost never happens.

### S44 · Other hands
**Picture:** `GFX: card` RECORD: "…the business friendly and low regulatory environment…" Arizona Executive Order 2018-04, March 1, 2018. [D9, D10, D11]
> There were other hands on the scale. Arizona had openly courted Uber's testing, and its rules required no application at all. Seventeen days before the crash, the governor signed a new order praising the state's business friendly and low regulatory environment. The safety board faulted the state's oversight too.

### S45 · The crossing
**Picture:** `3D: road_median` Slow push toward the median sign "USE CROSSWALK" and the brick X. Tag RECONSTRUCTION. [A3, D3, D4, C8, B1]
> And the board named one more factor. Elaine Herzberg crossed outside a crosswalk, from a median whose brick paving looked like a path but was posted with signs telling people not to cross there. Her blood showed methamphetamine at a level that indicated impairment. That's in the record, and it counts. It doesn't change what the record also says: an attentive driver would likely have seen her in time, and the car saw her for five point six seconds.

### S46 · Third weight
**Picture:** `3D: scale_tip_right` The other pan drops. Lower third "EVIDENCE · THE DECISIONS THAT SET IT UP".
> So, the third weight. Ten days after the crash, Uber settled with her family. It shut down its testing in Arizona, and in 2020 it sold the whole unit. The only person who ever answered to a criminal court was the one in the driver's seat.

---

## IV. NO ONE AT THE WHEEL

### S47 · Act title
**Picture:** `GFX: title` IV · NO ONE AT THE WHEEL

### S48 · Now
**Picture:** `GFX: stat` "400,000+" counts up, "RIDES A WEEK · NO ONE IN THE DRIVER'S SEAT" · source line "Waymo, February 2026". [F14, F15]
> That was 2018, with a human in the seat. Today, Waymo says it gives more than four hundred thousand rides a week with nobody in the driver's seat at all, and Tesla runs robotaxis without safety drivers in Austin and several other cities.

### S49 · Cruise
**Picture:** `GFX: card` RECORD: "…attempted to pull over to the side of the road with the woman underneath it, dragging the woman over 20 feet." U.S. Attorney, N.D. Cal., 2024. [F2, F3]
> So what happens when one of those cars hurts someone? In October 2023, a driverless Cruise car in San Francisco ran over a woman who'd been thrown into its path by a human driver, then tried to pull over, dragging her more than twenty feet. She survived. It's the only criminal case against a self-driving company we could find, and it wasn't for hurting her. It was for leaving the dragging out of a report to regulators. Cruise paid a five hundred thousand dollar fine.

### S50 · Drivers and juries
**Picture:** `GFX: compare` Two columns. DRIVER: "Tesla Autopilot crash, 2019 · driver pleads no contest to vehicular manslaughter". COMPANY: "Benavides v. Tesla, 2025 · jury: Tesla 33% at fault · ~$243M · on appeal". [F1, F5]
> With driver assistance, the pattern holds. In California, a man whose Tesla was on Autopilot when it killed two people pleaded no contest to vehicular manslaughter. The company has faced civil juries instead. In 2025, a federal jury in Miami found Tesla's Autopilot defective and Tesla thirty-three percent at fault for a fatal crash, about two hundred and forty-three million dollars. Tesla is appealing.

### S51 · Considered the driver
**Picture:** `GFX: document` A.R.S. §28-9702(E): "When engaged, the automated driving system is considered the driver or operator of the autonomous vehicle for the purpose of assessing compliance with applicable traffic or motor vehicle laws." Highlight "for the purpose of assessing compliance with applicable traffic". [F7, F8]
> Arizona's law now says that when the system is engaged, the system is considered the driver. But only for traffic laws. It can get a ticket. Nothing in it says who answers for a death.

### S52 · Britain
**Picture:** `GFX: document` Automated Vehicles Act 2024, s.47 heading "User-in-charge not liable for manner of driving" and s.25 "…imprisonment for a term not exceeding 14 years…". Footer "Not yet in force · planned 2027". [F9]
> Britain has gone further. Under its Automated Vehicles Act, the person in the seat of a self-driving car commits no offence for the way it drives. Responsibility moves to a company that has to be authorised in advance, and hiding safety information when someone is killed can carry up to fourteen years in prison. Those parts aren't in force yet. The plan is 2027.

### S53 · The gap
**Picture:** `GFX: card` ARGUMENT: "…not one problem but a set of at least four interconnected problems…" Santoni de Sio & Mecacci, 2021. Small line: "the responsibility gap" (Matthias, 2004). [E9, E10]
> Philosophers call the hole in between a responsibility gap. When a machine acts, the people who built it can say they couldn't predict it, and the person beside it can say they couldn't control it. The fix most of them propose is easy to say and hard to do. Whoever really controls the system has to be the one who answers for it.

---

## V. THE VERDICT

### S54 · Act title
**Picture:** `GFX: title` V · THE VERDICT

### S55 · The case against the driver
**Picture:** `3D: scale_tip_right` Lower third "THE STRONGEST CASE: THE DRIVER IS GUILTY".
> First, the strongest case against the safety driver. She was the last line of defence, she knew it, and she chose a TV show. The safety board says she had time. If we excuse her, we tell every safety driver that the job is optional.

### S56 · The case for her
**Picture:** `3D: scale_tip_left` Lower third "THE STRONGEST CASE: THE SYSTEM IS GUILTY".
> Now the strongest case for her. She was one person doing a job built for two, at night, after more than half an hour of nothing happening, in a car that didn't warn her, wouldn't brake hard, and had its factory braking switched off. The research says nearly everyone fails that job sooner or later. She was the most visible failure in a system full of them.

### S57 · Verdict one
**Picture:** `GFX: verdict` VERDICT: "The safety driver: responsible, but not the main cause. Endangerment fits. Homicide would not have." CONFIDENCE 75%. WHAT WOULD CHANGE OUR MIND: "Evidence she had been warned the system failed on that stretch of road, and looked away anyway."
> Here's our verdict. Rafaela Vasquez was responsible, and the plea fits. She endangered people by choosing her phone over a job she knew mattered. But she was not the main cause of Elaine Herzberg's death, and a homicide conviction would have made her exactly what Elish describes, the crumple zone. Our confidence is seventy-five percent. What would change our mind: evidence that she had been warned the system failed on that stretch of road, and looked away anyway.

### S58 · Verdict two
**Picture:** `GFX: verdict` VERDICT: "Uber carried the larger share of the blame, and the law had no tool to say so." CONFIDENCE 80%. WHAT WOULD CHANGE OUR MIND: "Evidence those choices were industry standard, signed off by independent safety reviewers."
> On the company. Uber made the decisions that turned one person's lapse into a death. One operator instead of two. A deliberate second of delay with no warning. The factory brakes switched off. Footage nobody watched. Morally, Uber carries the larger share. The prosecutor may still have been right that criminal law, as written, couldn't reach it. That's the problem. Our confidence is eighty percent. What would change our mind: evidence that those choices were standard across the industry and signed off by independent safety reviewers. Then the failure belongs to the whole industry, not one company.

### S59 · Verdict three
**Picture:** `GFX: verdict` VERDICT: "With no one at the wheel, the company running the system stands where the driver stood, answerable in criminal court." CONFIDENCE 65%. WHAT WOULD CHANGE OUR MIND: "Evidence that criminal liability makes companies hide failures instead of fixing them."
> And the bigger question. When no one is behind the wheel, who's guilty? Our verdict: the company that runs the system should stand where the driver used to stand, answerable in criminal court for how its cars drive, the way Britain is about to try. Blame should follow control, and control now sits with the company. Our confidence is lower, sixty-five percent, because there's a real argument on the other side. Aviation got safer partly by investigating crashes without hunting for someone to punish, so that people report their mistakes. What would change our mind: evidence that criminal liability makes companies hide failures instead of fixing them. Cruise, which hid one, is a warning in both directions.

### S60 · The case stays open
**Picture:** `3D: scale_level_loaded` Level, slow orbit, fade toward black.
> That's our verdict. It's open, which means it can change. If you think we got it wrong, make your case in the comments. We'll answer the strongest one in the next episode.

### S61 · Next case
**Picture:** `GFX: words` "NEXT CASE" over black: "The Mignonette · 1884."
> Next case: four men in a lifeboat in 1884, nearly three weeks adrift, and a seventeen-year-old cabin boy. Is killing to survive murder?

### S62 · End card
**Picture:** `GFX: endcard` Title, subscribe area, two end-screen slots. Sources link. No narration.

---

## Pronunciation (applied to narration text only)

Model: eleven_multilingual_v2. Numbers are written out in the narration so the voice can't
misread them.

| Written | Spoken as |
|---|---|
| Herzberg | Hertzberg |

## Sources on screen (description box)

See `research.md`. Every RECORD card carries its citation on screen; the full list goes in the
description, led by the NTSB report HAR-19/03.
