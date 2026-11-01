"""Weight of Evidence, Case 09: Cameron Todd Willingham. Shot definitions for edit.py, hybrid look.

    python ep09.py <prod_dir> --stills | --only S02,S13 | --final -j 2

Shot ids, picture notes and research IDs are in episodes/09-cameron-todd-willingham/script.md.
graphics() lays out the cards, rows, numbers and verdicts as the script describes; build() puts the
picture under them (FORMAT.md §2): the fax on the night desk, the flashover test room, the desk with
the record's own words, the courtroom and the Scale from Blender, and a few Higgsfield clips of real
places (anim/ai_*.mp4).

Care rules (research §K): no images of the children, nothing about their injuries; no re-enactment of
the fire: the only fire imagery is the empty test room in Act IV, tagged ILLUSTRATION · NOT DATA, and it
never appears before the science is explained; no execution imagery: the last statement (S33) and the
sentence (S26) stay on black; no one involved is depicted. Our voice never says "innocent",
"exonerated", "cleared" or "wrongfully executed".
"""

import os
import sys
import textwrap

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import edit as E  # noqa: E402
import ep01 as E1  # noqa: E402  (shared helpers: stacked words, end card, overlays)
import ep02 as E2  # noqa: E402  (shared helpers: dated rows, big words, lower thirds)
import ep04 as E4  # noqa: E402  (shared helpers: number, bars)
import footage as F  # noqa: E402
import gfx as G  # noqa: E402
import score as S  # noqa: E402

OUT_NAME = "weight_of_evidence_case09.mp4"
TITLE = "Weight of Evidence, Case 09: Cameron Todd Willingham"

SILENT = {"S09": 6.5, "S10": 3.4, "S19": 3.4, "S28": 3.4, "S35": 3.4, "S46": 3.4, "S54": 20.0}
LEAD = {"S01": 2.0, "S02": 0.6, "S11": 0.8, "S20": 0.6, "S26": 1.0, "S29": 0.6, "S33": 1.0, "S36": 0.8,
        "S47": 0.6, "S53": 0.8}
PAD = {"S01": 0.8, "S02": 1.4, "S03": 1.8, "S04": 1.6, "S05": 1.6, "S06": 1.4, "S07": 1.6, "S08": 1.2,
       "S11": 1.4, "S12": 1.6, "S13": 1.6, "S14": 1.6, "S15": 1.4, "S16": 1.6, "S17": 1.6, "S18": 1.8,
       "S21": 1.6, "S22": 1.4, "S23": 1.4, "S24": 1.4, "S25": 1.6, "S26": 2.4, "S27": 1.8, "S29": 1.6,
       "S30": 1.6, "S31": 1.6, "S32": 1.6, "S33": 3.0, "S34": 1.8, "S36": 1.6, "S37": 1.4, "S38": 1.6,
       "S39": 1.6, "S40": 1.6, "S41": 1.6, "S42": 1.4, "S43": 1.6, "S44": 1.4, "S45": 1.8, "S47": 1.6,
       "S48": 1.8, "S49": 3.0, "S50": 3.0, "S51": 3.0, "S52": 2.0, "S53": 2.4}
FADE_IN = {"S01": 1.4, "S10": 0.6, "S19": 0.6, "S26": 0.8, "S28": 0.6, "S33": 0.8, "S35": 0.6, "S46": 0.6}
FADE_OUT = {"S08": 0.4, "S09": 1.0, "S18": 1.0, "S26": 1.0, "S27": 1.0, "S33": 1.2, "S34": 1.2, "S45": 1.2,
            "S52": 1.5, "S54": 1.5}
CHAPTERS = [("S01", "Texas, 2004"), ("S10", "I. The fire"), ("S19", "II. The trial"),
            ("S28", "III. The last four days"), ("S35", "IV. The science"), ("S46", "V. The verdict"),
            ("S53", "Next case")]

TFSC = "Texas Forensic Science Commission, 2011"
BEY = "Dr. Craig Beyler, for the Texas Forensic Science Commission, 2009"
NY = "The New Yorker, 2009"
CCA = "Willingham v. State, Texas Court of Criminal Appeals, 1995"

