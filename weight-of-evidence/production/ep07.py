"""Weight of Evidence, Case 07: Terri Schiavo. Shot definitions for edit.py.

    python ep07.py <prod_dir> --stills | --only S02,S13 | --final -j 2

Shot ids, picture notes and research IDs are in episodes/07-terri-schiavo/script.md.
Care rules (research §K): no image of her at all, nothing from the 2002 videotapes, no hospice,
hospital or bedside imagery, no feeding tubes, no brain scans (the brain weight is a number card
only); both families get their strongest case from the record; courts are quoted as written; the
Capitol dome and the courtroom are empty, generic reconstructions.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import edit as E  # noqa: E402
import ep01 as E1  # noqa: E402  (shared helpers: stacked words, end card, overlays)
import ep02 as E2  # noqa: E402  (shared helpers: dated rows, big words, lower thirds)
import ep04 as E4  # noqa: E402  (shared helpers: number, bars)
import gfx as G  # noqa: E402
import score as S  # noqa: E402

OUT_NAME = "weight_of_evidence_case07.mp4"
TITLE = "Weight of Evidence, Case 07: Terri Schiavo"

SILENT = {"S09": 6.5, "S10": 3.4, "S19": 3.4, "S30": 3.4, "S41": 3.4, "S49": 3.4, "S57": 20.0}
LEAD = {"S01": 2.0, "S02": 0.6, "S04": 0.6, "S11": 0.8, "S20": 0.6, "S31": 0.6, "S42": 0.6,
        "S50": 0.6, "S56": 0.8}
PAD = {"S01": 0.8, "S02": 1.4, "S03": 1.4, "S04": 1.4, "S05": 1.6, "S06": 1.4, "S07": 1.6,
       "S08": 1.2, "S12": 1.6, "S13": 1.4, "S14": 1.6, "S15": 1.6, "S17": 1.4, "S18": 1.8,
       "S21": 1.6, "S23": 1.4, "S24": 1.6, "S27": 1.4, "S28": 1.8, "S29": 1.8, "S32": 1.6,
       "S33": 1.8, "S36": 1.6, "S37": 1.4, "S38": 2.2, "S39": 1.6, "S40": 2.0, "S42": 1.4,
       "S45": 1.4, "S46": 1.4, "S47": 1.4, "S48": 1.8, "S52": 3.0, "S53": 3.0, "S54": 3.0,
       "S55": 2.0, "S56": 2.4}
FADE_IN = {"S01": 1.4, "S10": 0.6, "S19": 0.6, "S30": 0.6, "S41": 0.6, "S49": 0.6}
FADE_OUT = {"S08": 0.4, "S09": 1.0, "S18": 1.0, "S29": 1.0, "S38": 1.0, "S40": 1.2, "S48": 1.2,
            "S55": 1.5, "S57": 1.5}
CHAPTERS = [("S01", "Washington, 2005"), ("S10", "I. The collapse"), ("S19", "II. The trial"),
            ("S30", "III. The politicians"), ("S41", "IV. The rules"), ("S49", "V. The verdict"),
            ("S56", "Next case")]

GREER = "Judge Greer's order, 2000"
DCA = "Florida Second District Court of Appeal"
WOLF = "Jay Wolfson, guardian ad litem, 2003"
ME = "Pinellas-Pasco Medical Examiner, 2005"

# Case 08 teaser card (checked in Case 08 research, section 0)
NEXT_NAME = "KALIEF BROWDER · 2010"
NEXT_Q = "Should anyone be jailed for years before a trial?"
NEXT_AT = ("in New York", "Should anyone")


# ---------------------------------------------------------------- the shots

def build(ctx):
    P = ctx.prod
    C = lambda name, **kw: E.Clip(P, name, **kw)
    at = ctx.at
    rows = E2.rows_shot
    big = E2.big_words
    stack = E1.stacked_words_shot
    weight = E1.scale_overlay
    lower = E2.lower
    card = G.card_shot
    num = E4.number_shot
    shots = {}

    # COLD OPEN
    shots["S01"] = E.clip_shot(C("dome_push"), overlay=lower("Washington", "MARCH 21, 2005 · 12:45 A.M.", 2.4))
    shots["S02"] = card("“Any parent of Theresa Marie Schiavo shall have standing … Nothing in this Act shall "
                        "constitute a precedent with respect to future legislation.”", "RECORD",
                        "Pub. L. 109-3, March 21, 2005")
    shots["S03"] = num("26", "FEBRUARY 25, 1990", "her heart stopped at home in Florida",
                       GREER + " · Medical Examiner, 2005", at=at("S03", "when she was"))
    shots["S04"] = rows([("HER HUSBAND", "She wouldn't want to live like that"),
                         ("HER PARENTS", "She is still aware"),
                         ("A JUDGE", "Sided with her husband")],
                        [at("S04", "Her husband"), at("S04", "Her parents"), at("S04", "A judge")],
                        label="INFERENCE", source=GREER + " · Wolfson report, 2003")
    shots["S05"] = rows([("MAR 18, 2005", "Feeding tube removed"), ("MAR 22–30", "Federal courts decline"),
                         ("MAR 31", "She dies, aged 41")],
                        [0.3, at("S05", "declined"), at("S05", "She died")],
                        label="RECORD", source="Eleventh Circuit, 2005 · Medical Examiner, 2005")
    shots["S06"] = num("1 IN 3", "US ADULTS WITH AN ADVANCE DIRECTIVE", "a review of 150 studies, 2011–2016",
                       "Yadav et al., Health Affairs, 2017", colour=G.BRASS, at=at("S06", "only about"))
    shots["S07"] = E.clip_shot(C("scale_empty"), tag=None)
    shots["S08"] = G.words_shot("We'll give you a verdict, and tell you how sure we are.", size=64,
                                emphasis={"how", "sure"}, per_word=0.3, start=at("S08", "At the end"))
    shots["S09"] = G.title_shot("TERRI SCHIAVO", "Who should decide when to stop keeping someone alive?",
                                "WEIGHT OF EVIDENCE · CASE 07")

    # I. THE COLLAPSE
    shots["S10"] = G.title_shot("I · THE COLLAPSE")
    shots["S11"] = rows([("1984", "Married Michael Schiavo"), ("1986", "Moved to Florida; her family followed"),
                         ("FEB 25, 1990", "Her heart stopped")],
                        [at("S11", "She married"), at("S11", "moved with him"), at("S11", "Early on February")],
                        label="RECORD", source=GREER + " · Wolfson report, 2003")
    shots["S12"] = card("“…is not simply a coma. She is not asleep. She has cycles of apparent wakefulness and "
                        "apparent sleep without any cognition or awareness.”", "RECORD", DCA + ", 2001")
    shots["S13"] = card("“…the cause of which cannot be determined with reasonable medical certainty.”", "RECORD", ME)
    shots["S14"] = card("“…complete trust, mutual caring, explicit love and a common goal.”", "RECORD",
                        "Jay Wolfson, guardian ad litem, report to Governor Bush, 2003")
    t_fp = at("S15", "view was that")
    shots["S15"] = G.seq((rows([("1993", "Malpractice award, most of it in trust for her care"),
                                ("FEB 14, 1993", "The families stop speaking")],
                               [0.4, at("S15", "That February")], label="RECORD",
                               source=GREER + " · Wolfson report, 2003"), t_fp),
                         (card("“…neither side is exempt from finger pointing as to possible conflicts of "
                               "interest.”", "RECORD", "Judge George Greer, 2000"), 1))
    shots["S16"] = rows([("1994", "A do-not-resuscitate order; the nursing home objects"),
                         ("1994", "Her parents try to remove him as guardian; dismissed")],
                        [at("S16", "on medical advice"), at("S16", "Her parents went")],
                        label="RECORD", source=GREER + " · Wolfson report, 2003")
    shots["S17"] = card("“Petition for Authorization to Discontinue Artificial Life Support.”", "RECORD",
                        "Filed by Michael Schiavo, guardian, May 11, 1998")
    shots["S18"] = E.clip_shot(C("scale_tip_left"), tag=None,
                               overlay=weight("EVIDENCE · NO WRITTEN WISHES, AND TWO FAMILIES WHO NO LONGER SPOKE"))

    # II. THE TRIAL
    shots["S19"] = G.title_shot("II · THE TRIAL")
    shots["S20"] = E.clip_shot(C("courtroom_push"), overlay=lower("Clearwater, Florida", "JANUARY 2000", 1.2))
    shots["S21"] = card("“…if I ever go like that just let me go. Don't leave me there. I don't want to be kept "
                        "alive on a machine.”", "RECORD",
                        "Her words as recounted by Scott Schiavo, as found by Judge Greer, 2000")
    shots["S22"] = card("The court found the remarks about Karen Ann Quinlan were made when Terri was 11 or 12, and "
                        "gave them no weight.", "RECORD", GREER)
    shots["S23"] = card("“…is reliable, is creditable and rises to the level of clear and convincing evidence.”",
                        "RECORD", "Judge George Greer, Feb 11, 2000")
    shots["S24"] = card("“…the trial court essentially serves as the ward's guardian.”", "RECORD", DCA + ", 2001")
    shots["S25"] = rows([("APR 24, 2001", "Feeding tube removed"), ("APR 26, 2001", "Another judge orders it restored")],
                        [at("S25", "In April"), at("S25", "Two days later")], label="RECORD", source=DCA + ", 2001")
    shots["S26"] = rows([("FOR HER PARENTS", "2 doctors: not vegetative"), ("FOR HER HUSBAND", "2 doctors: vegetative"),
                         ("FOR THE COURT", "1 doctor: vegetative")],
                        [at("S26", "two chosen"), at("S26", "two chosen", offset=0.8), at("S26", "one by the court")],
                        label="RECORD", source=DCA + ", 2003")
    shots["S27"] = card("“There are instances where she appears to respond specifically to her mother. But these are "
                        "not repetitive or consistent.”", "RECORD", WOLF)
    shots["S28"] = card("“If Mrs. Schiavo were our own daughter, we could not but hold to such a faith. But in the "
                        "end, this case is not about the aspirations that loving parents have for their children. It "
                        "is about Theresa Schiavo's right to make her own decision…”", "RECORD",
                        DCA + ", June 6, 2003")
    shots["S29"] = E.clip_shot(C("scale_tip_right"), tag=None,
                               overlay=weight("EVIDENCE · A FULL TRIAL, FIVE DOCTORS, AND THE SAME ANSWER EVERY TIME"))

    # III. THE POLITICIANS
    shots["S30"] = G.title_shot("III · THE POLITICIANS")
    shots["S31"] = rows([("OCT 15, 2003", "Feeding tube removed again"),
                         ("OCT 21, 2003", "“Terri's Law” passed; the tube goes back in")],
                        [0.4, at("S31", "Six days later")], label="RECORD",
                        source="Bush v. Schiavo, Florida Supreme Court, 2004")
    shots["S32"] = card("“Sometimes good law is not enough, good medicine is not enough, and all too often, good "
                        "intentions do not suffice.”", "RECORD", "Jay Wolfson, guardian ad litem, Dec 1, 2003")
    shots["S33"] = card("“…But our hearts are not the law.”", "RECORD",
                        "Chief Justice Pariente, Bush v. Schiavo, Florida Supreme Court, 2004")
    t_wh = at("S34", "The White House")
    shots["S34"] = G.seq((rows([("MAR 18, 2005", "Tube removed a third time"),
                                ("MAR 20", "The Senate passes S. 686 by voice vote"),
                                ("MAR 21, 12:45 A.M.", "The House, 203–58; the President signs")],
                               [0.4, at("S34", "Two days later"), at("S34", "The House followed")],
                               label="RECORD", source="House Roll Call 90, 2005 · Pub. L. 109-3"), t_wh),
                         (card("“…our society, our laws, and our courts should have a presumption in favor of "
                               "life.”", "RECORD", "The White House, March 21, 2005"), 1))
    shots["S35"] = rows([("IT DID NOT", "Order the tube put back"),
                         ("IT DID", "Let a federal court hear the case from the start")],
                        [0.4, at("S35", "It gave")], label="RECORD", source="Pub. L. 109-3 · Eleventh Circuit, 2005")
    t_wil = at("S36", "Another")
    shots["S36"] = G.seq((card("“…acted in a manner demonstrably at odds with our Founding Fathers' blueprint for the "
                               "governance of a free people — our Constitution.”", "RECORD",
                               "Judge Birch, Eleventh Circuit, March 30, 2005"), t_wil),
                         (card("“…death, which is imminent, effectively ends the litigation without a fair "
                               "opportunity to fully consider the merits…”", "RECORD",
                               "Judge Wilson, dissenting, Eleventh Circuit, March 23, 2005"), 1))
    t82 = at("S37", "In a CBS")
    shots["S37"] = E4.bars_shot("WHAT CONGRESS AND THE PRESIDENT SHOULD HAVE DONE",
                                [("Stayed out", 82, G.BRASS, t82 + 1.0), ("Been involved", 13, G.DIM, t82 + 1.6)],
                                "CBS News poll, March 21–22, 2005 (via Gallup)")
    shots["S38"] = big("MARCH 31, 2005", 96)
    t_nel = at("S39", "But the neuropathologist")
    shots["S39"] = G.seq((num("615 g", "HER BRAIN AT AUTOPSY", "less than half the expected weight",
                              "Pinellas-Pasco Medical Examiner, June 2005", at=at("S39", "her brain weighed")), t_nel),
                         (card("“…cannot prove or disprove a diagnosis of persistent vegetative state or minimally "
                               "conscious state.”", "RECORD", "Dr. Stephen Nelson, neuropathologist, 2005"), 1))
    shots["S40"] = E.clip_shot(C("scale_tip_right", start=2), tag=None,
                               overlay=weight("EVIDENCE · EVERY BRANCH OF GOVERNMENT STEPPED IN. THE COURTS HELD."))

    # IV. THE RULES
    shots["S41"] = G.title_shot("IV · THE RULES")
    t_sca = at("S42", "Justice Scalia")
    shots["S42"] = G.seq((card("“…a State may apply a clear and convincing evidence standard in proceedings where a "
                               "guardian seeks to discontinue nutrition and hydration of a person diagnosed to be in a "
                               "persistent vegetative state.”", "RECORD",
                               "Cruzan v. Director, Missouri Dept. of Health, U.S. Supreme Court, 1990"), t_sca),
                         (card("“…the citizens of Missouri to decide, through their elected representatives.”",
                               "RECORD", "Justice Scalia, concurring, Cruzan, 1990"), 1))
    t_sp = at("S43", "then your spouse")
    shots["S43"] = rows([("1", "A guardian appointed by a court"), ("2", "The spouse"), ("3", "Adult children"),
                         ("4", "Parents"), ("5", "Siblings")],
                        [at("S43", "chosen anyone"), t_sp, at("S43", "adult children"), at("S43", "then your parents"),
                         at("S43", "then your parents", offset=0.6)],
                        header="FLORIDA · WHO SPEAKS FOR YOU", label="RECORD", source="Fla. Stat. § 765.401")
    shots["S44"] = num("68%", "SURROGATES' ACCURACY", "predicting patients' treatment choices · 16 studies",
                       "Shalowitz, Garrett-Mayer & Wendler, Arch Intern Med, 2006", colour=G.BRASS,
                       at=at("S44", "surrogates predicted"))
    shots["S45"] = card("The decision-maker must consider “the person's past and present wishes and feelings” and "
                        "“the beliefs and values that would be likely to influence his decision.”", "RECORD",
                        "Mental Capacity Act 2005, s. 4 (England and Wales)")
    t_dis = at("S46", "disability rights")
    shots["S46"] = G.seq((card("“…a natural means of preserving life, not a medical act.”", "RECORD",
                               "Pope John Paul II, March 20, 2004"), t_dis),
                         (card("“…a feeding tube is a low-tech support, and people who use them can and do live full "
                               "and meaningful lives.”", "ARGUMENT",
                               "Statement of 23 national disability organizations, Oct 27, 2003"), 1))
    shots["S47"] = num("43%", "MISDIAGNOSED", "of 40 patients referred as vegetative · one London unit",
                       "Andrews et al., BMJ, 1996", at=at("S47", "In one London"))
    shots["S48"] = E.clip_shot(C("scale_tip_left"), tag=None,
                               overlay=weight("EVIDENCE · THE LAW ASKS WHAT YOU WANTED. MOST OF US NEVER SAY."))

    # V. THE VERDICT
    shots["S49"] = G.title_shot("V · THE VERDICT")
    shots["S50"] = E.clip_shot(C("scale_tip_left"), tag=None,
                               overlay=weight("THE STRONGEST CASE: THE COURTS GOT IT RIGHT"))
    shots["S51"] = E.clip_shot(C("scale_tip_right"), tag=None,
                               overlay=weight("THE STRONGEST CASE: WHEN IN DOUBT, CHOOSE LIFE"))
    shots["S52"] = G.verdict_shot("When a family can't agree, a judge should decide, on the person's own words and the "
                                  "medical evidence. Not a legislature, and not whoever is loudest.", 80,
                                  "Evidence that judges in contested cases decide less faithfully to patients' wishes "
                                  "than families or doctors would.",
                                  meter_at=at("S52", "Our confidence"), change_at=at("S52", "What would change"),
                                  kicker="WHO DECIDES")
    shots["S53"] = G.verdict_shot("The courts got her case right. Her words were thin, but they were tested harder than "
                                  "in almost any case before or since, and the medicine agreed.", 70,
                                  "Credible evidence that the testimony about her words was invented, or that she was "
                                  "minimally conscious.",
                                  meter_at=at("S53", "Our confidence"), change_at=at("S53", "What would change"),
                                  kicker="TERRI SCHIAVO")
    shots["S54"] = G.verdict_shot("Florida and Congress were wrong to step into one family's case after the courts had "
                                  "ruled.", 85,
                                  "Evidence that the courts' process was actually deficient: that something that "
                                  "mattered was never heard.",
                                  meter_at=at("S54", "Our confidence"), change_at=at("S54", "What would change"),
                                  kicker="THE POLITICIANS")
    shots["S55"] = E.clip_shot(C("scale_level_loaded", start=4), tag=None, fout=1.5)
    shots["S56"] = stack([("NEXT CASE", G.MONO(30, True), G.RED),
                          (NEXT_NAME, G.SANS(58, "SemiBold"), G.INK),
                          (NEXT_Q, G.SERIF_I(46), G.DIM)],
                         [0.3, at("S56", NEXT_AT[0]), at("S56", NEXT_AT[1])])
    shots["S57"] = E1.endcard_shot()
    return shots


# ---------------------------------------------------------------- sound

def music(ctx):
    return [("S01", "S09", S.cue_open, 2), ("S10", "S18", S.cue_patient, 0), ("S19", "S29", S.cue_law, -1),
            ("S30", "S40", S.cue_tower, -1), ("S41", "S48", S.cue_science, -2), ("S49", "S57", S.cue_verdict, 0)]


def sfx(ctx):
    at = ctx.at
    ev = [("S01", 0.0, S.hum(ctx.dur["S01"], vol=0.025), -18), ("S20", 0.0, S.hum(ctx.dur["S20"], vol=0.02), -20),
          ("S09", 0.2, S.hit(), -3), ("S03", 0.4, S.hit(0.5), -10), ("S06", 0.4, S.hit(0.4), -12),
          ("S39", 0.4, S.hit(0.5), -12)]
    for sid in ("S02", "S12", "S13", "S14", "S17", "S21", "S22", "S23", "S24", "S27", "S28", "S32", "S33",
                "S36", "S42", "S45", "S46"):
        ev.append((sid, 0.0, S.card_drop(), -10))
    for sid, ph in (("S15", "view was that"), ("S34", "The White House"), ("S36", "Another"),
                    ("S39", "But the neuropathologist"), ("S42", "Justice Scalia"), ("S46", "disability rights")):
        ev.append((sid, at(sid, ph), S.card_drop(), -10))
    for sid in ("S18", "S29", "S40", "S48", "S50", "S51"):
        ev.append((sid, 0.3, S.clink(), -11))
    for sid in ("S52", "S53", "S54"):
        ev.append((sid, at(sid, "Our confidence"), S.whoosh(1.4), -12))
    for sid in ("S10", "S19", "S30", "S41", "S49"):
        ev.append((sid, 0.1, S.whoosh(1.6), -10))
    return ev


if __name__ == "__main__":
    E.main(sys.modules[__name__])
