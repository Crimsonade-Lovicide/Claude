# Case 10: Tarasoff

**Question:** Should a therapist break a patient's confidence to warn someone in danger?
**Runtime target:** 17–19 min. Narration about 2,400 words.
**Voice:** the same ElevenLabs voice and model as Cases 01–09.

Every factual line traces to `research.md` (IDs in brackets in the picture notes). Picture
notes name the tool that builds each shot, in the hybrid look (FORMAT.md §2):
- `3D:` Blender scene from `production/scenes.py`
- `AI:` Higgsfield clip (places and objects only; tagged ILLUSTRATIVE · AI-GENERATED; budget 150 credits)
- `GFX:` Pillow graphic from `production/gfx.py` / `production/ep10.py`, laid over the footage named
  with it ("over …"), except act cards, verdict cards, the title, the next-case card and the end card,
  which stay on black.

Narration is the `>` lines only. `production/narration.py` extracts them and applies the
pronunciation table at the bottom.

Care rules for this episode (research §K):
- **Tatiana Tarasoff was murdered.** She is the person at the center of this case. Named in full once
  (S03), then "Tatiana". She is given more than her death: she was a student, and she said no (S11).
  **How she died is never said, shown or described**: "he killed her", and at most "near her family's
  home". No figures, silhouettes, house, route, weapons or sound design for the killing.
- **No photographs** of Tatiana or of Poddar, **no dramatization**: no re-voiced therapy session, no actor
  reading the threat, no recreated police stop, and **no recreated "letter from Dr. Moore"**. Documents on
  screen carry only the court opinions' and statutes' own words, tagged `RECONSTRUCTION · TEXT FROM …`.
- **The stalking** is described once, in the record's terms (S11–S12). Never framed as romance. The New
  Year's Eve line from the criminal opinion is not used.
- **Her brother** is never named or pictured; one sentence only (S17). Her parents are "her parents".
- **Poddar** is named once (S11) and then "he", sparingly. His caste, later life and marriage are not
  mentioned. He was convicted of second-degree murder and found sane; the conviction was reversed and he
  was never retried (S18). Never "acquitted", "insane", "deported" as fact, or "served five years".
- **The clinicians and the police were never found negligent.** Everything after the threat is what her
  parents **alleged**; every act of Dr. Powelson is attributed (S16). Never "covered up", never "the
  therapist did nothing": Moore sought commitment and told the police.
- **Mental illness:** the episode is about a threat, not a diagnosis. S06 puts the data on screen before any
  diagnosis appears; his diagnosis is called disputed (S14, S18). No "psycho", "madman", "a schizophrenic".
- **No therapy-room imagery that suggests a real session**: the `consult` room is empty, tagged
  ILLUSTRATIVE.

---

## COLD OPEN

### S01 · Berkeley, 1969
**Picture:** `AI: campus_night` A university campus walkway at night, 1960s buildings, lamps, no people, slow push; then `3D: consult` the empty consulting room, two chairs, one lamp. Lower third "Berkeley, California · Summer 1969". [T1, A4, A5]
> Berkeley, California, the summer of 1969. According to the lawsuit that followed, a graduate student tells his therapist at the university's hospital that he's going to kill a young woman when she comes home from a summer in Brazil. He doesn't say her name. He doesn't need to.

### S02 · He believes him
**Picture:** `GFX: card` over `3D: consult` RECORD: "…he was going to kill an unnamed girl, readily identifiable as Tatiana, when she returned home from spending the summer in Brazil." Tarasoff v. Regents, 1976 (as alleged). [T3, T4, T5]
> The therapist, a psychologist, believes him. With two psychiatrists, he decides the student should be committed for observation, and he asks the campus police to pick him up. They do. They find him rational, and let him go on his promise to stay away from her.

### S03 · No one warned her family
**Picture:** `GFX: rows` over `AI: bay_dusk`, then `3D: desk_blank_pen` (Case 07) ROWS: AUG 20, 1969 · A threat in therapy (as alleged) / AUG 1969 · Held by campus police; released / OCT 27, 1969 · Tatiana Tarasoff is killed. Label RECORD. Source "Tarasoff v. Regents, 1976". [T5–T7, B3, B7]
> Her parents later alleged that the head of the department then asked for the therapist's letter back, had his notes destroyed, and ordered no further action. No one warned her family. On October the twenty-seventh, 1969, after she'd come home, he killed her. Her name was Tatiana Tarasoff.

