# Research: Case 02, The Safety Driver

**Question:** When a car that drives itself kills someone, who's guilty?
**Anchor:** Tempe, Arizona, Sunday March 18, 2018, 9:58 p.m. An Uber Advanced Technologies
Group (ATG) test vehicle in autonomous mode struck and killed Elaine Herzberg, 49.
**Bigger question:** As cars lose their drivers, who is left to blame, and should blame
follow the person nearest the machine or the people who designed it?

Tags: `RECORD` = in a primary source (NTSB report, court filing, statute, government release,
the paper itself). `INFERENCE` = reliable press or secondary sources, or our reasoning from the
record. `UNCERTAIN` = sources disagree or unverified; don't state on screen without the hedge
shown. Researched 12 Oct 2026.

Before air, spot-check every on-screen quote against the page cited.

**Names.** Elaine Marie Herzberg (indictment). The operator: court papers use "Rafael Stuart
Vasquez, aka Rafaela Vasquez"; the Maricopa County Attorney's 2023 release uses Rafaela and
she/her. **We say Rafaela Vasquez, she/her.**

---

## Primary sources

- **[NTSB]** NTSB, *Collision Between Vehicle Controlled by Developmental Automated Driving
  System and Pedestrian, Tempe, Arizona, March 18, 2018*, Highway Accident Report NTSB/HAR-19/03,
  adopted Nov 19, 2019. https://www.ntsb.gov/investigations/AccidentReports/Reports/HAR1903.pdf
- **[NTSB-P]** NTSB preliminary report, May 2018 (superseded; use [NTSB] for numbers).
- **[IND]** Maricopa County grand jury indictment, Aug 27, 2020.
  https://maricopacountyattorney.org/DocumentCenter/View/1724/Rafael-Vasquez-GJ-Indictment ·
  release https://maricopacountyattorney.org/CivicAlerts.aspx?AID=751
- **[PLEA]** Plea agreement, July 28, 2023, CR2020-001853-001.
  https://maricopacountyattorney.org/DocumentCenter/View/2780/Rafaela-Vasquez-Plea-Agreement ·
  release https://maricopacountyattorney.org/CivicAlerts.aspx?AID=1012
- **[8K]** Uber 8-K, Dec 7, 2020 (sale of ATG to Aurora).
  https://www.sec.gov/Archives/edgar/data/1543151/000155278120000598/e20603_uber-8k.htm

---

## A. The night (what happened)

| # | Claim | Tag | Source |
|---|---|---|---|
| A1 | Sunday March 18, 2018, 9:58 p.m.; modified 2017 Volvo XC90 run by Uber ATG; "struck a pedestrian walking midblock across the northbound lanes of N. Mill Avenue in Tempe" | RECORD | NTSB p.1 |
| A2 | About 400 ft south of Curry Road; no crosswalk. Nearest crosswalks 380 ft north (Curry Rd) and 2,700 ft south | RECORD | NTSB pp.3–5 (preliminary said 360 ft; use 380) |
| A3 | She crossed from a 71-ft-wide median with an X-shaped red-brick design that "had the appearance of a pathway"; four signs on the median said not to cross / USE CROSSWALK. After the crash Tempe replaced the brick with rock | RECORD | NTSB pp.3–5 |
| A4 | Posted speed limit 45 mph. ~44 mph at first detection; impact at about 39 mph | RECORD | NTSB p.3; table pp.15–16 |
| A5 | "35 mph zone / speeding" (early press) is wrong: the limit was 45; the car sped up from 35 mph 9.9 s out "in response to increased speed limit" | RECORD | NTSB table |
| A6 | Night, dry, street-lit; 5 of 6 nearby lights working. "the nighttime visibility in the area was considerably greater than depicted on the video recording" | RECORD | NTSB pp.3, 17, 25 |
| A7 | She was walking east, pushing a bicycle at her left side; looked toward the SUV about 1 s before impact | RECORD | NTSB pp.1, 7–8, 17 |
| A8 | She "died on scene from multiple blunt force injuries" (early press said hospital) | RECORD | NTSB p.2 |
| A9 | Friends: she had struggled with homelessness and "was trying to get her life back and was succeeding with it" | INFERENCE | CBS News 2018 (friend Deniel Klapthor) |
| A10 | Widely described as the first pedestrian killed by a self-driving test vehicle. The NTSB does not say "first" | INFERENCE | press; say "widely described as" |
| A11 | Early police claim it would have been "difficult to avoid… based on how she came from the shadows" (Chief Moir, Mar 2018) was contradicted by the NTSB and by Tempe PD's own later report ("entirely avoidable") | RECORD (NTSB) / INFERENCE (police quotes via press) | KTAR Mar 21 2018; TechCrunch Jun 22 2018 |