# verbatim, TDCJ (research C11); S33 shows it typed, on black: no image of the chamber
LAST_STATEMENT = ("Yeah. The only statement I want to make is that I am an innocent man - convicted of a crime I "
                  "did not commit. I have been persecuted for 12 years for something I did not do. From God's dust "
                  "I came and to dust I will return - so the earth shall become my throne. I gotta go, road dog. "
                  "I love you Gabby.")

# Case 10 teaser card (checked in Case 10 research, section 0)
NEXT_NAME = "TARASOFF · 1969"
NEXT_Q = "Should a therapist break a patient's confidence to warn someone in danger?"
NEXT_AT = ("Berkeley, 1969", "Should a therapist")

# honesty tag per clip (generated ai_* clips get "ILLUSTRATIVE · AI-GENERATED" from footage.py)
ILL = "ILLUSTRATIVE"
TXT = "RECONSTRUCTION · TEXT FROM "
FIRE = "ILLUSTRATION · NOT DATA"
TAGS = {"fax_push": "RECONSTRUCTION", "fax_page": "RECONSTRUCTION", "fire_push": FIRE, "fire_floor": FIRE,
        "desk_hurst": TXT + "HURST'S REPORT, 2004", "desk_vasquez": TXT + "THE COMMISSION'S REPORT, 2011",
        "desk_beyler": TXT + "BEYLER'S REPORT, 2009", "desk_herrera": TXT + "HERRERA v. COLLINS, 1993"}
for _c in ("court_push", "court_bench", "court_witness", "court_gallery", "courtroom_push", "courtroom_bench",
           "desk_blank_pen", "evidence_shelf", "tier_corridor", "cell_door"):
    TAGS[_c] = ILL

# when each card lands: card_after() delays (footage plays clean first)
CARD_AT = {"S02": 3.0, "S05": 3.0, "S12": 3.0, "S13": 3.0, "S16": 3.0, "S21": 3.0, "S22": 3.0, "S25": 3.0,
           "S29": 3.0, "S32": 3.0, "S39": 3.0, "S41": 3.0}


# ---------------------------------------------------------------- the graphics