### S04 · The line every therapist learns
**Picture:** `GFX: card` over `3D: desk doc=t76` (the 1976 opinion's own words on the page) RECORD: "The protective privilege ends where the public peril begins." Justice Mathew Tobriner, Tarasoff v. Regents, July 1, 1976. Tag on the desk: RECONSTRUCTION · TEXT FROM 17 CAL.3D 425. [T9, D4, D5]
> Her parents sued. In 1976, California's Supreme Court ruled that when a therapist decides a patient poses a serious danger of violence to someone, the therapist must take reasonable care to protect that person. And it wrote a line that has followed therapists ever since: the protective privilege ends where the public peril begins.

### S05 · It will backfire
**Picture:** `GFX: card` over `3D: court_gallery` ARGUMENT: "…certain to result in a net increase in violence." Justice William Clark, dissenting, 1976. [D10, I8]
> Two of its judges said the rule would backfire: that the people who most needed help would stop telling their therapists the truth. Half a century later, that argument still isn't settled.

### S06 · One fact first
**Picture:** `GFX: number` over `AI: rain_window` (reused from Case 07) "1 IN 20" in brass; above, mono "VIOLENT CRIMES COMMITTED BY PEOPLE WITH SEVERE MENTAL ILLNESS"; below, "Sweden, national registers, 13 years". Source "Fazel & Grann, Am J Psychiatry, 2006". Then second number "11×" — "more likely than others to be victims of violent crime · Chicago, 936 patients". Source "Teplin et al., Arch Gen Psychiatry, 2005". [F1, F3]
> One fact before we go on. This case is about a threat, not a diagnosis. People with severe mental illness commit about one in twenty violent crimes. In one large study, they were more than eleven times as likely as others to be the victims of one.

### S07 · The question
**Picture:** `3D: scale_empty` The Scale, empty and level; on "should the law", cut to `3D: consult`.
> So, should a therapist break a patient's confidence to warn someone in danger? And if they should, should the law make them?

### S08 · The promise
**Picture:** `GFX: words` over `3D: evidence_shelf` (Case 05) then `3D: desk doc=t76 view=stack`. White words, "how sure" in brass.
> We went through both of the California Supreme Court's rulings, the criminal appeal, the laws written since, the research on predicting violence, and how England answers the same question. At the end, we'll give you a verdict, and tell you how sure we are.

### S09 · Title
**Picture:** `GFX: title` WEIGHT OF EVIDENCE · CASE 10 / TARASOFF / *Should a therapist break a patient's confidence to warn someone in danger?* No narration; music hit.

---

## I. THE THREAT

### S10 · Act title
**Picture:** `GFX: title` I · THE THREAT

### S11 · She said no
**Picture:** `AI: dance_hall` An empty 1960s hall with a wooden floor at dusk, folding chairs stacked, no people; then `AI: campus_night`. GFX rows: FALL 1968 · They meet at a folk-dance class / LATE 1968 · She tells him she isn't interested. Label RECORD. Source "People v. Poddar, 1974". [A1, A2]
> Tatiana Tarasoff was a student. In the fall of 1968 she met Prosenjit Poddar, a graduate student from India, at a folk-dance class at the university's International House. They saw each other weekly that fall. When she learned he thought they were in a serious relationship, she told him she wasn't interested.

### S12 · He couldn't accept it
**Picture:** `GFX: card` over `3D: tv` (the CRT, static; stands for what we won't reconstruct) RECORD: "…tape recorded various of their conversations in an attempt to ascertain why she did not love him." People v. Poddar, 1974. [A3, A4]
> He couldn't accept it. He became depressed, and stopped looking after himself and his studies. He secretly recorded their conversations, trying to work out why she didn't love him. That summer she went to South America. He began to improve, and on a friend's advice he went to the university's hospital for help.

### S13 · August 20, 1969
**Picture:** `3D: consult` slow push to the empty chair; `GFX: card` RECORD: "…readily identifiable as Tatiana…" Tarasoff v. Regents, 1976 (as alleged). [A5, T3]
> According to her parents' complaint, on August the twentieth, 1969, he told his psychologist, Dr. Lawrence Moore, that he was going to kill her when she got back from Brazil. He didn't use her name. The court later said he didn't have to: she was readily identifiable.

### S14 · They believed him
**Picture:** `GFX: rows` over `AI: hospital_1969` (a 1960s university hospital exterior at night, lit windows, no signs) ROWS: THE PSYCHOLOGIST · Believes the threat / TWO PSYCHIATRISTS · Agree: commit him for observation / THE CAMPUS POLICE · Asked to pick him up. Label RECORD. Source "Tarasoff v. Regents, 1976 (as alleged)". [A6, B1, C3]
> Moore took it seriously. He and two psychiatrists agreed Poddar should be committed for observation in a mental hospital. Moore believed he was seriously ill; at his trial, the experts would disagree about his diagnosis. Moore told the campus police he'd ask for a seventy-two-hour emergency hold, and wrote to their chief asking for help to confine him.

### S15 · Rational
**Picture:** `AI: police_car_1969` A 1960s police car parked under a campus streetlight at night, empty, no markings legible, no people; `GFX: card` RECORD: "…satisfied that Poddar was rational, released him on his promise to stay away from Tatiana." Tarasoff v. Regents, 1976 (as alleged). [B2, T5]
> Three officers picked him up. They found him rational, and let him go when he promised to stay away from her. At the time, campus police didn't have the power to start an emergency hold, and the university's hospital had never been authorized to start one either. The people who could legally hold him weren't the people who had him.

### S16 · Ordered no action
**Picture:** `GFX: card` over `3D: desk doc=t76_complaint` RECORD: "…'ordered no action to place Prosenjit Poddar in 72-hour treatment and evaluation facility.'" Her parents' complaint, as quoted in Tarasoff v. Regents, 1976. Label under the card: AS ALLEGED · NEVER TESTED AT TRIAL. [B3, B4, D12]
> Then, her parents alleged, the director of the department of psychiatry, Dr. Harvey Powelson, asked the police to return Moore's letter, had the letter and Moore's notes destroyed, and ordered no action to hold him. If that happened, we don't know why. No court ever tested any of it.

### S17 · October 27, 1969
**Picture:** `AI: bay_dusk` San Francisco Bay at dusk from the hills, no people; then `GFX: words` "OCTOBER 27, 1969" over black. [B5, B6, B7, T6]
> He had persuaded Tatiana's brother to share an apartment with him, near her family's home. She came back from Brazil, and he stopped seeing his psychologist. No one warned her parents. On October the twenty-seventh, 1969, he killed her.

### S18 · The criminal case
**Picture:** `GFX: rows` over `3D: court_bench` ROWS: TRIAL · Second-degree murder; the jury finds him sane / FEB 7, 1974 · Conviction reversed: the jury wasn't properly instructed / AFTER · Never retried; returned to India. Label RECORD. Source "People v. Poddar, 1974". [C1–C7]
> A jury convicted him of second-degree murder and found him sane. In 1974, California's Supreme Court overturned the conviction, because the jury hadn't been properly instructed on his mental state. The state never retried him. He was released, and returned to India.

### S19 · First weight
**Picture:** `3D: scale_tip_left` The first pan drops. Lower third "EVIDENCE · A THREAT, A FAILED HOLD, AND A FAMILY NEVER TOLD". [§A, §B]
> So, the first weight. A threat against someone anyone could identify. Clinicians who believed it and tried to have him held. Police who let him go. And the one family it pointed at, never told.

---

## II. THE RULING

### S20 · Act title
**Picture:** `GFX: title` II · THE RULING

### S21 · The lawsuit
**Picture:** `AI: ca_court` A grand state supreme-court building at dusk, columns, no people, no readable inscriptions; `GFX: rows` FAILURE TO DETAIN / FAILURE TO WARN / ABANDONMENT OF A DANGEROUS PATIENT. Label RECORD. Source "Tarasoff v. Regents, 1976 (her parents' claims)". [D1]
> Tatiana's parents sued the university's Regents, the four clinicians and the campus police. They said the therapists should have held him, or warned them. The trial court threw the case out before any trial. Her parents appealed.

### S22 · Twice
**Picture:** `GFX: rows` over `3D: court_push` ROWS: DEC 23, 1974 · "A duty to warn" (vacated) / 1975 · Rehearing; the profession objects / JULY 1, 1976 · "A duty to protect". Label RECORD. Source "Tarasoff v. Regents, 1974 and 1976". [D2, D3, E1]
> In December 1974, the state Supreme Court revived the case, and said therapists could have a duty to warn. Then it agreed to hear the case again. The American Psychiatric Association and other professional groups weighed in: therapists, they argued, can't reliably predict violence, and tend to overpredict it.

### S23 · One word
**Picture:** `GFX: card` over `3D: desk doc=t76` RECORD: "When a therapist determines, or pursuant to the standards of his profession should determine, that his patient presents a serious danger of violence to another, he incurs an obligation to use reasonable care to protect the intended victim against such danger." Tarasoff v. Regents, 1976. [D4, T9]
> In July 1976, the court ruled again, and changed one word. Not a duty to warn: a duty to protect. When a therapist decides, or by the standards of the profession should decide, that a patient poses a serious danger of violence to someone, the therapist must take reasonable care to protect that person. Warning them is one way. Calling the police is another.

### S24 · Where the peril begins
**Picture:** `GFX: card` over `3D: desk doc=t76 view=pen` RECORD: "…the public policy favoring protection of the confidential character of patient-psychotherapist communications must yield to the extent to which disclosure is essential to avert danger to others." Then card RECORD: "The risk that unnecessary warnings may be given is a reasonable price to pay for the lives of possible victims that may be saved." Justice Tobriner, 1976. [D5, D6, I2]
> Justice Mathew Tobriner wrote that the secrecy of therapy must give way when disclosure is essential to avert danger. But not routinely: a therapist should break a confidence only when it's necessary, and even then, discreetly. And he answered the profession's fear of false alarms. Unnecessary warnings, he wrote, are a reasonable price to pay for the lives that may be saved.

### S25 · What it didn't decide
**Picture:** `GFX: rows` over `3D: court_witness` ROWS: IT DID NOT · Find anyone liable / IT DID NOT · Give the police a duty / IT DID · Let her parents' case go forward. Label RECORD. Source "Tarasoff v. Regents, 1976". Then card INFERENCE: "The case was reportedly settled out of court. No amount has been made public." Source "Psychiatric Times, 2009 · Orthopedics Today, 2013". [D8, D11, L]
> It's worth being exact about what the court did. It found no one liable. It ruled that her parents could bring their case against the therapists and the university, and that the police owed no duty. The case was reportedly settled out of court. We could find no record of the amount.

### S26 · The wonderland of clairvoyance
**Picture:** `GFX: card` over `3D: court_bench` ARGUMENT: "The majority's expansion of that rule will take us from the world of reality into the wonderland of clairvoyance." Justice Stanley Mosk, concurring and dissenting, 1976. [D9, I10, I13]
> Justice Stanley Mosk agreed with the result, but only because these therapists had actually predicted violence. Psychiatric predictions are inherently unreliable, he wrote. To blame therapists for what they should have predicted would take the law from the world of reality into the wonderland of clairvoyance. And these therapists had told the police. He doubted more should be required.

### S27 · The dissent
**Picture:** `GFX: card` over `3D: consult` ARGUMENT: "…the very practice of psychiatry vitally depends upon the reputation in the community that the psychiatrist will not tell." Ralph Slovenko, quoted by Justice Clark, dissenting, 1976. Then card ARGUMENT: "…certain to result in a net increase in violence." Justice Clark, 1976. [D10, I8, I9, I12]
> Justice William Clark dissented. Therapy, he argued, depends on patients trusting that their therapist won't tell. Many people who might be violent, but could be helped, would be put off seeking help. And therapists, afraid of being sued, would resolve their doubts by warning, or committing, people who were never dangerous. The new duty, he wrote, was certain to result in a net increase in violence.

### S28 · Second weight
**Picture:** `3D: scale_tip_right` Lower third "EVIDENCE · A DUTY TO STRANGERS, ON FACTS NO COURT EVER TESTED". [§D]
> So, the second weight. The court made therapists responsible for people they had never met. Its own members warned that it couldn't be done well, and might do harm. And no court ever tested what happened in 1969.

---

## III. THE PREDICTION

### S29 · Act title
**Picture:** `GFX: title` III · THE PREDICTION

### S30 · The base rate
**Picture:** `GFX: dots` 100,000 dots; 100 brass (would kill), 95 of them ringed (caught); 4,995 grey ringed (flagged, never would). Tag ILLUSTRATION · NOT DATA. Source "Comment quoted in Thompson v. County of Alameda, 1980". [E4]
> Here's the problem the doubters saw. Imagine a test that spots ninety-five percent of the people who will kill, and is wrong about only five percent of everyone else. Test a hundred thousand people, of whom a hundred will kill. It catches ninety-five. It also flags nearly five thousand who never would.

### S31 · Better than chance
**Picture:** `GFX: bars` over `3D: corridor_b` (Case 01) VIOLENT WITHIN SIX MONTHS: Predicted violent 53% (brass) / Not predicted 36% (dim). Source "Lidz, Mulvey & Gardner, JAMA, 1993". [E2]
> Clinicians do better than chance, but not by much. In a 1993 study of psychiatric emergency patients, fifty-three percent of those clinicians predicted would be violent were, over the next six months. So were thirty-six percent of those they didn't flag.

### S32 · Good at the opposite job
**Picture:** `GFX: number` over `3D: evidence_shelf` "41%" in brass; above, "FLAGGED HIGH RISK WHO WENT ON TO BE VIOLENT"; below, "median · 73 samples, 24,827 people". Then "91%" dim: "rated low risk who did not". Source "Fazel et al., BMJ, 2012". [E3]
> Modern risk tools are better at the opposite job. Across seventy-three studies, people flagged as high risk went on to be violent a median forty-one percent of the time. People rated low risk stayed that way about nine times in ten. The researchers' conclusion: good at spotting low risk, not good enough to lock anyone up on.

### S33 · Not a prediction case
**Picture:** `3D: consult` the empty chair; `GFX: words` "HE SAID WHO. HE SAID WHAT." [E5, T3, A6]
> But this case wasn't really about prediction. He said who, and what. His therapists believed him, and acted. The question it leaves isn't whether therapists can see the future. It's what they owe someone when a patient tells them.

### S34 · Would patients stop talking?
**Picture:** `GFX: card` over `AI: rain_window` RECORD: "…these findings do not hold up in research with actual therapy patients…" Roback & Shelton, review, 1995. [E6, D7]
> Clark's fear, that patients would stop talking, has been studied less than you'd think. A 1995 review found that people imagining therapy say limits on secrecy would put them off. In studies of actual patients, the effect mostly disappeared, except where what they said could bring serious legal trouble. The evidence is old, and thin.

### S35 · When they warn
**Picture:** `GFX: rows` over `3D: ward_window` (Case 07) ROWS: ALMOST HALF · Of residents had issued a warning / MOST · Said it had little effect on therapy, or helped / ~3 IN 4 · Of people reached already knew. Label RECORD. Source "Binder & McNiel, Psychiatric Services, 1996 · 46 residents, San Francisco". [E7, I5]
> When therapists do warn, it seems to do less damage than feared. In a small 1996 study of psychiatry residents in San Francisco, almost half had issued a warning. Most said it made little difference to the therapy, or even helped. And in almost three quarters of the cases where they reached the person in danger, that person already knew.

### S36 · Third weight
**Picture:** `3D: scale_tip_left` Lower third "EVIDENCE · PREDICTION IS WEAK. HERE, IT WASN'T NEEDED." [§E]
> So, the third weight. Therapists can't predict violence well. But when a patient says it plainly, prediction isn't the problem. And the damage to therapy is, so far, mostly feared rather than found.

---

## IV. THE RULES

### S37 · Act title
**Picture:** `GFX: title` IV · THE RULES

### S38 · California narrows it
**Picture:** `GFX: card` over `3D: desk doc=civ4392` RECORD: "…a serious threat of physical violence against a reasonably identifiable victim or victims." Cal. Civ. Code § 43.92 (1985; amended 2012). [G2, G3]
> California's legislature narrowed the rule in 1985. Today a therapist there can be held responsible only if a patient has communicated a serious threat of physical violence against a reasonably identifiable victim. And a therapist who makes reasonable efforts to tell the victim and the police is protected.

### S39 · And courts stretched it
**Picture:** `GFX: rows` over `AI: va_hospital` (a large 1970s veterans' hospital exterior at dusk, no signs, no people), then `3D: court_push` ROWS: 1983 · A veterans' hospital is liable: the doctors never got his past records / 2004 · A threat told by a patient's family counts too. Label RECORD. Source "Jablonski v. United States, 9th Cir. 1983 · Ewing v. Goldstein, Cal. Ct. App. 2004". [G4, G5]
> Courts have stretched it in both directions. In 1983, a federal court held the government liable when doctors at a veterans' hospital failed to get a patient's earlier records, which showed violence toward a former partner. He went on to kill the woman he was then with. And in 2004, a California appeals court ruled that a threat reported by a patient's own family counts, too.

### S40 · Fifty rules
**Picture:** `GFX: rows` over `3D: book_night` (Case 04) ROWS: MUST · 23 states by statute, 10 by court ruling / MAY · 11 states / SILENT · 6 states. Label RECORD. Source "Johnson, Persad & Sisti, JAAPL, 2014 (laws as of 2012)". On screen under the source: "Counts differ by method and year". [G6]
> Across America, there's no single rule. Some states require therapists to act. Others only allow them to. A few say nothing at all. One 2014 review counted twenty-three states with a duty written into law and ten more through their courts. But the counts depend on who's counting, and when.

### S41 · May, not must
**Picture:** `GFX: card` over `3D: desk doc=hipaa` RECORD: "A covered entity may … use or disclose protected health information, if the covered entity, in good faith, believes the use or disclosure … is necessary to prevent or lessen a serious and imminent threat to the health or safety of a person or the public…" 45 C.F.R. § 164.512(j). [G8–G10]
> Federal privacy law lets a therapist disclose to prevent a serious and imminent threat. It doesn't require it. The psychologists' and doctors' ethics codes say the same thing: you may, to protect someone from harm.

### S42 · One study
**Picture:** `GFX: number` over `AI: rain_window` "+5%" in brass; above, "HOMICIDES WHERE WARNINGS WERE MADE MANDATORY"; below, "one study · observational · not replicated". Source "Griffin Edwards, Journal of Law and Economics, 2014". [H1, H2, I11]
> Does requiring warnings save lives? There's one serious attempt to measure it. An economist, Griffin Edwards, compared states over time, and found that where warnings became mandatory, homicides rose by about five percent. He thinks patients stopped seeking the help that would have prevented them. But it's one study. It can't prove cause, the mechanism wasn't measured, and no one has replicated it.

### S43 · England
**Picture:** `AI: london_courts` (the Royal Courts of Justice, London, at dusk, no people); `GFX: card` RECORD: "…is entitled to take such steps as are reasonable in all the circumstances to communicate the grounds of his concern to the responsible authorities." Lord Justice Bingham, W v Egdell, Court of Appeal, 1989. [H3, H4]
> England answers differently. In 1989, a psychiatrist sent his report on a dangerous patient to the authorities against the patient's wishes. The patient had shot seven people; five had died. The Court of Appeal said the psychiatrist was entitled to do it: not obliged. Guidance for British doctors today says the same: they may disclose to protect someone from death or serious harm, and should share as little as they need to.

### S44 · Fourth weight
**Picture:** `3D: scale_tip_right` Lower third "EVIDENCE · EVERYONE SAYS MAY. NO ONE AGREES ON MUST." [§G, §H]
> So, the fourth weight. Nearly everyone now agrees a therapist may break a confidence to save a life. Where they disagree is whether the law should make them. And the only study of that suggests making them may cost lives.

---

## V. THE VERDICT

### S45 · Act title
**Picture:** `GFX: title` V · THE VERDICT

### S46 · The case for a duty
**Picture:** `B-roll montage` with the weight lower third "THE STRONGEST CASE: SILENCE HAS A VICTIM WITH A NAME": `3D: scale_tip_left`, `3D: consult`, `AI: police_car_1969`, `3D: desk doc=t76`, `3D: scale_tip_left`. [I1–I7, I14]
> First, the strongest case for a duty. A therapist isn't a bystander to the danger: often, they're the only person who knows. In 1969, everyone who could act on what he said did something, except tell the one family it pointed at. A warning costs a patient some privacy. Silence can cost someone her life. Unnecessary warnings, the court said, are a reasonable price. Every major code already allows disclosure; a duty only makes sure it happens. And when therapists do warn, therapy mostly survives.

### S47 · The case against
**Picture:** montage with lower third "THE STRONGEST CASE: DON'T MAKE SILENCE A LAWSUIT": `3D: scale_tip_right`, `3D: consult`, `3D: ward_window`, `AI: rain_window`, `3D: scale_tip_right`. [I8–I13, I14]
> Now the strongest case against a duty. Therapy works because people say things they'd never say anywhere else, including the worst thing they've ever thought. Make therapists legally answerable for every threat, and they'll protect themselves first: more warnings, more commitments, people losing their liberty for things they'd never do. Therapists can't predict well. Patients who sense the limit may stay away. And the one study of mandatory warnings found more homicides, not fewer. Let therapists act when they must. Don't make silence a lawsuit.

### S48 · Verdict one
**Picture:** `GFX: verdict` Kicker BERKELEY, 1969. VERDICT: "On the facts as her parents alleged them: once the clinicians judged him dangerous enough to hold, and the hold failed, someone should have made sure Tatiana or her family knew." CONFIDENCE 80%. WHAT WOULD CHANGE OUR MIND: "Evidence that she or her family already knew of the threat, or that a warning would have made an attack more likely."
> Here's our verdict. On Berkeley, 1969, on the facts as her parents alleged them: once the clinicians judged him dangerous enough to hold, and the hold failed, someone should have made sure Tatiana or her family knew. Our confidence is eighty percent. What would change our mind: evidence that she or her family already knew of the threat, or that a warning would have made an attack more likely.

### S49 · Verdict two
**Picture:** `GFX: verdict` Kicker THE RULE. VERDICT: "A legal duty to protect, not a duty to warn: when a patient makes a serious threat against an identifiable person, the therapist must act, and a warning is one way to do it." CONFIDENCE 70%. WHAT WOULD CHANGE OUR MIND: "A replicated study showing that states with the duty have more violence, or fewer people seeking treatment, than states that only permit disclosure."
> On the rule: there should be a legal duty to protect, not a duty to warn. When a patient makes a serious threat against an identifiable person, the therapist must act, and a warning is one way to do it. Our confidence is seventy percent, lower, because the one study of outcomes points the other way. What would change our mind: a replicated study showing that states with the duty have more violence, or fewer people seeking treatment, than states that only permit disclosure.

### S50 · Verdict three
**Picture:** `GFX: verdict` Kicker THE QUESTION. VERDICT: "Yes, but only for a serious threat against someone identifiable, only when nothing less will protect them, and only as much as the danger requires. A narrow exception, not a reporting rule." CONFIDENCE 75%. WHAT WOULD CHANGE OUR MIND: "Good evidence that patients who know about the limit stop telling therapists about the threats that matter."
> And on the question: should a therapist break a patient's confidence to warn someone in danger? Yes, but only for a serious threat against someone identifiable, only when nothing less will protect them, and only as much as the danger requires. A narrow exception, not a reporting rule. Our confidence is seventy-five percent. What would change our mind: good evidence that patients who know about the limit stop telling therapists about the threats that matter.

### S51 · The case stays open
**Picture:** `3D: scale_level_loaded` Level, slow orbit, fade toward black.
> That's our verdict. It's open, which means it can change. If you think we got it wrong, make your case in the comments. We'll answer the strongest one in the next episode.

### S52 · Next case
**Picture:** `GFX: words` "NEXT CASE" over black: "<NAME · YEAR>" / *<question>*
> Next case: [to be written once the owner chooses Case 11; fact-check it in that case's research §0 before recording].

### S53 · End card
**Picture:** `GFX: endcard` Title, subscribe area, two end-screen slots. Sources link. No narration.

---

## Pronunciation (applied to narration text only)

Model: eleven_multilingual_v2. Numbers are written out in the narration where the voice could
misread them. All guesses, to confirm by ear in the review copy (research §M).

| Written | Spoken as |
|---|---|
| Tatiana | Tah-tee-ah-nuh |
| Tarasoff | Tar-uh-soff |
| Prosenjit | Proh-shen-jeet |
| Poddar | Pod-dar |
| Powelson | Pow-ul-sun |
| Tobriner | Toh-brin-er |
| Egdell | Egg-del |

## New footage for this case

- **3D (new):** `consult`, an empty consulting room: two armchairs facing each other, a side table, a lamp, a
  window with blinds, nothing on the walls that reads as a real practice (tag ILLUSTRATIVE). `desk` gains
  the documents `t76` (the holding and the "protective privilege" line), `t76_complaint` (only the quoted
  allegation in S16), `civ4392` and `hipaa`, each tagged `RECONSTRUCTION · TEXT FROM …`. `dots` (S30) is a
  GFX, not 3D.
- **3D (reused):** the courtroom (Case 07), the corridor (Case 01), the shelf (Case 05), the book (Case 04),
  the care-home window (Case 07), the TV (Case 07), the Scale (Case 01).
- **AI (new, about 9 clips, ~90 credits):** `campus_night`, `dance_hall`, `bay_dusk`, `hospital_1969`,
  `police_car_1969`, `ca_court`, `va_hospital`, `london_courts`; `rain_window` is reused from Case 07.
  Places and objects only; reject any clip with a face, a person, or readable fake text.

## Sources on screen (description box)

See `research.md`. Every RECORD card carries its citation on screen; the full list goes in the
description, led by *Tarasoff v. Regents* (1974, vacated; 1976), *People v. Poddar* (1974), *Thompson v. County
of Alameda* (1980), *Jablonski v. United States* (1983), *Ewing v. Goldstein* (2004), Cal. Civ. Code § 43.92,
45 C.F.R. § 164.512(j), the APA and AMA ethics codes, *W v Egdell* (1989), Edwards (2014), Lidz et al. (1993),
Fazel et al. (2012), Fazel & Grann (2006), Teplin et al. (2005), Roback & Shelton (1995), Binder & McNiel
(1996), and Johnson, Persad & Sisti (2014).

## Before recording (from research §N and our own checks)

- **Allegations:** every fact about the therapists, Powelson and the police in S01–S17 comes from her parents'
  complaint as the court accepted it for the ruling. The narration says "according to the lawsuit" (S01) and
  "her parents alleged" (S03, S16); keep both.
- **S03, S17:** "No one warned her family / her parents" is the 1976 opinion's wording; never "no one warned
  her" (research T6).
- **S11:** "at the university's International House" and "weekly" are from *People v. Poddar*; Tatiana's school
  and age are unverified, so she is "a student".
- **S13:** the August 20 date is the complaint's; the criminal opinion puts the end of therapy in October
  (research T7). The narration dates only the threat, attributed.
- **S15:** the commitment-power point is from the 1976 opinion (research B2). "The people who could legally
  hold him weren't the people who had him" is our inference; it rides on the record, but keep it as phrased.
- **S17:** the order follows *People v. Poddar* (he stopped therapy in October, after she returned); the
  apartment with her brother is undated in the complaint, so "had persuaded".
- **S18:** "returned to India" is from secondary sources (research C6). No year for the trial.
- **S39:** *Jablonski*: the records showed "homicidal ideation toward his wife" (a former partner); the victim,
  Melinda Kimball, is not named on air. Confirm "the woman he was then with" against the opinion's facts.
- **S22:** the 1974 opinion was read only through a summary (research D2); the narration paraphrases it.
  Confirm "duty to warn" against 13 Cal.3d 177 before air.
- **S25:** "reportedly settled" (research D11). No amount, ever.
- **S30:** the base-rate numbers are a 1975 law-review comment quoted by the California Supreme Court in 1980;
  the graphic is an illustration, tagged so.
- **S32:** "about nine times in ten" rounds the median negative predictive value of 91%.
- **S40:** the 23/10/11/6 split is the 2012 classification reported in 2014. Check NCSL's table on the
  recording date; if it's current and readable, use it with its date on screen instead.
- **S42:** the units of ".4" are unconfirmed (research H2); the narration uses only "about five percent".
- **S43:** the GMC's own wording was read only through a medical defence organization's summary (research H4);
  the narration paraphrases it. *Egdell*'s facts: seven shot, five died (research H3).
- **Pronunciations:** Tatiana, Prosenjit and Powelson are unverified.
- **Family:** before publishing, check whether a member of Tatiana's family is reachable; the owner may want to
  let them know (research §N).
