"""Weight of Evidence, Case 06: The Central Park Five. Shot definitions for edit.py.

    python ep06.py <prod_dir> --stills | --only S02,S13 | --final -j 2

Shot ids, picture notes and research IDs are in episodes/06-the-central-park-five/script.md.
Care rules (research §K): no image of the five men at any age and nothing from the videotaped
statements; Trisha Meili is named, never "the jogger", and nothing about her injuries beyond
"close to death"; the man whose DNA matched is named once (S32) and never shown; every
interrogation room is empty; the NYPD panel and the prosecutors' dissent are given their own cards.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import edit as E  # noqa: E402
import ep01 as E1  # noqa: E402  (shared helpers: stacked words, end card, overlays)
import ep02 as E2  # noqa: E402  (shared helpers: dated rows, big words, lower thirds)
import ep04 as E4  # noqa: E402  (shared helpers: number, lines)
import gfx as G  # noqa: E402
import score as S  # noqa: E402

OUT_NAME = "weight_of_evidence_case06.mp4"
TITLE = "Weight of Evidence, Case 06: The Central Park Five"

SILENT = {"S09": 6.5, "S10": 3.4, "S20": 3.4, "S31": 3.4, "S40": 3.4, "S48": 3.4, "S56": 20.0}
LEAD = {"S01": 2.0, "S02": 0.6, "S04": 0.6, "S11": 0.8, "S21": 0.6, "S32": 0.6, "S41": 0.6,
        "S49": 0.6, "S55": 0.8}
PAD = {"S01": 0.8, "S02": 1.2, "S03": 1.4, "S04": 1.4, "S05": 1.6, "S06": 1.4, "S07": 1.6,
       "S08": 1.2, "S12": 1.6, "S14": 1.6, "S16": 1.6, "S17": 1.4, "S19": 1.8, "S22": 1.4,
       "S25": 1.4, "S28": 1.6, "S30": 1.8, "S33": 1.4, "S35": 1.4, "S37": 1.6, "S39": 2.0,
       "S43": 1.2, "S46": 1.2, "S47": 1.8, "S51": 3.0, "S52": 3.0, "S53": 3.0, "S54": 2.0, "S55": 2.4}
FADE_IN = {"S01": 1.4, "S10": 0.6, "S20": 0.6, "S31": 0.6, "S40": 0.6, "S48": 0.6}
FADE_OUT = {"S08": 0.4, "S09": 1.0, "S19": 1.0, "S30": 1.0, "S39": 1.2, "S47": 1.2, "S54": 1.5, "S56": 1.5}
CHAPTERS = [("S01", "New York, 1989"), ("S10", "I. The night"), ("S20", "II. The statements"),
            ("S31", "III. The match"), ("S40", "IV. The rules"), ("S48", "V. The verdict"),
            ("S55", "Next case")]

AFF = "Manhattan DA, Affirmation, Dec 5, 2002"
ARM = "Central Park Jogger Case Panel Report, to the NYPD, Jan 27, 2003"
SRP = "Kassin et al., Law and Human Behavior, 2025"

# Case 07 teaser card: set once the line is fact-checked (Case 07 research, section 0)
NEXT_NAME = "TERRI SCHIAVO · 1990"
NEXT_Q = "Who should decide when to stop keeping someone alive?"
NEXT_AT = ("young woman", "Who should")


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
    shots["S01"] = E.clip_shot(C("room_push"), overlay=lower("New York", "APRIL 1989", 2.4))
    shots["S02"] = num("4 OF 5", "VIDEOTAPED STATEMENTS", "the fifth was never recorded", AFF,
                       at=at("S02", "Four of them"))
    shots["S03"] = card("A detective told him his fingerprints could be on her clothing. There were no such prints.",
                        "INFERENCE", "Trial testimony, as reported by the New York Times · Drizin & Leo, 2004")
    shots["S04"] = big("NO PHYSICAL EVIDENCE", 84, sub="the DNA at the scene matched none of them · convicted in 1990",
                       sub_at=at("S04", "The DNA found"))
    shots["S05"] = rows([("2002", "Another man confesses; his DNA matches"),
                         ("DEC 19, 2002", "Every conviction vacated")],
                        [0.4, at("S05", "asked the court")], label="RECORD", source=AFF + " · NYPD panel, 2003")
    shots["S06"] = card("“…while relevant, insufficient in our view to make this otherwise voluntary confession "
                        "inadmissible.”", "RECORD", "Frazier v. Cupp, U.S. Supreme Court, 1969")
    shots["S07"] = E.clip_shot(C("scale_empty"), tag=None)
    shots["S08"] = G.words_shot("We'll give you a verdict, and tell you how sure we are.", size=64,
                                emphasis={"how", "sure"}, per_word=0.3, start=at("S08", "At the end"))
    shots["S09"] = G.title_shot("THE CENTRAL PARK FIVE", "Should police be allowed to lie to suspects?",
                                "WEIGHT OF EVIDENCE · CASE 06")

    # I. THE NIGHT
    shots["S10"] = G.title_shot("I · THE NIGHT")
    shots["S11"] = E.clip_shot(C("park_path"), overlay=lower("Central Park, New York", "APRIL 19, 1989", 1.2))
    shots["S12"] = card("Trisha Meili, 29, went out to run at about 8:55 p.m. She was found about 1:30 a.m., "
                        "close to death.", "RECORD", AFF)
    shots["S13"] = rows([("UNDER 16", "A parent or guardian must be present"), ("16", "Questioned as an adult")],
                        [at("S13", "anyone under"), at("S13", "At sixteen")],
                        header="NEW YORK, 1989", label="INFERENCE", source="NYPD panel report, 2003 · Drizin & Leo, 2004")
    shots["S14"] = rows([("14", "Kevin Richardson"), ("14", "Raymond Santana"), ("15", "Antron McCray"),
                         ("15", "Yusef Salaam"), ("16", "Korey Wise")],
                        [at("S14", "Kevin Richardson"), at("S14", "Raymond Santana"), at("S14", "Antron"),
                         at("S14", "Yusef"), at("S14", "Wise was sixteen")],
                        header="AGE IN APRIL 1989", label="RECORD", source=AFF)
    t_card = at("S15", "But the camera")
    shots["S15"] = G.seq((E.clip_shot(C("room_camera")), t_card),
                         (card("“…the earlier interrogation sessions had not been taped.”", "INFERENCE",
                               "Drizin & Leo, North Carolina Law Review, 2004"), 1))
    shots["S16"] = card("“…changed his story after the detective said falsely … that his fingerprints were found "
                        "on the victim's pants.”", "INFERENCE",
                        "New York Times, on trial testimony · other accounts: “would be found”, “if … found”")
    shots["S17"] = card("“None of them admitted actually raping the Central Park jogger, but each gave an account of "
                        "events in which he made himself an accomplice to the crime.”", "RECORD", AFF)
    shots["S18"] = rows([("THE BOYS", "Yelled at, called liars, told they could go home"),
                         ("THE JUDGE", "Every statement admitted but one remark")],
                        [at("S18", "Before trial"), at("S18", "The judge")],
                        header="THE HEARING · 1989–90", label="RECORD",
                        source="NYPD panel report, 2003, quoting Justice Galligan")
    shots["S19"] = E.clip_shot(C("scale_tip_left"), tag=None,
                               overlay=weight("EVIDENCE · FIVE BOYS, HOURS UNRECORDED, ONE LIE ON THE RECORD"))

    # II. THE STATEMENTS
    shots["S20"] = G.title_shot("II · THE STATEMENTS")
    shots["S21"] = rows([("AUG 1990", "McCray, Salaam, Santana convicted"),
                         ("DEC 1990", "Richardson convicted; Wise, but not of rape")],
                        [at("S21", "In August"), at("S21", "In December")], label="RECORD", source=AFF)
    shots["S22"] = card("“The People's case at both trials rested almost entirely on the statements made by the "
                        "defendants.”", "RECORD", AFF)
    shots["S23"] = card("“There proved to be no physical or forensic evidence … which connected the defendants to "
                        "the attack on the jogger.”", "RECORD", AFF)
    shots["S24"] = rows([("1", "Who started it"), ("2", "Who knocked her down"), ("3", "Who held her"),
                         ("4", "What weapons were used"), ("5", "When it happened")],
                        [at("S24", "who started"), at("S24", "who knocked"), at("S24", "who held"),
                         at("S24", "what weapons"), at("S24", "when it happened")],
                        header="THE STATEMENTS DIFFERED ON", label="RECORD", source=AFF + ", ¶86")
    shots["S25"] = card("“Perhaps most significant, none of the defendants accurately described where the attack on "
                        "the jogger took place.”", "RECORD", AFF)
    shots["S26"] = num("94%", "SIGNED A FALSE CONFESSION", "after a false witness · up from 48%",
                       "Kassin & Kiechel, 1996, as reported in Kassin, 2005", colour=G.BRASS,
                       at=at("S26", "rose from"))
    shots["S27"] = card("Observers “were not better than chance” at telling true confessions from false ones.",
                        "RECORD", "Kassin, American Psychologist, 2005")
    t_42 = at("S28", "In another")
    t_half = at("S28", "That study also")
    shots["S28"] = G.seq((num("1 IN 3", "OF 125 PROVEN FALSE CONFESSIONS", "were made by juveniles",
                              "Drizin & Leo, 2004", at=at("S28", "about a third")), t_42),
                         (num("42%", "OF JUVENILE EXONEREES", "had falsely confessed", "Gross et al., 2005",
                              colour=G.BRASS, at=0.4), t_half - t_42),
                         (card("“Five of the false confessions in rape exonerations—more than half of the total—"
                               "were in the Central Park jogger case.”", "RECORD", "Gross et al., 2005"), 1))
    shots["S29"] = num("29%", "OF 375 DNA EXONERATIONS", "involved a false confession", "Innocence Project, 1989–2020",
                       colour=G.BRASS, at=at("S29", "about three"))
    shots["S30"] = E.clip_shot(C("scale_tip_right"), tag=None,
                               overlay=weight("EVIDENCE · NO PHYSICAL LINK, AND STATEMENTS THAT DIDN'T FIT"))

    # III. THE MATCH
    shots["S31"] = G.title_shot("III · THE MATCH")
    shots["S32"] = rows([("LATE 2001", "A prisoner speaks up"), ("JAN 17, 2002", "He says he did it, alone"),
                         ("FEB 2002", "The DA's office is told")],
                        [0.4, at("S32", "His name was"), at("S32", "chance meeting")], label="RECORD", source=AFF)
    shots["S33"] = num("1 IN 6 BILLION", "HIS DNA MATCHED", "no one else's DNA was present", AFF, colour=G.BRASS,
                       at=at("S33", "the FBI reported"))
    shots["S34"] = card("“…a serial rapist was also at large. The newly discovered evidence provides incontrovertible "
                        "proof that he was.”", "RECORD", AFF)
    t_tej = at("S35", "On December")
    shots["S35"] = G.seq((card("“The People consent to the relief requested and recommend that the Court vacate the "
                               "defendants' convictions in their entirety.”", "RECORD",
                               "Nancy E. Ryan, Manhattan DA's office, Dec 5, 2002"), t_tej),
                         (rows([("DEC 19, 2002", "Justice Tejada vacates every conviction"),
                                ("AUG 2002", "Korey Wise already released")],
                               [0.3, at("S35", "Korey Wise had", offset=-t_tej)], label="RECORD",
                               source="NYPD panel report, 2003 · National Registry of Exonerations"), 1))
    t_fair = at("S36", "Linda")
    shots["S36"] = G.seq((card("“…it is more likely than not that the defendants participated in an attack upon the "
                               "jogger.”", "RECORD", ARM), t_fair),
                         (card("The five should not have been “totally” exonerated.", "ARGUMENT",
                               "Linda Fairstein, as reported, 2019"), 1))
    shots["S37"] = card("“I know I have no memory.” … “I always knew that there was at least one more person involved "
                        "because there was unidentified DNA.”", "INFERENCE", "Trisha Meili, ABC News, May 2019")
    shots["S38"] = rows([("2014", "$41 million settlement; no admission of wrongdoing"),
                         ("2022", "Gate of the Exonerated, Central Park"),
                         ("2024", "Yusef Salaam joins the New York City Council")],
                        [at("S38", "In 2014"), at("S38", "In 2022"), at("S38", "now represents")],
                        label="INFERENCE", source="AP, 2014 · Central Park Conservancy · NYC Council")
    shots["S39"] = E.clip_shot(C("scale_tip_right", start=2), tag=None,
                               overlay=weight("EVIDENCE · THE DNA FOUND A MAN THE STATEMENTS NEVER MENTIONED"))

    # IV. THE RULES
    shots["S40"] = G.title_shot("IV · THE RULES")
    shots["S41"] = card("“The fact that the police misrepresented the statements that Rawls had made is, while "
                        "relevant, insufficient in our view to make this otherwise voluntary confession "
                        "inadmissible.”", "RECORD", "Frazier v. Cupp, 394 U.S. 731 (1969)")
    t_jdb = at("S42", "In 2011")
    shots["S42"] = G.seq((card("“…the questioning was of short duration, and petitioner was a mature individual of "
                               "normal intelligence.”", "RECORD", "Frazier v. Cupp, 1969"), t_jdb),
                         (card("“…a reasonable child subjected to police questioning will sometimes feel pressured to "
                               "submit when a reasonable adult would feel free to go.”", "INFERENCE",
                               "J.D.B. v. North Carolina, 2011"), 1))
    t_pace = at("S43", "Under a 1984")
    shots["S43"] = G.seq((card("Officers “decided to invent evidence”: “a fingerprint of his had been found in a very "
                               "telling place.”", "RECORD", "R v Mason, Court of Appeal, 1987"), t_pace),
                         (rows([("s. 76", "A likely unreliable confession is excluded, even if true"),
                                ("s. 78", "Evidence that harms a fair trial can be refused")],
                               [0.3, at("S43", "and must exclude", offset=-t_pace)],
                               header="POLICE AND CRIMINAL EVIDENCE ACT 1984", label="RECORD"), 1))
    t_peace = at("S44", "new way of interviewing")
    shots["S44"] = rows([("P", "Preparation and planning"), ("E", "Engage and explain"), ("A", "Account"),
                         ("C", "Closure"), ("E", "Evaluate")],
                        [t_peace + 0.3 * k for k in range(5)],
                        header="PEACE · ENGLAND AND WALES, 1992", label="RECORD", source=SRP)
    shots["S45"] = rows([("JULY 2021", "Illinois · Oregon"), ("2022", "California · Delaware · Utah"),
                         ("2023", "Colorado · Connecticut · Indiana · Nevada"), ("2024", "Minnesota")],
                        [at("S45", "In July"), at("S45", "Eight more"), at("S45", "Eight more", offset=0.6),
                         at("S45", "Eight more", offset=1.2)],
                        header="RESTRICTING POLICE LIES TO MINORS", label="INFERENCE", source=SRP + " · state statutes")
    shots["S46"] = card("In every state, police may still lie to adults about the evidence.", "INFERENCE",
                        "NPR, 2024 · " + SRP)
    shots["S47"] = E.clip_shot(C("scale_tip_left"), tag=None,
                               overlay=weight("EVIDENCE · THE LAW STILL ALLOWS THE LIE. THE LINE IS MOVING TO AGE."))

    # V. THE VERDICT
    shots["S48"] = G.title_shot("V · THE VERDICT")
    shots["S49"] = E.clip_shot(C("scale_tip_left"), tag=None, overlay=weight("THE STRONGEST CASE: LET POLICE BLUFF"))
    shots["S50"] = E.clip_shot(C("scale_tip_right"), tag=None, overlay=weight("THE STRONGEST CASE: NO LIES IN THE ROOM"))
    shots["S51"] = G.verdict_shot("The statements should never have convicted them. The lie was one part of what went "
                                  "wrong; age, hours of unrecorded questioning and a tape of only the end did more.", 85,
                                  "Reliable evidence, beyond the statements, that any of the five took part in the "
                                  "attack on Trisha Meili.",
                                  meter_at=at("S51", "Our confidence"), change_at=at("S51", "What would change"),
                                  kicker="THE EXONERATED FIVE")
    shots["S52"] = G.verdict_shot("No. Police should not be allowed to lie to children about the evidence, or promise "
                                  "them leniency they can't give.", 85,
                                  "Field evidence that the new state laws cost true confessions in serious cases "
                                  "without reducing false ones.",
                                  meter_at=at("S52", "Our confidence"), change_at=at("S52", "What would change"),
                                  kicker="THE CHILD IN THE ROOM")
    shots["S53"] = G.verdict_shot("Not about the evidence. A confession that follows a lie about the evidence should be "
                                  "presumed unreliable, for adults too.", 65,
                                  "Evidence from England or elsewhere that serious crimes go unsolved because police "
                                  "can't bluff.",
                                  meter_at=at("S53", "Our confidence"), change_at=at("S53", "What would change"),
                                  kicker="EVERYONE ELSE")
    shots["S54"] = E.clip_shot(C("scale_level_loaded", start=4), tag=None, fout=1.5)
    shots["S55"] = stack([("NEXT CASE", G.MONO(30, True), G.RED),
                          (NEXT_NAME, G.SANS(58, "SemiBold"), G.INK),
                          (NEXT_Q, G.SERIF_I(46), G.DIM)],
                         [0.3, at("S55", NEXT_AT[0]), at("S55", NEXT_AT[1])])
    shots["S56"] = E1.endcard_shot()
    return shots


# ---------------------------------------------------------------- sound

def music(ctx):
    return [("S01", "S09", S.cue_open, 2), ("S10", "S19", S.cue_patient, 0), ("S20", "S30", S.cue_science, -2),
            ("S31", "S39", S.cue_tower, -1), ("S40", "S47", S.cue_law, -1), ("S48", "S56", S.cue_verdict, 0)]


def sfx(ctx):
    at = ctx.at
    ev = [("S01", 0.0, S.hum(ctx.dur["S01"], vol=0.025), -18), ("S11", 0.0, S.hum(ctx.dur["S11"], vol=0.02), -20),
          ("S15", 0.0, S.hum(ctx.dur["S15"], vol=0.025), -18),
          ("S09", 0.2, S.hit(), -3), ("S02", 0.4, S.hit(0.5), -10), ("S04", 0.3, S.hit(0.4), -12),
          ("S33", 0.4, S.hit(0.5), -10)]
    for sid in ("S03", "S06", "S12", "S16", "S17", "S22", "S23", "S25", "S27", "S34", "S35", "S36", "S37",
                "S41", "S42", "S43", "S46"):
        ev.append((sid, 0.0, S.card_drop(), -10))
    for sid, ph in (("S15", "But the camera"), ("S28", "That study also"), ("S36", "Linda"), ("S42", "In 2011")):
        ev.append((sid, at(sid, ph), S.card_drop(), -10))
    for sid in ("S19", "S30", "S39", "S47", "S49", "S50"):
        ev.append((sid, 0.3, S.clink(), -11))
    for sid in ("S51", "S52", "S53"):
        ev.append((sid, at(sid, "Our confidence"), S.whoosh(1.4), -12))
    for sid in ("S10", "S20", "S31", "S40", "S48"):
        ev.append((sid, 0.1, S.whoosh(1.6), -10))
    return ev


if __name__ == "__main__":
    E.main(sys.modules[__name__])