## B. The machine (what the system did)

All RECORD, NTSB Executive Summary, §1.5.5 and the table on pp.15–16 unless noted.

| # | Time to impact | What the system did |
|---|---|---|
| B1 | −5.6 s | First detection (radar), classified **vehicle**. She was ~350 ft ahead. "Although the ADS continued to track the pedestrian until the crash, it never accurately classified her as a pedestrian or predicted her path." |
| B2 | −5.2 s | Lidar: **other**, predicted static |
| B3 | −4.2 to −2.7 s | **vehicle**, then alternating vehicle / other; path static or "left through lane" |
| B4 | −2.6 s | **bicycle**, static; −2.5 s bicycle, left through lane |
| B5 | −1.5 s | **other**, partly in the SUV's lane; plans to steer around it |
| B6 | −1.2 s | **bicycle**, in the SUV's lane. Emergency declared; **action suppression** begins: a 1-second hold on braking. "No alert was given to the operator when action suppression was initiated." ATG did it "because of concerns about false alarms" |
| B7 | −0.2 s | Suppression ends; auditory alert; plan to slow gradually. "the ADS was not designed to apply maximum braking only to lessen the severity of a collision" |
| B8 | −0.02 s | Operator grabs the wheel (39 mph); brakes 0.7 s after impact |

| # | Claim | Tag | Source |
|---|---|---|---|
| B9 | Why it never predicted her path: "If the perception process changed the classification of a detected object, it no longer considered the tracking history of that object." "other" objects "were not assigned goals." "Pedestrians outside the vicinity of a crosswalk were also not assigned an explicit goal." | RECORD | NTSB p.13 |
| B10 | "the system design did not include consideration for jaywalking pedestrians" | RECORD | NTSB p.16 |
| B11 | "The car never saw her" is wrong: it saw her for 5.6 s and never understood what she was | RECORD | B1 |
| B12 | Volvo's factory forward collision warning and automatic emergency braking (City Safety) were automatically deactivated whenever the ATG system drove, because the two radars shared frequencies and the brake module couldn't arbitrate two braking commands | RECORD | NTSB §1.6.3 |
| B13 | Volvo's simulation: FCW would have alerted 2.5 s out; AEB would have activated 1.4 s out and avoided the collision in 17 of 20 variations (the other 3: impact under 10 mph) | RECORD (Volvo's simulation, as reported by NTSB) | NTSB pp.21–22 |
| B14 | NTSB finding: deactivating Volvo's FCW/AEB "without replacing their full capabilities removed a layer of safety redundancy" | RECORD | NTSB finding 7 |
| B15 | ADS could brake up to 0.71 g, only when that would avoid the crash | RECORD | NTSB p.13 fn.33 |
| B16 | Single roof lidar (software "Krypton"); no sensor faults | RECORD | NTSB |
| B17 | After the crash ATG kept tracking history across reclassification, added jaywalking as a pedestrian goal, dropped action suppression; its simulation says the new software would have classified her as a pedestrian 4.5 s (~290 ft) out | RECORD (ATG claim via NTSB) | NTSB §1.9.1 |
| B18 | Uber's cars were struggling to reach 13 miles between interventions in Arizona (Mar 2018); Waymo reported ~5,600 miles per disengagement in California, 2017. Not standardised safety measures | INFERENCE | NYT Mar 23 2018 via CNBC/Inverse; CA DMV filings |
| B19 | ATG had gone from seven lidars (Ford Fusions) to one (Volvos) | UNCERTAIN | Reuters 2018 via secondary copies; don't use on screen |

## C. The operator

