"""Weight of Evidence, Case 08: Kalief Browder. Shot definitions for edit.py, in the hybrid look.

    python ep08.py <prod_dir> --stills | --only S02,S13 | --final -j 2

Shot ids, picture notes and research IDs are in episodes/08-kalief-browder/script.md.
build() lays out the graphics (rows, cards, numbers, verdicts) exactly as the script describes;
footage() then puts the picture under them, changing every few seconds (FORMAT.md §2): our Blender
clips (the empty cell, the tier, the desk with the record's own words, the courtroom, the Scale)
and a few Higgsfield clips (anim/ai_*.mp4) for real places only.

Care rules (research §J): no image of him at all, none of the 2015 surveillance videos (S36 says
so over the static TV), no re-enactment of violence; every jail interior is an empty Blender
reconstruction, never AI. His death is said once (S43), on black, with a help line and no music
change or effect; S37 stays on black too. The accuser and the friend are not named or shown.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import edit as E  # noqa: E402
import ep01 as E1  # noqa: E402  (shared helpers: stacked words, end card, overlays)
import ep02 as E2  # noqa: E402  (shared helpers: dated rows, big words, lower thirds)
import ep04 as E4  # noqa: E402  (shared helpers: number, bars)
import footage as F  # noqa: E402
import gfx as G  # noqa: E402
import score as S  # noqa: E402

OUT_NAME = "weight_of_evidence_case08.mp4"
TITLE = "Weight of Evidence, Case 08: Kalief Browder"

SILENT = {"S09": 6.5, "S10": 3.4, "S19": 3.4, "S30": 3.4, "S41": 3.4, "S52": 3.4, "S60": 20.0}
LEAD = {"S01": 2.0, "S02": 0.6, "S11": 0.8, "S20": 0.6, "S31": 0.6, "S42": 0.6, "S43": 1.2,
        "S53": 0.6, "S59": 0.8}
PAD = {"S01": 0.8, "S02": 1.4, "S03": 1.4, "S04": 1.4, "S05": 1.6, "S06": 1.4, "S07": 1.6,
       "S08": 1.2, "S12": 1.6, "S13": 1.4, "S14": 1.6, "S15": 1.6, "S16": 1.4, "S17": 1.6, "S18": 1.8,
       "S21": 1.4, "S22": 1.6, "S24": 1.6, "S25": 1.6, "S26": 1.8, "S27": 1.8, "S28": 1.6, "S29": 1.8,
       "S32": 1.6, "S33": 1.6, "S35": 1.6, "S36": 1.8, "S37": 2.4, "S38": 1.6, "S39": 1.8, "S40": 2.0,
       "S43": 3.0, "S44": 1.6, "S45": 1.8, "S47": 1.4, "S48": 1.6, "S49": 1.6, "S50": 1.6, "S51": 1.8,
       "S55": 3.0, "S56": 3.0, "S57": 3.0, "S58": 2.0, "S59": 2.4}
FADE_IN = {"S01": 1.4, "S10": 0.6, "S19": 0.6, "S30": 0.6, "S41": 0.6, "S43": 1.0, "S52": 0.6}
FADE_OUT = {"S08": 0.4, "S09": 1.0, "S18": 1.0, "S29": 1.0, "S40": 1.2, "S43": 1.0, "S51": 1.2,
            "S58": 1.5, "S60": 1.5}
CHAPTERS = [("S01", "Rikers Island, 2010"), ("S10", "I. The arrest"), ("S19", "II. The clock"),
            ("S30", "III. The island"), ("S41", "IV. The rules"), ("S52", "V. The verdict"),
            ("S59", "Next case")]

NY = "The New Yorker, 2014"
NY2 = "The New Yorker, 2014 and 2015"
DOJ = "U.S. Attorney, S.D.N.Y., 2014"
HELP = "If you're struggling, call or text 988 (US) or find a helpline at findahelpline.com"

# Case 09 teaser card (checked in Case 09 research, section 0)
NEXT_NAME = "CAMERON TODD WILLINGHAM · 1991"
NEXT_Q = "Should a state execute someone when the evidence is disputed?"
NEXT_AT = ("Texas, 1991", "Should a state")

# honesty tag per clip (generated ai_* clips get "ILLUSTRATIVE · AI-GENERATED" from footage.py)
ILL = "ILLUSTRATIVE"
TXT = "RECONSTRUCTION · TEXT FROM "
DOJR = "RECONSTRUCTION FROM DOJ REPORT DATA"
TAGS = {"cell_push": DOJR, "cell_slot": DOJR, "cell_window": DOJR, "cell_door": DOJR,
        "tier_corridor": "RECONSTRUCTION", "tier_phone": "RECONSTRUCTION", "tier_dorm": "RECONSTRUCTION",
        "desk_cpl3030": TXT + "N.Y. CPL § 30.30", "desk_docket": "RECONSTRUCTION · WORDS AS QUOTED IN COURT",
        "desk_sdny": TXT + "THE 2014 FEDERAL FINDINGS", "desk_stack": TXT + "STACK v. BOYLE",
        "desk_salerno": TXT + "UNITED STATES v. SALERNO", "desk_bailact": TXT + "THE BAIL ACT 1976",
        "desk_dgy": TXT + "THE AER STUDY, 2018", "desk_bjs": TXT + "BJS, 2026"}
for _c in ("court_push", "court_bench", "court_witness", "court_gallery", "courtroom_push", "courtroom_bench",
           "tv_static", "desk_blank_pen", "evidence_shelf", "park_path", "room_push"):
    TAGS[_c] = ILL


# when each card lands: card_after() delays (footage plays clean first); S37 is on black
CARD_AT = {"S04": 3.0, "S12": 3.0, "S13": 2.5, "S16": 3.0, "S21": 3.0, "S22": 3.0, "S26": 3.0, "S27": 3.0,
           "S32": 3.0, "S37": 0.0, "S44": 3.0, "S45": 3.0, "S47": 3.0, "S50": 3.0}


# ---------------------------------------------------------------- one-off graphics

def date_help_shot(date, note):
    """The date of his death, held on black, a help line in small mono beneath. Nothing else."""
    def frame(t, dur):
        img = G.canvas()
        a = G.fade(t, dur, 1.0, 1.0)
        G.centered(img, G.text_layer(date, G.SANS(96, "SemiBold"), fill=G.INK, spacing=0.06), G.H // 2 - 20,
                   a * G.ease(t / 1.0))
        G.centered(img, G.text_layer(note, G.MONO(24), fill=G.DIM), G.H - 170, a * G.ease((t - 1.5) / 1.0))
        return G.finish(img, t)
    return frame


# ---------------------------------------------------------------- the graphics

def graphics(ctx):
    P = ctx.prod
    C = lambda name, **kw: E.Clip(P, name, **kw)
    at = ctx.at
    rows = E2.rows_shot
    weight = E1.scale_overlay
    lower = E2.lower
    card = G.card_shot
    num = E4.number_shot
    stack = E1.stacked_words_shot
    shots = {}

    # COLD OPEN
    shots["S01"] = E.clip_shot(C("cell_push"), tag=DOJR,
                               overlay=lower("Rikers Island, New York", "MAY 2010", 2.4))
    shots["S02"] = rows([("ACCUSED", "Robbing a man of his backpack"), ("HE SAID", "“I didn't rob anybody”"),
                         ("THE CASE", "One man's memory")],
                        [at("S02", "He was accused"), at("S02", "He said"), at("S02", "The case against")],
                        label="INFERENCE", source="Jennifer Gonnerman, " + NY)
    shots["S03"] = rows([("MAY 16, 2010", "Bail set at $3,000. His family can't pay"),
                         ("BY JUL 28, 2010", "Held without bail, for a probation violation"),
                         ("MAY 29, 2013", "Prosecutors can't proceed. Never tried")],
                        [at("S03", "For the first"), at("S03", "After that"), at("S03", "From then on")],
                        label="INFERENCE", source=NY)
    shots["S04"] = card("“If you want that, I will do that today.”", "INFERENCE",
                        "Judge Patricia DiMango, March 13, 2013 · " + NY)
    shots["S05"] = num("1,110", "DAYS HELD", "never tried · the case was dismissed",
                       "our count from The New Yorker's dates", at=at("S05", "went into Rikers"))
    shots["S06"] = num("450,700", "PEOPLE IN US JAILS NOT CONVICTED", "68% of everyone in local jails · midyear 2024",
                       "Bureau of Justice Statistics, 2026", colour=G.BRASS, at=at("S06", "In mid-2024"))
    shots["S07"] = E.clip_shot(C("scale_empty"), tag=None)
    shots["S08"] = G.words_shot("We'll give you a verdict, and tell you how sure we are.", size=64,
                                emphasis={"how", "sure"}, per_word=0.3, start=at("S08", "At the end"))
    shots["S09"] = G.title_shot("KALIEF BROWDER", "Should anyone be jailed for years before a trial?",
                                "WEIGHT OF EVIDENCE · CASE 08")

    # I. THE ARREST
    shots["S10"] = G.title_shot("I · THE ARREST")
    shots["S11"] = rows([("FAMILY", "Youngest of seven; his mother also fostered dozens of children"),
                         ("2010", "A high school sophomore in the Bronx"),
                         ("MAY 15, 2010", "Ten days before his seventeenth birthday")],
                        [at("S11", "the youngest"), at("S11", "In the spring"), at("S11", "Most of what")],
                        label="INFERENCE", source=NY)
    shots["S12"] = card("“I didn't rob anybody … You can check my pockets.”", "INFERENCE",
                        "Kalief Browder, as he recalled the stop, " + NY)
    shots["S13"] = card("“…which insured that he wouldn't have a criminal record.”", "INFERENCE",
                        "On his earlier case, " + NY)
    shots["S14"] = rows([("THE COMPLAINT", "Chased him, pushed him against a fence, took his backpack"),
                         ("CHARGED", "Robbery, grand larceny, assault"),
                         ("17 HOURS LATER", "Questioned again; says he's innocent")],
                        [at("S14", "The complaint"), at("S14", "He was charged"), at("S14", "Seventeen hours")],
                        label="INFERENCE", source=NY + ", summarizing the complaint")
    shots["S15"] = num("$3,000", "BAIL · MAY 16, 2010", "out of reach for his family", NY, colour=G.BRASS,
                       at=at("S15", "set bail"))
    shots["S16"] = card("“…a ‘relatively straightforward case.’”", "INFERENCE",
                        "A prosecutor, in court papers · " + NY)
    shots["S17"] = rows([("JUL 28, 2010", "Indicted: robbery in the second degree. Pleads not guilty"),
                         ("BY THEN", "Held without bail, for violating probation"),
                         ("AFTER", "Bail applications fail")],
                        [at("S17", "Ten weeks later"), at("S17", "By then"), at("S17", "His lawyer asked")],
                        label="INFERENCE", source=NY)
    shots["S18"] = E.clip_shot(C("scale_tip_left"), tag=None,
                               overlay=weight("EVIDENCE · ONE MAN'S ACCOUNT, BAIL HE COULDN'T PAY, THEN NO BAIL AT ALL"))

    # II. THE CLOCK
    shots["S19"] = G.title_shot("II · THE CLOCK")
    shots["S20"] = E.clip_shot(C("courtroom_push"), tag=ILL,
                               overlay=lower("The Bronx, New York", "2010–2013", 1.2))
    shots["S21"] = card("“…where the people are not ready for trial within: (a) six months of the commencement of a "
                        "criminal action…”", "RECORD", "N.Y. Criminal Procedure Law § 30.30(1)(a)")
    shots["S22"] = card("“The People are not ready. We are requesting one week.”", "INFERENCE",
                        "A prosecutor in court, Jan 28, 2011 · " + NY)
    shots["S23"] = rows([("", "Prosecutor on trial"), ("", "On jury duty"), ("", "“Conflicts in my schedule”"),
                         ("", "“The assigned assistant is currently on vacation”")],
                        [at("S23", "the prosecutor was"), at("S23", "or on jury"), at("S23", "scheduling conflict"),
                         at("S23", "on vacation")],
                        header="THE REASONS GIVEN IN COURT", label="INFERENCE", source=NY)
    t_law = at("S24", "A lawsuit")
    shots["S24"] = G.seq((F.delay(card("“These long delays … they're horrendous, but the D.A. is not really "
                                       "accountable for that kind of delay.”", "INFERENCE",
                                       "Robert Johnson, Bronx District Attorney · " + NY),
                                  at("S24", "The Bronx district")), t_law),
                         (card("Prosecutors said they were ready “when in fact, they never were.”", "INFERENCE",
                               "The lawsuit filed for Browder · " + NY), 1))
    t_om = at("S25", "His lawyer")
    shots["S25"] = G.seq((rows([("EARLY 2012", "Plead guilty: 3½ years in prison"), ("IF CONVICTED", "Up to 15 years"),
                                ("FALL 2012", "Plead guilty: 2½ years")],
                               [at("S25", "In early 2012"), at("S25", "against up to"), at("S25", "Later that year")],
                               label="INFERENCE", source=NY), t_om),
                         (card("“Ninety-nine out of a hundred would take the offer that gets you out of jail.”",
                               "INFERENCE", "Brendan O'Meara, his lawyer, 2014"), 1))
    t_he = at("S26", "He said: I'm")
    shots["S26"] = G.seq((card("“If you want that, I will do that today.”", "INFERENCE",
                               "Judge DiMango, March 13, 2013, court transcript · " + NY), t_he),
                         (card("“I'm all right … I did not do it. I'm all right.”", "INFERENCE",
                               "Kalief Browder, the same day, as quoted in " + NY), 1))
    t_rel = at("S27", "Browder was released")
    shots["S27"] = G.seq((card("“The District Attorney is really in a position right now where they cannot "
                               "proceed.”", "INFERENCE", "Judge DiMango, May 29, 2013, as quoted in " + NY), t_rel),
                         (num("1,110", "DAYS HELD", "never tried", "our count from The New Yorker's dates", at=0.4), 1))
    shots["S28"] = num("75 DAYS", "AVERAGE STAY · ADOLESCENTS ON RIKERS, FY2013", "his: about fifteen times as long",
                       DOJ, colour=G.BRASS, at=at("S28", "about seventy-five"))
    shots["S29"] = E.clip_shot(C("scale_tip_right"), tag=None,
                               overlay=weight("EVIDENCE · A SIX-MONTH RULE, AND THREE YEARS OF ‘NOT READY’"))

    # III. THE ISLAND
    shots["S30"] = G.title_shot("III · THE ISLAND")
    shots["S31"] = rows([("400 ACRES", "An island in the East River"), ("10", "Jails"),
                         ("~600", "Boys in the adolescent jail when he arrived")],
                        [at("S31", "four hundred acres"), at("S31", "ten jails"), at("S31", "some six hundred")],
                        label="INFERENCE", source=NY)
    shots["S32"] = card("“…a deep-seated culture of violence is pervasive throughout the adolescent facilities.”",
                        "RECORD", "U.S. Attorney, Southern District of New York, Aug 4, 2014")
    shots["S33"] = num("43.7%", "SUBJECTED TO FORCE BY STAFF",
                       "of 705 adolescent boys in custody, Oct 30, 2012 · at least once", DOJ,
                       at=at("S33", "forty-four percent"))
    shots["S34"] = E.clip_shot(C("cell_slot"), tag=DOJR,
                               overlay=lower("PUNITIVE SEGREGATION", "6 × 8 FT · 23 HOURS A DAY", 1.2))
    shots["S35"] = num("ABOUT 2 YEARS", "IN SOLITARY", "his own estimate: ‘seven hundred, eight hundred’ days · "
                       "no official count", NY2, colour=G.BRASS, label="INFERENCE", at=at("S35", "about two years"))
    shots["S36"] = rows([("IN THE CELL", "Handcuffed and searched whenever he left"),
                         ("CALLS", "One, six minutes a day"), ("FOOD", "Through a slot; often hungry")],
                        [at("S36", "handcuffed"), at("S36", "one six-minute"), at("S36", "about being hungry")],
                        label="INFERENCE", source="Kalief Browder, to " + NY)
    shots["S37"] = card("“I'm not all right. I'm messed up … I'm mentally scarred right now.”", "INFERENCE",
                        "Kalief Browder, 2014")
    shots["S38"] = rows([("MAY 30, 2013", "Walks out; a bus and two subways home"),
                         ("MISSED", "Junior year, senior year, graduation, the prom")],
                        [at("S38", "he walked out"), at("S38", "He had missed")], label="INFERENCE", source=NY)
    shots["S39"] = rows([("MAR 2014", "Passes his high school equivalency exam, first try"),
                         ("FALL 2014", "Starts at Bronx Community College"),
                         ("SEPT 2014", "Tells his story in The New Yorker")],
                        [at("S39", "He passed"), at("S39", "and started at"), at("S39", "In 2014 he decided")],
                        label="INFERENCE", source=NY2)
    shots["S40"] = E.clip_shot(C("scale_tip_right", start=2), tag=None,
                               overlay=weight("EVIDENCE · A VIOLENT JAIL FOR BOYS, AND ABOUT TWO YEARS IN SOLITARY"))

    # IV. THE RULES
    shots["S41"] = G.title_shot("IV · THE RULES")
    shots["S42"] = rows([("SEPT 2014", "His story is published"), ("DEC 2014", "NYC ends solitary for adolescents"),
                         ("JAN 13, 2015", "Board of Correction votes to end it for everyone 21 and under")],
                        [at("S42", "His story"), at("S42", "That December"), at("S42", "In January 2015")],
                        label="RECORD", source="NYC Department of Correction, Jan 13, 2015")
    shots["S43"] = date_help_shot("JUNE 6, 2015", HELP)
    shots["S44"] = card("“Unless this right to bail before trial is preserved, the presumption of innocence, secured "
                        "only after centuries of struggle, would lose its meaning.”", "RECORD",
                        "Chief Justice Vinson, Stack v. Boyle, U.S. Supreme Court, 1951")
    t_mar = at("S45", "Justice Marshall")
    shots["S45"] = G.seq((card("“In our society liberty is the norm, and detention prior to trial or without trial is "
                               "the carefully limited exception.”", "RECORD",
                               "Chief Justice Rehnquist, United States v. Salerno, 1987"), t_mar),
                         (card("“…the shortcuts we take with those whom we believe to be guilty injure only those "
                               "wrongfully accused and, ultimately, ourselves.”", "RECORD",
                               "Justice Marshall, dissenting, Salerno, 1987"), 1))
    shots["S46"] = rows([("2018", "No one under 18 held on Rikers"),
                         ("2019", "Cash bail ended for most misdemeanors and nonviolent felonies"),
                         ("2019", "“Ready” for trial requires handing over the evidence"),
                         ("2020–22", "Judges regain bail for more charges, including felonies while on "
                                         "probation")],
                        [at("S46", "From 2018"), at("S46", "In 2019"), at("S46", "and said prosecutors"),
                         at("S46", "Since then")], label="RECORD",
                        source="NYC Mayor's Office, 2018 · Data Collaborative for Justice, 2023 · CPL §§ 30.30, 510.10")
    shots["S47"] = card("“New York continues to be the only state in the country where judges cannot consider "
                        "community safety in setting bail.”", "ARGUMENT",
                        "Judge Jeffrey Zimmerman, Bronx Criminal Court, July 2023")
    shots["S48"] = num("+13 POINTS", "CHANCE OF CONVICTION IF HELD", "felony defendants · nearly a million New York "
                       "City cases", "Leslie & Pope, Journal of Law & Economics, 2017 · Dobbie, Goldin & Yang, AER, "
                       "2018", at=at("S48", "thirteen percentage"))
    t44 = at("S49", "forty-four percent")
    t_not = at("S49", "But not everyone")
    shots["S49"] = G.seq((E4.bars_shot("RE-ARRESTED WITHIN 2 YEARS · NEW YORK CITY",
                                       [("After bail was eliminated", 44, G.BRASS, t44 + 0.6),
                                        ("Before", 50, G.DIM, t44 + 1.4)],
                                       "Data Collaborative for Justice, 2023 (New York City)"), t_not),
                         (card("Release “tended to increase recidivism for people with more substantial recent "
                               "criminal histories.”", "RECORD", "Data Collaborative for Justice, 2023"), 1))
    t_clk = at("S50", "And England's clock")
    shots["S50"] = G.seq((card("“A person to whom this section applies shall be granted bail except as provided in "
                               "Schedule 1.”", "RECORD", "Bail Act 1976, s. 4 (England and Wales)"), t_clk),
                         (rows([("HELD ONLY IF", "Substantial grounds he'd run, offend, or interfere with witnesses "
                                                 "(among other exceptions)"),
                                ("THE CLOCK", "182 days in custody before a Crown Court trial, unless a court "
                                              "extends it")],
                               [0.3, 1.0], label="RECORD",
                               source="Bail Act 1976 · Custody Time Limits Regulations 1987, reg. 5"), 1))
    shots["S51"] = E.clip_shot(C("scale_tip_left"), tag=None,
                               overlay=weight("EVIDENCE · THE LAW SAYS EXCEPTION. TWO IN THREE IN JAIL ARE UNCONVICTED"))

    # V. THE VERDICT
    shots["S52"] = G.title_shot("V · THE VERDICT")
    shots["S53"] = E.clip_shot(C("scale_tip_left"), tag=None,
                               overlay=weight("THE STRONGEST CASE: SOME PEOPLE SHOULD WAIT INSIDE"))
    shots["S54"] = E.clip_shot(C("scale_tip_right"), tag=None,
                               overlay=weight("THE STRONGEST CASE: INNOCENT UNTIL PROVEN GUILTY"))
    shots["S55"] = G.verdict_shot("No one should wait years in jail for a trial. Time held before trial should have a "
                                  "hard limit, counted in days, that only a judge can extend, for a stated reason.", 85,
                                  "Evidence that hard limits mostly free people who go on to seriously hurt someone, "
                                  "or rush trials until they're unfair.",
                                  meter_at=at("S55", "Our confidence"), change_at=at("S55", "What would change"),
                                  kicker="THE CLOCK")
    shots["S56"] = G.verdict_shot("No one should be held because they can't pay. If someone is too dangerous or too "
                                  "likely to run, a judge should hold them openly, after a hearing, for that reason.", 80,
                                  "Evidence that hearing-based systems end up holding the same poor defendants, for as "
                                  "long as money bail did.",
                                  meter_at=at("S56", "Our confidence"), change_at=at("S56", "What would change"),
                                  kicker="MONEY BAIL")
    shots["S57"] = G.verdict_shot("He should never have spent three years on Rikers. Money put him there. An automatic "
                                  "probation hold and a clock that never ran out kept him there.", 85,
                                  "The sealed court file showing most of the delay came from his own side, or evidence "
                                  "beyond one man's account that the case against him was strong.",
                                  meter_at=at("S57", "Our confidence"), change_at=at("S57", "What would change"),
                                  kicker="KALIEF BROWDER")
    shots["S58"] = E.clip_shot(C("scale_level_loaded", start=4), tag=None, fout=1.5)
    shots["S59"] = stack([("NEXT CASE", G.MONO(30, True), G.RED),
                          (NEXT_NAME, G.SANS(58, "SemiBold"), G.INK),
                          (NEXT_Q, G.SERIF_I(46), G.DIM)],
                         [0.3, at("S59", NEXT_AT[0]), at("S59", NEXT_AT[1])])
    shots["S60"] = E1.endcard_shot(note="If you're struggling: call or text 988 (US) · findahelpline.com")
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

    def card_after(sid, d, *items):
        """A card shot whose card lands d seconds in, over footage that plays clean until then."""
        return F.over(Bq(*items), F.delay(old[sid], d), clear_until=d)

    lower = E2.lower
    weight = E1.scale_overlay

    # ------------------------------------------------------------ COLD OPEN
    c1, c2 = at("S01", "He will wait"), at("S01", "The trial will")
    shots["S01"] = B(("cell_push", c1), ("ai_bridge", c2 - c1 + 1.0), "cell_window",
                     overlay=lower("Rikers Island, New York", "MAY 2010", 2.4))
    c1 = at("S02", "He was accused")
    shots["S02"] = under("S02", ("ai_bronx_night", c1 + 4), "ai_lights", clear=c1)
    c1, c2 = at("S03", "For the first"), at("S03", "After that")
    shots["S03"] = under("S03", ("ai_court_ext", c2), ("court_bench", 6), "cell_door", clear=c1)
    shots["S04"] = card_after("S04", CARD_AT["S04"], ("court_witness", 6), "court_gallery")
    c1, c2 = at("S05", "Then the case"), at("S05", "went into Rikers")
    shots["S05"] = under("S05", ("ai_island", c1 + 5), ("cell_door", c2 - c1 - 5, 1.0), "tier_corridor",
                         clear=c2)
    c1 = at("S06", "In mid-2024")
    shots["S06"] = under("S06", ("ai_razor_wire", c1), ("tier_dorm", None), clear=c1)
    q = [at("S08", p) for p in ("the federal investigation", "the Supreme Court's", "New York's bail",
                                "and how England", "At the end")]
    shots["S08"] = G.seq((B(("ai_archive", q[0]), ("desk_sdny", q[1] - q[0]), ("ai_scotus", q[2] - q[1]),
                            ("desk_cpl3030", q[3] - q[2]), "ai_westminster"), q[4]), (old["S08"], 1))

    # ------------------------------------------------------------ I. THE ARREST
    c1, c2, c3 = at("S11", "the youngest"), at("S11", "Most of what"), at("S11", "His court file")
    shots["S11"] = under("S11", ("ai_bronx_night", c2), ("ai_papers", c3 - c2), "ai_archive", clear=c1)
    shots["S12"] = card_after("S12", CARD_AT["S12"], ("ai_lights", 6), ("ai_bronx_night", None, 1.0))
    shots["S13"] = card_after("S13", CARD_AT["S13"], ("desk_blank_pen", 6), "evidence_shelf")
    c1, c2, c3 = at("S14", "The complaint"), at("S14", "He was charged"), at("S14", "Seventeen hours")
    shots["S14"] = under("S14", ("ai_papers", c2), ("desk_blank_pen", c3 - c2), "room_push", clear=c1)
    c1 = at("S15", "set bail")
    shots["S15"] = under("S15", ("court_bench", c1), ("ai_bridge", None), clear=c1)
    shots["S16"] = card_after("S16", CARD_AT["S16"], ("ai_papers", 6), "evidence_shelf")
    c1, c2 = at("S17", "Ten weeks later"), at("S17", "By then")
    shots["S17"] = under("S17", ("ai_court_ext", c2), ("court_push", 6), ("desk_blank_pen", 5), "cell_door",
                         clear=c1)

    # ------------------------------------------------------------ II. THE CLOCK
    shots["S20"] = B(("ai_court_ext", 5), ("courtroom_push", 7), ("ai_court_corridor", 5), "court_gallery",
                     overlay=lower("The Bronx, New York", "2010–2013", 1.2))
    shots["S21"] = card_after("S21", CARD_AT["S21"], ("ai_clock", 6), "desk_cpl3030")
    shots["S22"] = card_after("S22", CARD_AT["S22"], ("ai_court_corridor", 6), "desk_docket")
    c1 = at("S23", "the prosecutor was")
    shots["S23"] = under("S23", ("ai_clock", c1 + 3), ("court_bench", 6), ("ai_court_corridor", 5), "court_gallery",
                         clear=c1)
    c1, c2 = at("S24", "The Bronx district"), at("S24", "A lawsuit")
    shots["S24"] = under("S24", ("ai_court_ext", c2), ("ai_papers", 6), "ai_archive", clear=c1)
    c1 = at("S25", "In early 2012")
    shots["S25"] = under("S25", ("court_witness", c1 + 5), ("desk_blank_pen", 6), "court_gallery", clear=c1)
    shots["S26"] = card_after("S26", CARD_AT["S26"], ("court_bench", 8), ("court_witness", 8), "courtroom_bench")
    shots["S27"] = card_after("S27", CARD_AT["S27"], ("court_push", 8), ("ai_bridge", 5), "cell_door")
    c1 = at("S28", "about seventy-five")
    shots["S28"] = under("S28", ("tier_dorm", c1 + 4), "tier_corridor", clear=c1)

    # ------------------------------------------------------------ III. THE ISLAND
    c1 = at("S31", "four hundred acres")
    shots["S31"] = under("S31", ("ai_island", c1 + 5), ("ai_razor_wire", 5), "tier_corridor", clear=c1)
    shots["S32"] = card_after("S32", CARD_AT["S32"], ("tier_corridor", 6), "desk_sdny")
    c1 = at("S33", "forty-four percent")
    shots["S33"] = under("S33", ("tier_dorm", c1 + 3), ("tier_corridor", None, 3.0), clear=c1)
    c1 = at("S34", "On any given")
    shots["S34"] = B(("cell_slot", c1), ("cell_window", 7), "cell_push",
                     overlay=lower("PUNITIVE SEGREGATION", "6 × 8 FT · 23 HOURS A DAY", 1.2))
    c1 = at("S35", "about two years")
    shots["S35"] = under("S35", ("cell_window", c1), ("cell_door", None), clear=c1)
    c1, c2, c3, c4 = (at("S36", p) for p in ("handcuffed", "one six-minute", "about being hungry", "In 2015"))
    shots["S36"] = under("S36", ("cell_door", c2), ("tier_phone", c3 - c2), ("cell_slot", c4 - c3), "tv_static",
                         clear=c1)
    # S37 stays on black (care: no picture under the self-harm line)
    c1, c2 = at("S38", "he walked out"), at("S38", "He had missed")
    shots["S38"] = under("S38", ("ai_bridge", c1 + 4), ("ai_subway", None), clear=c2)
    c1, c2 = at("S39", "He passed"), at("S39", "In 2014 he decided")
    shots["S39"] = under("S39", ("ai_classroom", c2), ("ai_papers", 6), "ai_rain_window", clear=c1)

    # ------------------------------------------------------------ IV. THE RULES
    c1 = at("S42", "His story")
    shots["S42"] = under("S42", ("ai_papers", c1 + 4), ("cell_door", 6), "ai_skyline", clear=c1)
    # S43 stays on black: the date and the help line only
    shots["S44"] = card_after("S44", CARD_AT["S44"], ("ai_scotus", 6), "desk_stack")
    shots["S45"] = card_after("S45", CARD_AT["S45"], ("ai_scotus", 5), ("desk_salerno", 9), ("court_bench", None, 2.0))
    c1 = at("S46", "From 2018")
    shots["S46"] = under("S46", ("ai_skyline", c1 + 4), ("tier_dorm", 5), ("ai_court_ext", 5), "desk_blank_pen",
                         clear=c1)
    shots["S47"] = card_after("S47", CARD_AT["S47"], ("court_bench", 7), "ai_court_corridor")
    c1 = at("S48", "thirteen percentage")
    shots["S48"] = under("S48", ("desk_dgy", c1 + 3), ("ai_philly", 5), "court_witness", clear=c1)
    c1 = at("S49", "forty-four percent")
    shots["S49"] = under("S49", ("ai_skyline", c1), ("ai_lights", 6), "ai_papers", clear=c1)
    shots["S50"] = card_after("S50", CARD_AT["S50"], ("ai_westminster", 5), ("desk_bailact", 9), ("ai_london", 5), "ai_clock")

    # ------------------------------------------------------------ V. THE VERDICT: the two strongest cases
    q = [at("S53", p) for p in ("Some people charged", "The Supreme Court allows", "While someone is held",
                                "And Browder's case", "What failed")]
    shots["S53"] = B(("scale_tip_left", q[0]), ("ai_lights", q[1] - q[0]), ("ai_scotus", q[2] - q[1]),
                     ("tier_corridor", q[3] - q[2]), ("desk_docket", q[4] - q[3]), ("ai_clock", 5),
                     ("scale_tip_left", None, 3.0),
                     overlay=weight("THE STRONGEST CASE: SOME PEOPLE SHOULD WAIT INSIDE"))
    q = [at("S54", p) for p in ("A person who hasn't", "Money bail doesn't", "Being held makes",
                                "Where New York City", "And for a sixteen-year-old", "If someone is truly")]
    shots["S54"] = B(("scale_tip_right", q[0]), ("desk_stack", q[1] - q[0]), ("ai_court_ext", q[2] - q[1]),
                     ("desk_dgy", q[3] - q[2]), ("ai_skyline", q[4] - q[3]), ("cell_push", q[5] - q[4]),
                     ("court_bench", 6), ("scale_tip_right", None, 3.0),
                     overlay=weight("THE STRONGEST CASE: INNOCENT UNTIL PROVEN GUILTY"))
    return shots


# ---------------------------------------------------------------- sound

def music(ctx):
    return [("S01", "S09", S.cue_open, 2), ("S10", "S18", S.cue_tower, -1), ("S19", "S29", S.cue_law, -1),
            ("S30", "S40", S.cue_patient, -1), ("S41", "S51", S.cue_science, -2), ("S52", "S60", S.cue_verdict, 0)]


def sfx(ctx):
    at = ctx.at
    ev = [("S01", 0.0, S.hum(ctx.dur["S01"], vol=0.025), -18), ("S34", 0.0, S.hum(ctx.dur["S34"], vol=0.02), -20),
          ("S09", 0.2, S.hit(), -3), ("S05", at("S05", "went into Rikers"), S.hit(0.5), -10),
          ("S06", at("S06", "In mid-2024"), S.hit(0.4), -12)]
    for sid, d in CARD_AT.items():
        ev.append((sid, d, S.card_drop(), -10))
    ev.append(("S24", at("S24", "The Bronx district"), S.card_drop(), -10))
    for sid, ph in (("S24", "A lawsuit"), ("S25", "His lawyer"), ("S26", "He said: I'm"), ("S27", "Browder was released"),
                    ("S45", "Justice Marshall"), ("S49", "But not everyone"), ("S50", "And England's clock")):
        ev.append((sid, at(sid, ph), S.card_drop(), -10))
    for sid in ("S18", "S29", "S40", "S51", "S53", "S54"):
        ev.append((sid, 0.3, S.clink(), -11))
    for sid in ("S55", "S56", "S57"):
        ev.append((sid, at(sid, "Our confidence"), S.whoosh(1.4), -12))
    for sid in ("S10", "S19", "S30", "S41", "S52"):
        ev.append((sid, 0.1, S.whoosh(1.6), -10))
    return ev


if __name__ == "__main__":
    E.main(sys.modules[__name__])