def graphics(ctx):
    P = ctx.prod
    C = lambda name, **kw: E.Clip(P, name, **kw)
    at = ctx.at
    rows = E2.rows_shot
    weight = E1.scale_overlay
    lower = E2.lower
    big = E2.big_words
    card = G.card_shot
    num = E4.number_shot
    stack = E1.stacked_words_shot
    shots = {}

    def handoff(sid, phrase):
        """When the second card of a two-card shot takes over: the narration time, less the delay
        build() puts before the whole card shot (CARD_AT), so it lands on the words."""
        return max(0.5, at(sid, phrase) - CARD_AT[sid])

    # COLD OPEN
    shots["S01"] = E.clip_shot(C("fax_push"), tag="RECONSTRUCTION",
                               overlay=lower("Texas", "FEBRUARY 13, 2004", 2.4))
    shots["S02"] = card("“…most of the conclusions reached by the Fire Marshall would be considered invalid in "
                        "light of current knowledge.”", "RECORD",
                        "Dr. Gerald Hurst, report for the clemency petition, Feb 13, 2004")
    shots["S03"] = rows([("DEC 23, 1991", "A house fire in Corsicana, Texas"),
                         ("AUG 1992", "Convicted of capital murder"), ("FEB 17, 2004", "Executed")],
                        [at("S03", "The fire was"), at("S03", "Their father"), at("S03", "Their father", offset=1.2)],
                        label="RECORD", source="Willingham v. State, 1995 · TDCJ")
    shots["S04"] = rows([("FEB 13, 2004", "The parole board: 15–0 against clemency"),
                         ("FEB 17, 2004", "No reprieve from the governor; executed")],
                        [at("S04", "The parole board"), at("S04", "The governor")],
                        label="RECORD", source="Board of Pardons and Paroles, Feb 13, 2004 · TDCJ")
    t_st = handoff("S05", "And the girls'")
    shots["S05"] = G.seq((card("“A finding of arson could not be sustained.”", "RECORD", BEY), t_st),
                         (card("“My ex-husband murdered my daughters, and just before he was executed, he told me "
                               "he did it.”", "ARGUMENT", "Stacy Kuykendall, Oct 6, 2010"), 1))
    shots["S06"] = num("4%", "DEATH SENTENCES THAT ARE FALSE CONVICTIONS", "at least · a conservative estimate",
                       "Gross, O'Brien, Hu & Kennedy, PNAS, 2014", colour=G.BRASS, at=at("S06", "at least four"))
    shots["S07"] = E.clip_shot(C("scale_empty"), tag=None)
    shots["S08"] = G.words_shot("We'll give you a verdict, and tell you how sure we are.", size=64,
                                emphasis={"how", "sure"}, per_word=0.3, start=0.2)  # build() cuts to it
    shots["S09"] = G.title_shot("CAMERON TODD WILLINGHAM", "Should a state execute someone when the evidence is "
                                "disputed?", "WEIGHT OF EVIDENCE · CASE 09")

    # I. THE FIRE
    shots["S10"] = G.title_shot("I · THE FIRE")
    shots["S11"] = rows([("ABOUT 9:15 A.M.", "Stacy goes out to pick up a Christmas present"),
                         ("10:34 A.M.", "The fire, by Beyler's timeline"),
                         ("HIS ACCOUNT", "Woken by Amber calling; smoke; he couldn't reach the twins")],
                        [at("S11", "On the morning"), at("S11", "His account"), at("S11", "He said he tried")],
                        label="INFERENCE", source="Beyler, 2009 · " + NY)
    shots["S12"] = card("Neighbors saw smoke at the front door, then flames when the bedroom windows broke; then the "
                        "bedroom reached flashover.", "INFERENCE", "Dr. Craig Beyler's reading of the witness statements, 2009")
    t_fn = handoff("S13", "The state commission")
    shots["S13"] = G.seq((card("“The fire tells a story. I am just the interpreter.”", "RECORD",
                               "Manuel Vasquez, trial testimony, 1992, as quoted by the commission"), t_fn),
                         (card("The commission noted this phrasing was commonly taught at training seminars of the day.",
                               "RECORD", TFSC), 1))
    shots["S14"] = rows([("POUR PATTERNS", "Shapes on the floor, read as poured liquid"),
                         ("LOW BURNS", "Floor hotter than ceiling"), ("THREE ORIGINS", "Fires started in three places"),
                         ("CRAZED GLASS", "Read as a fast, hot fire"),
                         ("THE THRESHOLD", "Charring under the front door's metal strip")],
                        [at("S14", "Shapes on the floor"), at("S14", "Burning low"), at("S14", "Three separate"),
                         at("S14", "Cracked"), at("S14", "And charring")],
                        label="RECORD", source="Vasquez's testimony, as quoted by the " + TFSC)
    shots["S15"] = rows([("SAMPLES", "An unknown number sent to the lab"), ("POSITIVE", "One: at the front-door threshold"),
                         ("FOUND", "Charcoal lighter fluid; a grill had stood on the porch")],
                        [at("S15", "Samples went"), at("S15", "One came back"), at("S15", "A barbecue grill")],
                        label="RECORD", source=TFSC + " · Beyler, 2009")
    shots["S16"] = card("“…entirely consistent with being exposed to a room fire environment…”", "RECORD",
                        "Dr. Craig Beyler, on Willingham's injuries, 2009")
    shots["S17"] = rows([("JAN 8, 1992", "Arrested, sixteen days after the fire"),
                         ("MOTIVE", "None ever established")],
                        [at("S17", "Sixteen days"), at("S17", "No motive")],
                        label="RECORD", source="Willingham v. State, 1995 · " + NY)
    shots["S18"] = E.clip_shot(C("scale_tip_left"), tag=None,
                               overlay=weight("EVIDENCE · A FIRE MARSHAL WHO READ ARSON IN THE FLOOR"))

    # II. THE TRIAL
    shots["S19"] = G.title_shot("II · THE TRIAL")
    shots["S20"] = E.clip_shot(C("courtroom_push"), tag=ILL, overlay=lower("Corsicana, Texas", "AUGUST 1992", 1.2))
    shots["S21"] = card("“So when I found that the floor is hotter than the ceiling, that's backwards, upside down … "
                        "The only reason that the floor is hotter is because there was an accelerant.”", "RECORD",
                        "Manuel Vasquez, trial testimony, 1992")
    shots["S22"] = card("“…appellant openly admitted to a fellow inmate that he purposely started this fire…”",
                        "RECORD", "Texas Court of Criminal Appeals, summarizing the trial evidence, 1995")
    shots["S23"] = rows([("EXPERT", "Agreed it was arson; didn't testify"),
                         ("WITNESSES", "One: the babysitter"), ("THE JURY", "Out about an hour")],
                        [at("S23", "His court-appointed"), at("S23", "They called one"), at("S23", "The jury deliberated")],
                        header="THE DEFENSE", label="INFERENCE", source=NY + " · AP, 2010")
    shots["S24"] = rows([("HIS RECORD", "Burglary, theft and other offenses in Oklahoma"),
                         ("WITNESSES", "Said he had beaten Stacy, including while she was pregnant"),
                         ("STACY", "Testified for him at sentencing")],
                        [at("S24", "He had a record"), at("S24", "Witnesses said"), at("S24", "Stacy herself")],
                        label="RECORD", source="Willingham v. State, 1995 · AP, 2009")
    t_fn = handoff("S25", "Neither of them")
    shots["S25"] = G.seq((card("“…fits the profile of an extremely severe sociopath…”", "RECORD",
                               "Dr. James Grigson's testimony, as summarized by the Court of Criminal Appeals"), t_fn),
                         (card("Neither expert had examined him. The American Psychiatric Association expelled "
                               "Grigson in 1995.", "RECORD", "American Psychiatric Association, 1995"), 1))
    shots["S26"] = big("DEATH", 120)
    shots["S27"] = E.clip_shot(C("scale_tip_right"), tag=None,
                               overlay=weight("EVIDENCE · THE FIRE MARSHAL, AN INFORMANT, AND EXPERTS WHO NEVER MET HIM"))

    # III. THE LAST FOUR DAYS
    shots["S28"] = G.title_shot("III · THE LAST FOUR DAYS")
    t_fs = handoff("S29", "The safety net")
    shots["S29"] = G.seq((card("“…a claim of ‘actual innocence’ is not itself a constitutional claim…”", "RECORD",
                               "Herrera v. Collins, U.S. Supreme Court, 1993"), t_fs),
                         (card("“Executive clemency has provided the ‘fail safe’ in our criminal justice system.”",
                               "RECORD", "Chief Justice Rehnquist, Herrera v. Collins, 1993"), 1))
    shots["S30"] = rows([("“CRAZED GLASS”", "“an ‘Old Wives Tale’”"),
                         ("“THE THRESHOLD”", "“Liquid accelerants can no more burn under an aluminum threshold than "
                                             "can grease burn in a skillet even with a loose-fitting lid”"),
                         ("“POUR PATTERNS”", "Can't be told apart after a room flashes over")],
                        [at("S30", "Crazed glass"), at("S30", "A liquid can"), at("S30", "And once a room")],
                        label="RECORD", source="Dr. Gerald Hurst, report, Feb 13, 2004")
    shots["S31"] = rows([("FEB 3, 2004", "Clemency petition filed"),
                         ("FEB 13", "Hurst's report faxed to the Board and the governor's office"),
                         ("FEB 10–13", "The Board votes 15–0; four votes cast before the report was signed")],
                        [0.4, at("S31", "On February"), at("S31", "The board voted")],
                        label="RECORD", source=TFSC + " · Board of Pardons and Paroles, Feb 13, 2004")
    shots["S32"] = card("The courts “agreed that the new opinion by Gerald Hurst was simply an opinion and did not "
                        "merit reopening the case.”", "INFERENCE", "Lucy Nashed, spokeswoman for Gov. Rick Perry, 2011")
    shots["S33"] = G.document_shot(textwrap.wrap(LAST_STATEMENT, 52),
                                   header="LAST STATEMENT · FEB 17, 2004",
                                   footer="Texas Department of Criminal Justice")
    shots["S34"] = E.clip_shot(C("scale_tip_right", start=2), tag=None,
                               overlay=weight("EVIDENCE · A WARNING IN TIME, AND NO ONE REQUIRED TO TEST IT"))

    # IV. THE SCIENCE
    shots["S35"] = G.title_shot("IV · THE SCIENCE")
    shots["S36"] = E.clip_shot(C("fire_push"), tag=FIRE, overlay=lower("A TEST BURN", "NO ACCELERANT", 1.2))
    shots["S37"] = rows([("POUR PATTERNS", "Made by flashover and melting materials"),
                         ("LOW BURNS", "Radiant heat; floors aren't hotter than ceilings"),
                         ("THREE ORIGINS", "Burning debris dropping, separate patches"),
                         ("CRAZED GLASS", "Water on hot glass; “no longer has any value”"),
                         ("THE THRESHOLD", "Heat at doorways")],
                        [at("S37", "The patterns could"), at("S37", "Low burns"), at("S37", "Separate patches"),
                         at("S37", "Crazed glass"), at("S37", "A Texas commission")],
                        header="WHAT THE SIGNS MEAN NOW", label="RECORD", source=TFSC + " · Hurst, 2004")
    shots["S38"] = rows([("1986", "A fire in West Texas kills two women"),
                         ("1987", "Ernest Ray Willis sentenced to death on “pour patterns”"),
                         ("OCT 2004", "A new prosecutor has the science reviewed; Willis freed")],
                        [at("S38", "Ernest Ray Willis"), at("S38", "had been sentenced"), at("S38", "A new prosecutor")],
                        label="RECORD", source="National Registry of Exonerations · " + TFSC)
    t_bey = handoff("S39", "Texas had just")
    shots["S39"] = G.seq((card("“…each and every one of the indicators relied upon have since been scientifically "
                               "proven to be invalid.”", "RECORD", "Arson Review Committee, 2006"), t_bey),
                         (card("“…more characteristic of mystics or psychics.”", "RECORD",
                               "Dr. Craig Beyler, on the fire marshal's statements, 2009"), 1))
    t_mon, t_dr = at("S40", "He called Willingham"), at("S40", "The chair he replaced")
    shots["S40"] = G.seq((rows([("SEPT 30, 2009", "The governor replaces the commission's chair and members"),
                                ("OCT 2, 2009", "The scheduled hearing on Beyler's report is called off")],
                               [0.4, at("S40", "The new chair")], label="INFERENCE",
                               source="Dallas Morning News, via DPIC · CNN, 2011"), t_mon),
                         (card("“Willingham was a monster.”", "ARGUMENT", "Gov. Rick Perry, Oct 14, 2009"), t_dr - t_mon),
                         (card("“…this kind of endless drumbeat of strategies and actions to stop this "
                               "investigation.”", "ARGUMENT", "Sam Bassett, former commission chair, 2011"), 1))
    t_un = handoff("S41", "In 2011")
    shots["S41"] = G.seq((card("“In reviewing documents and standards in place then and now, we stand by the original "
                               "investigator's report and conclusions.”", "RECORD",
                               "State Fire Marshal's Office, Aug 20, 2010"), t_un),
                         (card("“…an untenable position in light of advances in fire science.”", "RECORD",
                               "Texas Forensic Science Commission, April 15, 2011"), 1))
    shots["S42"] = rows([("1992", "Testifies Willingham confessed"), ("2000", "Tries to recant; withdraws it"),
                         ("2014", "Says he lied in exchange for help"),
                         ("2017", "The prosecutor is cleared by a jury, 11–1")],
                        [at("S42", "The informant"), at("S42", "tried to recant"), at("S42", "In 2014"),
                         at("S42", "and in 2017")],
                        label="INFERENCE", source="CNN, 2014 · The Intercept, 2017 · Marshall Project, 2017")
    shots["S43"] = rows([("2010", "A court of inquiry is stopped before any ruling"),
                         ("APR 3, 2014", "The parole board declines a posthumous pardon")],
                        [at("S43", "That inquiry"), at("S43", "In 2014")], label="INFERENCE",
                        source="Texas Tribune, 2014")
    shots["S44"] = rows([("2011", "Investigators should tell those affected when new science changes old results "
                                  "(recommendation)"),
                         ("2013", "Texas lets courts overturn convictions built on discredited science"),
                         ("1965", "England abolishes the death penalty for murder")],
                        [at("S44", "The commission recommended"), at("S44", "In 2013"), at("S44", "England took")],
                        label="RECORD", source=TFSC + " · Tex. Code Crim. Proc. art. 11.073 · Murder (Abolition of "
                                                      "Death Penalty) Act 1965")
    shots["S45"] = E.clip_shot(C("scale_tip_left"), tag=None,
                               overlay=weight("EVIDENCE · THE SCIENCE CHANGED. THE CONVICTION DIDN'T."))

    # V. THE VERDICT
    shots["S46"] = G.title_shot("V · THE VERDICT")
    shots["S47"] = E.clip_shot(C("scale_tip_left"), tag=None,
                               overlay=weight("THE STRONGEST CASE: THE VERDICT STOOD ON MORE THAN FIRE"))
    shots["S48"] = E.clip_shot(C("scale_tip_right"), tag=None,
                               overlay=weight("THE STRONGEST CASE: DEATH CAN'T BE CORRECTED"))
    shots["S49"] = G.verdict_shot("The signs the jury heard were not evidence of arson, by today's science or by the "
                                  "best fire science of 1991.", 90,
                                  "An independent fire scientist defending those signs on modern science, or lab "
                                  "results showing accelerant where the patterns were.",
                                  meter_at=at("S49", "Our confidence"), change_at=at("S49", "What would change"),
                                  kicker="THE FIRE EVIDENCE")
    shots["S50"] = G.verdict_shot("Texas should not have carried out the execution that day. With a credible scientific "
                                  "challenge to its only physical evidence, it should have used the 30-day reprieve "
                                  "to test it.", 85,
                                  "Records showing a qualified fire scientist reviewed Hurst's report for the State "
                                  "before the execution, and found it wrong on the merits.",
                                  meter_at=at("S50", "Our confidence"), change_at=at("S50", "What would change"),
                                  kicker="FEBRUARY 17, 2004")
    shots["S51"] = G.verdict_shot("No state should carry out an execution while a credible, specific challenge to the "
                                  "evidence that convicted the person has not been heard by someone competent to "
                                  "judge it.", 80,
                                  "Evidence that such a rule is routinely used to delay executions without finding "
                                  "real errors.",
                                  meter_at=at("S51", "Our confidence"), change_at=at("S51", "What would change"),
                                  kicker="THE QUESTION")
    shots["S52"] = E.clip_shot(C("scale_level_loaded", start=4), tag=None, fout=1.5)
    shots["S53"] = stack([("NEXT CASE", G.MONO(30, True), G.RED),
                          (NEXT_NAME, G.SANS(58, "SemiBold"), G.INK),
                          (NEXT_Q, G.SERIF_I(46), G.DIM)],
                         [0.3, at("S53", NEXT_AT[0]), at("S53", NEXT_AT[1])])
    shots["S54"] = E1.endcard_shot()
    return shots