| # | Claim | Tag | Source |
|---|---|---|---|
| C1 | 44; at ATG since June 2017; had driven this route 73 times in autonomous mode | RECORD | NTSB §1.7.2 |
| C2 | Over the 31.5 minutes the car moved she spent 34% of the time looking down toward the bottom of the center console, where her phone was; longest continuous look 26.5 s | RECORD | NTSB pp.17–18 |
| C3 | Last ~3 minutes: looked down 23 times; longest 6.9 s | RECORD | NTSB |
| C4 | "The operator began glancing down toward the bottom of the center console 6 seconds before impact, where she retained her gaze for the next 5 seconds. She returned her gaze to the road about 1 second before impact." | RECORD | NTSB |
| C5 | Her account "was continually streaming a television show between 9:16 p.m. and 9:59 p.m." (NTSB doesn't name the show) | RECORD | NTSB p.24 |
| C6 | Police: The Voice, on Hulu | INFERENCE | Tempe PD report via TechCrunch, Jun 22 2018 |
| C7 | She told the NTSB her phone was in her purse and she'd been using the Uber tablet; tablet data show no interaction near the crash | RECORD | NTSB p.24, fn.55 |
| C8 | NTSB: "had the vehicle operator been attentive, she would likely have had sufficient time to detect and react to the crossing pedestrian to avoid the crash or mitigate the impact" (2 to 4 seconds to detect and respond) | RECORD | NTSB p.47 |
| C9 | ATG consolidated two operators into one in Sept–Oct 2017; it "allowed the company to increase the number of test vehicles" | RECORD | NTSB §1.8.4 |
| C10 | Uber's rules banned phone use. Spot-checks of the inward camera were "infrequent"; Apr 2017–Feb 2018 ATG caught 18 operators violating the phone policy (9 retrained, 9 fired). No evidence anyone reviewed her video before the crash | RECORD | NTSB pp.27–28 |
| C11 | Finding 13: ATG "had the means to retroactively monitor the behavior of vehicle operators… it rarely did so" | RECORD | NTSB |
| C12 | Her pay record included a performance reward for Q4 2017 | RECORD | NTSB (per research agent) — verify page before use |

## D. The findings and the law (Tempe)

| # | Claim | Tag | Source |
|---|---|---|---|
| D1 | **Probable cause:** "the failure of the vehicle operator to monitor the driving environment and the operation of the automated driving system because she was visually distracted throughout the trip by her personal cell phone." | RECORD | NTSB p.59 |
| D2 | **Contributing:** ATG's "(1) inadequate safety risk assessment procedures, (2) ineffective oversight of vehicle operators, and (3) lack of adequate mechanisms for addressing operators' automation complacency—all a consequence of its inadequate safety culture." | RECORD | NTSB p.59 |
| D3 | **Further contributing:** "(1) the impaired pedestrian's crossing of N. Mill Avenue outside a crosswalk, and (2) the Arizona Department of Transportation's insufficient oversight of automated vehicle testing." | RECORD | NTSB p.59 |
| D4 | Toxicology: methamphetamine at a level that "strongly indicates impairment and chronic misuse"; negative for alcohol | RECORD | NTSB pp.22, 36 |
| D5 | ATG at the time: no safety division, no dedicated safety manager, no formal safety plan, no standard operating procedures, no fatigue policy | RECORD | NTSB |
| D6 | The NTSB on monitoring: "When it comes to the human capacity to monitor an automation system for its failures, research findings are consistent—humans are very poor at this task." The distraction was "a typical effect of automation complacency" | RECORD | NTSB (cites Parasuraman & Manzey 2010) |
| D7 | Vice Chairman Landsberg: "Automation performs remarkably well most of the time and therein lies the problem. Human attention span is limited, and we are notoriously poor monitors." He also: "everyone has some responsibility" | RECORD | NTSB p.63, concurring statement |
| D8 | Chairman Sumwalt at the board meeting: "Anybody's crash is everybody's crash." | INFERENCE | Arizona Republic, Nov 19 2019 |
| D9 | Arizona: EO 2015-09 required no application; EO 2018-04 (Mar 1, 2018, 17 days before the crash) added nothing safety-specific for cars with a person inside. NTSB finding 18 faults the state | RECORD | NTSB; EO 2018-04 https://azgovernor.gov/sites/default/files/related-docs/eo2018-04_1.pdf |
| D10 | EO 2018-04 preamble cites "the business friendly and low regulatory environment." | RECORD | EO 2018-04 |
| D11 | Dec 2016 press release: "Governor Ducey Tells Uber 'CA May Not Want You, But AZ Does'" | INFERENCE | title seen; page 403 |
| D12 | Mar 26, 2018: governor suspends Uber's testing; letter calls the crash "an unquestionable failure to comply with this expectation" | RECORD (suspension, NTSB §1.9) / INFERENCE (letter via AP) | |
| D13 | Uber settled with Herzberg's husband and daughter Mar 28, 2018, ten days after; terms undisclosed | INFERENCE | Reuters/AP via NBC Mar 29 2018 |
| D14 | Yavapai County Attorney Sheila Polk (Maricopa had a conflict) found "no basis for criminal liability for the Uber corporation" (letter released Mar 5, 2019) | INFERENCE (letter not found; consistent press) | KTAR; AP |
| D15 | Aug 27, 2020: Vasquez indicted for **negligent homicide**, class 4 felony | RECORD | [IND] |
| D16 | July 28, 2023: pleaded guilty to **endangerment**, class 6 undesignated; **3 years supervised probation**; misdemeanor only if probation completed | RECORD | [PLEA] |
| D17 | County Attorney Rachel Mitchell: "Getting behind the wheel of a car is a serious responsibility. Regardless of whatever technology might be available to drivers, safety for everyone on the street and in the vehicle must always be a driver's first priority." | RECORD | release AID=1012 |
| D18 | Uber resumed testing Dec 2018 in Pittsburgh: 1-mile loop, 25 mph, two operators, driver monitoring, Volvo AEB on | RECORD | NTSB §1.9 |
| D19 | Dec 7, 2020: Aurora acquires ATG; Uber invests $400M in Aurora | RECORD | [8K] |

## E. Human factors and responsibility

| # | Claim | Tag | Source |
|---|---|---|---|
| E1 | Mackworth (1948) clock test: watchers miss more signals as a watch goes on; the decline appears within the first half hour. **Exact % unverified; don't state a number** | RECORD (paper metadata) / INFERENCE (size) | Q J Exp Psychol 1:6–21; Klein & Feltmate 2025 Frontiers review |
| E2 | Bainbridge (1983): "it is impossible for even a highly motivated human being to maintain effective visual attention towards a source of information on which very little happens, for more than about half an hour." | RECORD | "Ironies of Automation," Automatica 19(6):775–779 |
| E3 | Bainbridge: "the designer who tries to eliminate the operator still leaves the operator to do the tasks which the designer cannot think how to automate." | RECORD | same |
| E4 | Warm, Parasuraman & Matthews (2008): "vigilance requires hard mental work and is stressful" | RECORD | Human Factors 50(3):433–441 |
| E5 | Parasuraman & Manzey (2010): complacency "is found in both naive and expert participants and cannot be overcome with simple practice" | RECORD | Human Factors 52(3):381–410 |
| E6 | Takeover times in lab studies of non-critical handovers: 1.9 to 25.7 s (Eriksson & Stanton 2017) | RECORD (abstract) / INFERENCE (numbers via Southampton release) | Human Factors 59(4) |
| E7 | Google's own 2013 tests: employees napped, used phones, did makeup at highway speed; Google dropped driver-assist handover for full autonomy | INFERENCE | Waymo/Krafcik remarks 2017 |
| E8 | Elish (2019), moral crumple zone: "responsibility for an action may be misattributed to a human actor who had limited control over the behavior of an automated or autonomous system… the moral crumple zone protects the integrity of the technological system, at the expense of the nearest human operator." She asks of self-driving cars: "Probably." | RECORD | Engaging Science, Technology, and Society 5:40–60 |
| E9 | Matthias (2004): with learning machines the maker "is in principle not capable of predicting the future machine behaviour any more, and thus cannot be held morally responsible"; society faces "a responsibility gap" | RECORD | Ethics & Info Tech 6:175–183 |
| E10 | Santoni de Sio & Mecacci (2021): responsibility gaps are "a set of at least four interconnected problems"; they arise "with non-learning systems" too; remedy: "meaningful human control" | RECORD | Philosophy & Technology 34 |
| E11 | Aristotle: acts done "under compulsion or owing to ignorance" are pardoned, but "we punish a man for his very ignorance, if he is thought responsible for the ignorance, as when penalties are doubled in the case of drunkenness" | RECORD | Nicomachean Ethics III.1, III.5 (Ross) |
| E12 | Abraham & Rabin (2019) propose manufacturer-funded no-fault compensation ("Manufacturer Enterprise Responsibility") | RECORD | 105 Va. L. Rev. 127 |

## F. Since Tempe (status as of Oct 2026)

| # | Claim | Tag | Source |
|---|---|---|---|
| F1 | Kevin George Aziz Riad, Tesla Autopilot, Gardena CA, Dec 29 2019, two killed; pleaded **no contest** to two counts of vehicular manslaughter; probation (2023); >$23,000 restitution. AP: first felony charges against a driver using a partially automated system | INFERENCE | AP via KVIA Dec 15 2023 |
| F2 | Cruise, San Francisco, Oct 2, 2023: driverless car ran over a pedestrian thrown into its path by a human driver, then "attempted to pull over to the side of the road with the woman underneath it, dragging the woman over 20 feet." She survived | RECORD | DOJ N.D. Cal. release Nov 14 2024 |
| F3 | Cruise admitted submitting a false report to NHTSA (omitted the dragging); deferred prosecution, **$500,000 criminal fine**. The only corporate criminal case we found in this field, and it is for the report, not the harm | RECORD | same |
| F4 | California DMV suspended Cruise's driverless permits Oct 24, 2023; GM ended robotaxi funding Dec 10, 2024 | RECORD | DMV statement; GM release |
| F5 | Benavides v. Tesla (S.D. Fla.), Aug 1 2025: jury finds a defect in the 2019 Model S Autopilot a legal cause; Tesla 33% at fault, driver 67%; judgment against Tesla $242.57M incl. $200M punitive; post-trial motions denied Feb 2026; appeal pending (11th Cir. 26-10858) | RECORD | court docket (CourtListener) |
| F6 | Harris County, TX, July 1 2026: a driver charged with manslaughter after a crash with FSD engaged; prosecutors allege he overrode it. Pending | INFERENCE | Electrek; Washington Post Jul 2026 |
| F7 | Arizona statute (2021): "When engaged, the automated driving system is considered the driver or operator… for the purpose of assessing compliance with applicable traffic or motor vehicle laws." Traffic law only; nothing on homicide | RECORD | A.R.S. §28-9702(E) |
| F8 | Texas (2017): the ADS owner "is considered the operator… solely for the purpose of assessing compliance with applicable traffic or motor vehicle laws" | RECORD | Tex. Transp. Code §545.453 |
| F9 | UK Automated Vehicles Act 2024 s.47: the "user-in-charge" commits no offence "arising from the way in which a vehicle is driven"; s.6: an Authorised Self-Driving Entity must take "general responsibility"; s.25: false or withheld safety information, aggravated where someone "is killed or seriously injured," up to 14 years. **Sections 6, 12, 25, 47 not yet in force; implementation planned for 2027** | RECORD | legislation.gov.uk; SI 2026/731; DfT |
| F10 | UK Corporate Manslaughter and Corporate Homicide Act 2007: an organisation is guilty if the way its activities are "managed or organised" causes a death and "amounts to a gross breach of a relevant duty of care"; fine only. No AV case known | RECORD | legislation.gov.uk |
| F11 | US corporate criminal liability: respondeat superior (NY Central v. US, 1909); DOJ manual | RECORD | 212 U.S. 481; JM 9-28.000 |
| F12 | Indiana v. Ford (Pinto): first criminal prosecution of an automaker over crash deaths; acquitted Mar 13, 1980 | INFERENCE | CS Monitor 1980; Cato |
| F13 | PG&E pleaded guilty to 84 counts of involuntary manslaughter (Camp Fire), June 2020 | INFERENCE | press |
| F14 | Waymo: "more than 400,000 rides provided every week across six major U.S. metropolitan areas" (Feb 2026); press puts it near 500,000 a week across 15 cities by Sept 2026 | RECORD (Waymo) / INFERENCE (Sept) | Waymo blog Feb 2026; TechCrunch Sep 24 2026 |
| F15 | Tesla runs unsupervised robotaxi service in Austin (from ~Jan 2026), Dallas, Houston, and Florida cities | INFERENCE | TechCrunch etc. |
| F16 | Waymo-authored studies claim large reductions in injury crashes vs human benchmarks (e.g., Swiss Re claims: 88–92% fewer claims over 25.3M miles). Company-authored; fatality evidence thin | RECORD (claims made) / disputed | Waymo blog Dec 2024; arXiv 2505.01515 |
| F17 | US 2024: 7,080 pedestrians killed; 73% away from intersections; 76% in the dark | RECORD | NHTSA DOT HS 813 818 |
| F18 | US 2024: 1.19 deaths per 100 million vehicle miles | RECORD | NHTSA DOT HS 813 791 |

## G. Notes for the script

- Lead with what the NTSB found, not with the video (the dashcam made it look darker than it was: A6).
- Don't say "the car didn't see her" (B11) or "the car couldn't see jaywalkers" (B9/B10 are more precise).
- Don't say "Uber disabled all braking" (B12/B15).
- State the pedestrian findings (D3/D4) once, plainly, as the NTSB's; then note the NTSB still
  found an attentive operator would likely have avoided her (C8). No dwelling, no blame language.
- No depiction of Herzberg, the operator, or the impact. Reconstructions: road (simplified),
  a generic SUV (not the actual vehicle), and the sensor diagram rebuilt from the NTSB table.
- The operator's own statement (C7) conflicts with the data; say so once, factually.