# ---------------------------------------------------------------- the footage under them

def build(ctx):
    P = ctx.prod
    at = ctx.at
    shots = graphics(ctx)
    old = dict(shots)

    def B(*items, **kw):
        return F.broll(P, list(items), tags=TAGS, **kw)

    def Bq(*items):  # footage for under a graphic: over() stamps the tag
        return B(*items, stamp=False)

    def under(sid, *items, clear=0.0):
        """The shot's own graphic over footage; the footage plays clean until `clear`."""
        return F.over(Bq(*items), old[sid], clear_until=clear)

    def card_after(sid, *items):
        """A card shot whose card lands CARD_AT[sid] seconds in, over footage that plays clean until then."""
        d = CARD_AT[sid]
        return F.over(Bq(*items), F.delay(old[sid], d), clear_until=d)

    lower = E2.lower
    weight = E1.scale_overlay

    # ------------------------------------------------------------ COLD OPEN
    c1, c2 = at("S01", "A fire scientist"), at("S01", "The execution")
    shots["S01"] = B(("fax_push", c1), ("ai_capitol", c2 - c1), "fax_page",
                     overlay=lower("Texas", "FEBRUARY 13, 2004", 2.4))
    shots["S02"] = card_after("S02", ("fax_page", 6), "desk_hurst")
    c1 = at("S03", "The fire was")
    shots["S03"] = under("S03", ("ai_tx_town", c1 + 4), "ai_tx_road", clear=c1)
    c1, c2 = at("S04", "The parole board"), at("S04", "The governor")
    shots["S04"] = under("S04", ("ai_hearing", c2), ("ai_capitol", 5), "ai_razor_wire", clear=c1)
    shots["S05"] = card_after("S05", ("ai_fire_lab", 6), ("desk_beyler", 7), "ai_tx_road")
    c1 = at("S06", "at least four")
    shots["S06"] = under("S06", ("ai_razor_wire", c1 + 2), "tier_corridor")  # label lands at 0.3: keep it readable
    q = [at("S08", p) for p in ("the fire reports", "the clemency file", "the state commission's", "and what the law",
                                "At the end")]
    shots["S08"] = G.seq((B(("ai_archive", q[0]), ("ai_lab_cans", q[1] - q[0]), ("fax_page", q[2] - q[1]),
                            ("ai_hearing", q[3] - q[2]), "ai_scotus"), q[4]), (old["S08"], 1))

    # ------------------------------------------------------------ I. THE FIRE (no fire imagery here)
    c1 = at("S11", "On the morning")
    shots["S11"] = under("S11", ("ai_tx_town", c1 + 5), ("ai_tx_road", 6), "ai_lights", clear=c1)
    shots["S12"] = card_after("S12", ("ai_tx_road", 6), "ai_lights")
    shots["S13"] = card_after("S13", ("ai_courthouse_tx", 6), ("desk_vasquez", 9), "evidence_shelf")
    c1 = at("S14", "Shapes on the floor")
    shots["S14"] = under("S14", ("ai_papers", c1 + 4), ("evidence_shelf", 6), ("desk_blank_pen", 6), "ai_archive",
                         clear=c1)
    c1 = at("S15", "Samples went")
    shots["S15"] = under("S15", ("ai_lab_cans", c1 + 5), "evidence_shelf", clear=c1)
    shots["S16"] = card_after("S16", ("ai_papers", 6), "desk_blank_pen")
    c1 = at("S17", "Sixteen days")
    shots["S17"] = under("S17", ("ai_tx_town", c1 + 4), ("ai_court_corridor", 6), "tier_corridor", clear=c1)

    # ------------------------------------------------------------ II. THE TRIAL
    shots["S20"] = B(("ai_courthouse_tx", 5), ("courtroom_push", 7), ("court_witness", 6), "court_gallery",
                     overlay=lower("Corsicana, Texas", "AUGUST 1992", 1.2))
    shots["S21"] = card_after("S21", ("court_witness", 6), "court_bench")
    shots["S22"] = card_after("S22", ("ai_court_corridor", 6), "court_gallery")
    c1 = at("S23", "His court-appointed")
    shots["S23"] = under("S23", ("court_push", c1 + 5), ("ai_clock", 5), "court_gallery", clear=c1)
    c1 = at("S24", "He had a record")
    shots["S24"] = under("S24", ("ai_papers", c1 + 4), "court_bench", clear=c1)
    shots["S25"] = card_after("S25", ("court_witness", 6), "ai_archive")
    # S26 ("DEATH") stays on black

    # ------------------------------------------------------------ III. THE LAST FOUR DAYS
    shots["S29"] = card_after("S29", ("ai_scotus", 6), ("desk_herrera", 9), "court_bench")
    c1 = at("S30", "Crazed glass")
    shots["S30"] = under("S30", ("desk_hurst", c1 + 3), ("fax_page", 6), "ai_fire_lab", clear=c1)
    c1 = at("S31", "On February")
    shots["S31"] = under("S31", ("fax_push", c1 + 3), ("ai_hearing", 6), ("ai_capitol", 5), "ai_clock", clear=c1)
    shots["S32"] = card_after("S32", ("ai_capitol", 6), "ai_court_corridor")
    # S33 (the last statement) stays on black: no image of the chamber

    # ------------------------------------------------------------ IV. THE SCIENCE (the test room appears here)
    c1 = at("S36", "In a few minutes")
    shots["S36"] = B(("ai_fire_lab", c1 - 1), ("fire_push", None, 0.0),
                     overlay=lower("A TEST BURN", "NO ACCELERANT", 1.2))
    c1 = at("S37", "The patterns could")
    shots["S37"] = under("S37", ("fire_floor", c1 + 4), ("ai_fire_lab", 6), "fire_push", clear=c1)
    c1 = at("S38", "Ernest Ray Willis")
    shots["S38"] = under("S38", ("ai_tx_road", c1 + 4), ("tier_corridor", 6), "ai_razor_wire", clear=c1)
    shots["S39"] = card_after("S39", ("ai_fire_lab", 6), ("desk_beyler", 10), "evidence_shelf")
    c1 = at("S40", "Two days before")
    shots["S40"] = under("S40", ("ai_capitol", c1 + 5), ("ai_hearing", 7), "ai_court_corridor", clear=c1)
    shots["S41"] = card_after("S41", ("fire_floor", 6), "ai_archive")
    c1 = at("S42", "The informant")
    shots["S42"] = under("S42", ("ai_papers", c1 + 4), ("court_bench", 6), "court_gallery", clear=c1)
    c1 = at("S43", "That inquiry")
    shots["S43"] = under("S43", ("ai_hearing", c1 + 4), "ai_tx_town", clear=c1)
    c1 = at("S44", "The commission recommended")
    shots["S44"] = under("S44", ("ai_fire_lab", c1 + 4), ("ai_capitol", 6), "ai_westminster", clear=c1)

    # ------------------------------------------------------------ V. THE VERDICT: the two strongest cases
    q = [at("S47", p) for p in ("The conviction never", "His conviction was", "Fire investigators in",
                                "And the person who")]
    s47_card = G.card_shot("“My ex-husband murdered my daughters, and just before he was executed, he told me he did "
                           "it.”", "ARGUMENT", "Stacy Kuykendall, 2010")
    shots["S47"] = G.seq(
        (B(("scale_tip_left", q[0]), ("court_witness", q[1] - q[0]), ("ai_archive", q[2] - q[1]),
           ("evidence_shelf", q[3] - q[2]), overlay=weight("THE STRONGEST CASE: THE VERDICT STOOD ON MORE THAN FIRE")),
         q[3]),
        (F.over(Bq(("ai_tx_road", 6), ("scale_tip_left", None, 3.0)), s47_card, clear_until=0.0), 1))
    q = [at("S48", p) for p in ("The only physical", "What remained", "A credible scientist", "Whether Willingham",
                                "But that's the point")]
    s48_card = G.card_shot("“The execution of a person who can show that he is innocent comes perilously close to "
                           "simple murder.”", "RECORD", "Justice Blackmun, dissenting, Herrera v. Collins, 1993")
    shots["S48"] = G.seq(
        (B(("scale_tip_right", q[0]), ("fire_floor", q[1] - q[0]), ("court_bench", q[2] - q[1]),
           ("fax_page", q[3] - q[2]), ("ai_archive", q[4] - q[3]),
           overlay=weight("THE STRONGEST CASE: DEATH CAN'T BE CORRECTED")), q[4]),
        (F.over(Bq(("ai_scotus", 6), ("scale_tip_right", None, 3.0)), s48_card, clear_until=0.0), 1))
    return shots


# ---------------------------------------------------------------- sound

def music(ctx):
    return [("S01", "S09", S.cue_open, 2), ("S10", "S18", S.cue_patient, -1), ("S19", "S27", S.cue_law, -1),
            ("S28", "S34", S.cue_tower, -1), ("S35", "S45", S.cue_science, -2), ("S46", "S54", S.cue_verdict, 0)]


def sfx(ctx):
    at = ctx.at
    ev = [("S01", 0.0, S.hum(ctx.dur["S01"], vol=0.025), -18), ("S09", 0.2, S.hit(), -3),
          ("S06", at("S06", "at least four"), S.hit(0.4), -12)]
    for sid, d in CARD_AT.items():
        ev.append((sid, d, S.card_drop(), -10))
    for sid, ph in (("S05", "And the girls'"), ("S13", "The state commission"), ("S25", "Neither of them"),
                    ("S29", "The safety net"), ("S39", "Texas had just"), ("S40", "He called Willingham"),
                    ("S40", "The chair he replaced"), ("S41", "In 2011"), ("S47", "And the person who"),
                    ("S48", "But that's the point")):
        ev.append((sid, at(sid, ph), S.card_drop(), -10))
    for sid in ("S18", "S27", "S34", "S45", "S47", "S48"):
        ev.append((sid, 0.3, S.clink(), -11))
    for sid in ("S49", "S50", "S51"):
        ev.append((sid, at(sid, "Our confidence"), S.whoosh(1.4), -12))
    for sid in ("S10", "S19", "S28", "S35", "S46"):
        ev.append((sid, 0.1, S.whoosh(1.6), -10))
    return ev


if __name__ == "__main__":
    E.main(sys.modules[__name__])
