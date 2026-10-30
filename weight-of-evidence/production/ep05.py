"""Weight of Evidence, Case 05: The Golden State Killer. Shot definitions for edit.py.

    python ep05.py <prod_dir> --stills | --only S02,S13 | --final -j 2

Shot ids, picture notes and research IDs are in episodes/05-the-golden-state-killer/script.md.
Care rules (research §F): the thirteen murdered are named once each; nothing about any attack is
shown or described; the perpetrator's name is said once and never shown, and there is no image of
him; no relative whose DNA was matched is named or hinted at, and the family tree is an
illustration with blank nodes; no re-created company web pages.
"""

import os
import sys

from PIL import ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import edit as E  # noqa: E402
import ep01 as E1  # noqa: E402  (shared helpers: stacked words, end card, overlays)
import ep02 as E2  # noqa: E402  (shared helpers: dated rows, big words, lower thirds)
import ep04 as E4  # noqa: E402  (shared helpers: number, bars, footnote, lines)
import gfx as G  # noqa: E402
import score as S  # noqa: E402

OUT_NAME = "weight_of_evidence_case05.mp4"
TITLE = "Weight of Evidence, Case 05: The Golden State Killer"

SILENT = {"S09": 6.5, "S10": 3.4, "S19": 3.4, "S30": 3.4, "S38": 3.4, "S46": 3.4, "S54": 20.0}
LEAD = {"S01": 2.0, "S02": 0.6, "S05": 0.8, "S11": 0.6, "S20": 0.6, "S31": 0.6, "S39": 0.6,
        "S47": 0.6, "S53": 0.8}
PAD = {"S01": 0.8, "S02": 1.2, "S03": 1.2, "S04": 2.0, "S05": 1.6, "S06": 1.4, "S07": 1.6,
       "S08": 1.2, "S13": 2.4, "S14": 2.0, "S15": 1.6, "S18": 1.8, "S21": 1.4, "S24": 1.2,
       "S26": 1.4, "S27": 1.2, "S29": 1.8, "S33": 1.0, "S35": 1.6, "S37": 2.0, "S39": 1.2,
       "S43": 1.2, "S45": 1.8, "S49": 3.0, "S50": 3.0, "S51": 3.0, "S52": 2.0, "S53": 2.4}
FADE_IN = {"S01": 1.4, "S10": 0.6, "S19": 0.6, "S30": 0.6, "S38": 0.6, "S46": 0.6}
FADE_OUT = {"S05": 0.8, "S08": 0.4, "S09": 1.0, "S18": 1.0, "S29": 1.0, "S37": 1.2, "S45": 1.2,
            "S52": 1.5, "S54": 1.5}
CHAPTERS = [("S01", "Roseville, 2018"), ("S10", "I. The cold case"), ("S19", "II. The family tree"),
            ("S30", "III. The reach"), ("S38", "IV. The rules"), ("S46", "V. The verdict"),
            ("S53", "Next case")]

COURT = "People v. DeAngelo, Sacramento Superior Court No. 18FE008017"
DAS = "Joint release of six California district attorneys, 2020"
LAT = "LA Times, Dec 2020"
ERLICH = "Erlich, Shor, Pe'er & Carmi, Science 2018"

VICTIMS = [("Claude Snelling", "VISALIA · 1975", "Claude Snelling"),
           ("Katie Maggiore", "RANCHO CORDOVA · 1978", "Katie and"),
           ("Brian Maggiore", "RANCHO CORDOVA · 1978", "Katie and"),
           ("Debra Alexandria Manning", "GOLETA · 1979", "Alexandria Manning"),
           ("Robert Offerman", "GOLETA · 1979", "Robert Offerman"),
           ("Charlene Smith", "VENTURA · 1980", "Charlene and"),
           ("Lyman Smith", "VENTURA · 1980", "Charlene and"),
           ("Keith Harrington", "DANA POINT · 1980", "Keith and Patrice"),
           ("Patrice Harrington", "DANA POINT · 1980", "Keith and Patrice"),
           ("Manuela Witthuhn", "IRVINE · 1981", "Manuela"),
           ("Cheri Domingo", "GOLETA · 1981", "Domingo"),
           ("Gregory Sanchez", "GOLETA · 1981", "Gregory Sanchez"),
           ("Janelle Cruz", "IRVINE · 1986", "Janelle Cruz")]


# ---------------------------------------------------------------- graphics

def strike_shot(ctx, sid):
    """'NOT A POLICE DATABASE' is struck through in red; 'A FAMILY TREE' lands beneath."""
    t_strike = ctx.at(sid, "He wasn't found", end=True)
    t_tree = ctx.at(sid, "He was found through")
    top = G.text_layer("NOT A POLICE DATABASE", G.SANS(64, "SemiBold"), fill=G.DIM, spacing=0.06)
    low = G.text_layer("A FAMILY TREE", G.SANS(84, "SemiBold"), fill=G.BRASS, spacing=0.06)

    def frame(t, dur):
        img = G.canvas()
        a = G.fade(t, dur, 0.4, 0.5)
        y = G.H // 2 - 110
        G.centered(img, top, y, a)
        k = G.ease((t - t_strike) / 0.5)
        if k > 0:
            x0 = (G.W - top.width) // 2
            d = ImageDraw.Draw(img)
            d.line([x0 - 10, y + top.height // 2 + 4, x0 - 10 + (top.width + 20) * k, y + top.height // 2 + 4],
                   fill=tuple(int(c * a) for c in G.RED), width=6)
        G.centered(img, low, G.H // 2 + 40, a * G.ease((t - t_tree) / 0.6))
        return G.finish(img, t)
    return frame


def names_shot(ctx, sid):
    """The thirteen murdered, in two columns, each landing as it is said. No photos."""
    times = [ctx.at(sid, ph) for _, _, ph in VICTIMS]

    def frame(t, dur):
        img = G.canvas()
        a = G.fade(t, dur, 0.4, 0.6)
        for i, ((name, place, _), ts) in enumerate(zip(VICTIMS, times)):
            k = G.ease((t - ts) / 0.5) * a
            if k <= 0:
                continue
            col, row = (0, i) if i < 7 else (1, i - 7)
            x, y = 200 + col * 820, 200 + row * 100
            G.paste_alpha(img, G.text_layer(name, G.SANS(38, "SemiBold"), fill=G.INK), (x, y), k)
            G.paste_alpha(img, G.text_layer(place, G.MONO(22, True), fill=G.BRASS, spacing=0.12), (x, y + 50), k)
        G.paste_alpha(img, G.text_layer(COURT, G.MONO(22), fill=G.FAINT), (200, G.H - 120), a)
        st = G.stamp("RECORD", 20)
        G.paste_alpha(img, st, (G.W - 200 - st.width, 110), a)
        return G.finish(img, t)
    return frame


def tree_shot(ctx, sid):
    """An illustration of how genealogists work: two matches climb to shared ancestors, the
    descendants fan out, and most grey out until six remain, then one. Blank nodes only."""
    t_up = 0.6
    t_down = ctx.at(sid, "then worked forward")
    t_six = ctx.at(sid, "six men fit")
    t_one = ctx.at(sid, "One had blue")
    W, H = G.W, G.H
    anc = [(W // 2 - 60, 200), (W // 2 + 60, 200)]
    chains = [[(560, 380), (440, 560), (320, 760)], [(1360, 380), (1480, 560), (1600, 760)]]  # down to each match
    kids = [(W // 2 - 170, 380), (W // 2 + 170, 380)]
    leaves = [(W // 2 - 315 + i * 90, 600) for i in range(8)]
    six = {0, 2, 3, 4, 6, 7}
    pick = 3

    def node(d, xy, r, col, a):
        x, y = xy
        d.ellipse([x - r, y - r, x + r, y + r], outline=tuple(int(c * a) for c in col), width=4)

    def frame(t, dur):
        img = G.canvas()
        a = G.fade(t, dur, 0.4, 0.5)
        d = ImageDraw.Draw(img)
        line = lambda p, q, col, k: d.line([p, q], fill=tuple(int(c * k) for c in col), width=3)
        ku = G.ease((t - t_up) / 1.4) * a
        for ch, top in zip(chains, anc):  # each match climbs its own line to the shared couple
            pts = [top] + ch
            for i in range(len(pts) - 1):
                line(pts[i], pts[i + 1], G.BRASS, ku * 0.8)
            for q in ch[:-1]:
                node(d, q, 16, G.BRASS, ku)
            node(d, ch[-1], 22, G.BRASS, a)
        line(anc[0], anc[1], G.BRASS, ku)
        for p in anc:
            node(d, p, 22, G.BRASS, ku)
        kd = G.ease((t - t_down) / 1.5) * a
        mid = (W // 2, 200)
        for c in kids:
            if kd > 0:
                line(mid, c, G.DIM, kd)
                node(d, c, 18, G.DIM, kd)
        for i, lf in enumerate(leaves):
            if kd <= 0:
                continue
            parent = kids[0] if i < 4 else kids[1]
            keep = 1.0
            if t > t_six and i not in six:
                keep = 1.0 - 0.75 * G.ease((t - t_six) / 0.8)
            if t > t_one and i != pick:
                keep = min(keep, 1.0 - 0.6 * G.ease((t - t_one) / 0.8))
            col = G.INK if (t > t_one and i == pick) else G.DIM
            line(parent, lf, G.FAINT, kd * keep)
            node(d, lf, 16, col, kd * keep)
        for (x, y) in (chains[0][-1], chains[1][-1]):
            lay = G.text_layer("MATCH", G.MONO(22, True), fill=G.BRASS, spacing=0.2)
            G.paste_alpha(img, lay, (x - lay.width // 2, y + 40), a)
        G.recon_tag(img, a, "ILLUSTRATION · NOT DATA")
        return G.finish(img, t)
    return frame


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
    shots["S01"] = E.clip_shot(C("lot_push"), overlay=lower("Roseville, California", "APRIL 18, 2018", 2.4))
    shots["S02"] = big("MATCH", 120, colour=G.BRASS, sub="DNA from a double murder · Ventura County · 1980",
                       sub_at=at("S02", "double murder"))
    shots["S03"] = strike_shot(ctx, "S03")
    shots["S04"] = card("The relatives whose DNA led to him were never asked, and most have never been named.",
                        "INFERENCE", LAT + " · AP, 2018")
    shots["S05"] = num("13", "MURDERED", "between 1975 and 1986, and dozens more attacked", DAS,
                       at=at("S05", "he murdered"))
    shots["S06"] = num("1,182", "CASES CLEARED BY GENETIC GENEALOGY",
                       "to February 2024 · one researcher's count", "T. L. Dowdeswell, 2024",
                       colour=G.BRASS, label=None, at=at("S06", "well over"))
    shots["S07"] = E.clip_shot(C("scale_empty"), tag=None)
    shots["S08"] = G.words_shot("We'll give you a verdict, and tell you how sure we are.", size=64,
                                emphasis={"how", "sure"}, per_word=0.3, start=at("S08", "At the end"))
    shots["S09"] = G.title_shot("THE GOLDEN STATE KILLER", "Should police search your family's DNA?",
                                "WEIGHT OF EVIDENCE · CASE 05")

    # I. THE COLD CASE
    shots["S10"] = G.title_shot("I · THE COLD CASE")
    shots["S11"] = rows([("1974–75", "Visalia"), ("1976–79", "Sacramento · East Bay"),
                         ("1979–86", "Santa Barbara · Ventura · Orange County")],
                        [0.4, at("S11", "moved north"), at("S11", "then south")],
                        label="RECORD", source="Sentencing memorandum, " + COURT)
    shots["S12"] = stack([("VISALIA RANSACKER", G.MONO(34, True), G.DIM),
                          ("EAST AREA RAPIST", G.MONO(34, True), G.DIM),
                          ("ORIGINAL NIGHT STALKER", G.MONO(34, True), G.DIM),
                          ("GOLDEN STATE KILLER", G.SANS(64, "SemiBold"), G.INK)],
                         [at("S12", "Ransacker", offset=-0.6), at("S12", "East Area"), at("S12", "Original Night"),
                          at("S12", "came later")])
    shots["S13"] = names_shot(ctx, "S13")
    t_sis = at("S14", "Her sister")
    shots["S14"] = G.seq((card("“…never made it to their first wedding anniversary.”", "RECORD",
                               "Orange County DA Todd Spitzer, Aug 21, 2020"), t_sis),
                         (card("“Janelle was my big sister. She was one year older than me.”", "RECORD",
                               "Michelle Cruz, victim-impact statement, Aug 2020"), 1))
    shots["S15"] = num("87", "VICTIMS", "on 53 occasions, in 11 counties · charged and uncharged, as admitted",
                       "People's Sentencing Memorandum, Aug 2020", at=at("S15", "prosecutors counted", end=True))
    shots["S16"] = big("CODIS · 12 MILLION+ PROFILES (2018)", 60, sub="it can only match someone already in it",
                       sub_at=at("S16", "But it can only"))
    shots["S17"] = card("In 2004, Keith Harrington's brother Bruce sponsored, and largely paid for, Proposition 69, "
                        "adding every felony arrestee in California to the state's DNA database.",
                        "INFERENCE", "California voter guide, 2004 · press")
    shots["S18"] = E.clip_shot(C("scale_tip_left"), tag=None,
                               overlay=weight("EVIDENCE · THIRTEEN DEAD, AND THE DATABASE COULDN'T FIND HIM"))

    # II. THE FAMILY TREE
    shots["S19"] = G.title_shot("II · THE FAMILY TREE")
    shots["S20"] = E.clip_shot(C("evidence_shelf"), overlay=lower("Contra Costa and Ventura counties", "2017", 1.2))
    shots["S21"] = card("March 2017: a judge ordered a DNA sample from a 73-year-old man in an Oregon nursing home. "
                        "He was not the killer.", "INFERENCE", "AP, Apr 30, 2018")
    shots["S22"] = rows([("FAMILYTREEDNA", "A made-up account, with the company's help"),
                         ("GEDMATCH", "A free site, never asked"),
                         ("MYHERITAGE", "A personal account; company not told")],
                        [at("S22", "let them search"), at("S22", "didn't know"), at("S22", "on her own account")],
                        label="INFERENCE", source=LAT + " · AP, 2018")
    shots["S23"] = card("Which site gave the decisive matches is disputed: GEDmatch, in 2018 accounts; "
                        "MyHeritage, in a 2020 LA Times investigation.", "INFERENCE", LAT + " · AP, 2018")
    shots["S24"] = tree_shot(ctx, "S24")
    shots["S25"] = E.clip_shot(C("lot_wide"))
    shots["S26"] = rows([("APR 18, 2018", "Door handle swabbed"), ("APR 23", "Tissue taken from his trash"),
                         ("APR 24", "Arrested at home")],
                        [0.4, 0.9, at("S26", "was arrested")],
                        label="RECORD", source="Unsealed warrants, via BuzzFeed News and AP, June 2018")
    shots["S27"] = rows([("JUNE 29, 2020", "Pleads guilty: 13 murders, 13 kidnappings"),
                         ("AUG 21, 2020", "11 consecutive life terms without parole")],
                        [at("S27", "he pleaded guilty"), at("S27", "He was sentenced")],
                        label="RECORD", source=DAS)
    shots["S28"] = card("“…perpetuates a fraudulent impression.”", "INFERENCE",
                        "Cheryl Temple, Ventura County prosecutor, Jan 2019 · via LA Times")
    shots["S29"] = E.clip_shot(C("scale_tip_right"), tag=None,
                               overlay=weight("EVIDENCE · IT WORKED, AND NO ONE WHOSE DNA MADE IT WORK WAS ASKED"))

    # III. THE REACH
    shots["S30"] = G.title_shot("III · THE REACH")
    t_24 = at("S31", "By early")
    shots["S31"] = G.seq((num("13", "CASES SOLVED", "April–August 2018", ERLICH, label=None, at=at("S31", "at least")), t_24),
                         (num("1,182", "CASES CLEARED", "to February 2024", "T. L. Dowdeswell, 2024", colour=G.BRASS,
                              label=None, at=0.4), 1))
    t_2 = at("S32", "A database covering")
    shots["S32"] = G.seq((num("60%", "OF SEARCHES FOR PEOPLE OF EUROPEAN DESCENT", "find a third cousin or closer",
                              ERLICH, colour=G.BRASS, at=at("S32", "they estimated", end=True)), t_2),
                         (num("2%", "OF A POPULATION IN THE DATABASE", "is enough to reach nearly anyone in it",
                              ERLICH, colour=G.BRASS, at=0.4), 1))
    t_pol = at("S33", "Police DNA databases")
    shots["S33"] = G.seq((num("30%", "MORE LIKELY TO HAVE A CLOSE MATCH",
                              "people of Northern European background, compared with sub-Saharan African background",
                              ERLICH, at=at("S33", "Northern European")), t_pol),
                         (card("Genealogy databases “might thus begin to redress” the racial skew of police DNA databases.",
                               "ARGUMENT", "Ram, Guerrini & McGuire, Science 2018"), 1))
    shots["S34"] = rows([("2018", "Police allowed: murder and rape"), ("NOV 2018", "An exception for an assault in Utah"),
                         ("MAY 2019", "Users must opt in"), ("JULY 2019", "A Florida warrant searches everyone"),
                         ("2019 · 2023", "Sold, then sold again")],
                        [at("S34", "changed its terms"), at("S34", "made an exception"), at("S34", "had to opt in"),
                         at("S34", "a judge in Florida"), at("S34", "Then the site")],
                        header="GEDMATCH", label="INFERENCE",
                        source="Salt Lake Tribune 2019 · NBC 2019 · NYT via Science News 2019 · QIAGEN 2023")
    shots["S35"] = card("“…a huge game changer… It's a signal that no genetic information can be safe.”",
                        "INFERENCE", "Erin Murphy, NYU School of Law, 2019 (as quoted in the New York Times)")
    shots["S36"] = rows([("23ANDME", "“Resists” police requests; none produced"),
                         ("2023", "14,000 accounts breached; 6.9M profiles exposed"),
                         ("2025", "Bankrupt, and sold with its data")],
                        [at("S36", "says it has never"), at("S36", "In 2023"), at("S36", "In 2025")],
                        label="INFERENCE", source="23andMe transparency report, 2026 · SEC filing, 2023 · AP, 2025")
    shots["S37"] = E.clip_shot(C("scale_tip_right", start=2), tag=None,
                               overlay=weight("EVIDENCE · YOU CAN BE FOUND WITHOUT EVER TAKING A TEST"))

    # IV. THE RULES
    shots["S38"] = G.title_shot("IV · THE RULES")
    shots["S39"] = rows([("1996", "Angie Dodge murdered, Idaho Falls"), ("1998", "Christopher Tapp convicted"),
                         ("2014", "A family search points to Michael Usry"),
                         ("2019", "The real killer found; Tapp exonerated")],
                        [at("S39", "In 1996"), at("S39", "Christopher Tapp"), at("S39", "In 2014"), at("S39", "In 2019")],
                        label="RECORD", source="National Registry of Exonerations · EFF, 2015")
    shots["S40"] = rows([("2008", "California: familial searches of its database"),
                         ("2010", "The Grim Sleeper, found through his son"), ("MARYLAND", "Bans them")],
                        [at("S40", "Since 2008"), at("S40", "That's how police"), at("S40", "Maryland bans")],
                        label="RECORD", source="California Attorney General, 2008, 2010 · Maryland v. King, 2013")
    shots["S41"] = rows([("1", "Homicides and sex crimes"), ("2", "The police database first"),
                         ("3", "Investigators identify themselves"), ("4", "Only sites that warn their users"),
                         ("5", "No arrest on a genetic link alone")],
                        [at("S41", "mainly for"), at("S41", "only after"), at("S41", "must identify"),
                         at("S41", "may only use"), at("S41", "No one may")],
                        header="U.S. JUSTICE DEPARTMENT · 2019", label="RECORD",
                        source="U.S. DOJ Interim Policy, effective Nov 1, 2019")
    shots["S42"] = rows([("MD · 2021", "A judge approves each search; relatives can refuse"),
                         ("MT · 2021", "A warrant or a court order"),
                         ("UT · 2023", "Violent felonies and missing persons only")],
                        [at("S42", "Maryland"), at("S42", "Montana"), at("S42", "Utah")],
                        label="RECORD", source="Md. Laws 2021 ch. 681 · Mont. Code § 44-6-104 · Utah S.B. 156")
    t_sc = at("S43", "The Supreme Court")
    shots["S43"] = G.seq((card("“There is no privacy interest in commonly held DNA that a relative voluntarily uploads "
                               "to a public database.”", "RECORD", "State v. Hartman, Washington Court of Appeals, 2023"), t_sc),
                         (rows([("1988", "California v. Greenwood · trash needs no warrant"),
                                ("2018", "Carpenter v. United States · phone location does")],
                               [at("S43", "Its closest", offset=-t_sc), at("S43", "taking his trash", offset=-t_sc)],
                               header="THE U.S. SUPREME COURT", label="RECORD"), 1))
    shots["S44"] = E4.bars_shot("PUBLIC SUPPORT FOR POLICE USE · MAY 2018 SURVEY",
                                [("Violent crimes", 80, G.BRASS, at("S44", "supported police")),
                                 ("Nonviolent crimes", 39, G.DIM, at("S44", "For nonviolent"))],
                                "Guerrini et al., PLoS Biology 2018 · online survey")
    shots["S45"] = E.clip_shot(C("scale_tip_left"), tag=None,
                               overlay=weight("EVIDENCE · EVERY RULE DRAWS THE SAME THREE LINES"))

    # V. THE VERDICT
    shots["S46"] = G.title_shot("V · THE VERDICT")
    shots["S47"] = E.clip_shot(C("scale_tip_left"), tag=None, overlay=weight("THE STRONGEST CASE: LET THEM SEARCH"))
    shots["S48"] = E.clip_shot(C("scale_tip_right"), tag=None, overlay=weight("THE STRONGEST CASE: NOT WITHOUT YOUR CONSENT"))
    shots["S49"] = G.verdict_shot("Catching him this way was right. Doing it in secret, on sites that hadn't warned "
                                  "their users, was not.", 80,
                                  "Evidence that being open about the search at the time would have let him escape.",
                                  meter_at=at("S49", "Our confidence"), change_at=at("S49", "What would change"),
                                  kicker="THE GOLDEN STATE KILLER")
    shots["S50"] = G.verdict_shot("Yes, but only for murder and rape, with a judge's approval each time, on sites "
                                  "that ask their users first.", 75,
                                  "Evidence that limits like these don't hold: that searches still spread to lesser "
                                  "crimes, or keep falling on innocent relatives.",
                                  meter_at=at("S50", "Our confidence"), change_at=at("S50", "What would change"),
                                  kicker="THE POLICE")
    t_v3 = at("S51", "no one can", offset=-1.2)
    shots["S51"] = G.seq((E4.lines_shot(["When one person shares their DNA,", "who consents for the family?"],
                                        [0.4, at("S51", "who consents")]), t_v3),
                         (G.verdict_shot("No one can fully consent for a family, so the limits should be set by law, "
                                         "not by whoever owns the database.", 70,
                                         "Evidence that company rules have held steadier, and protected people better, "
                                         "than the laws written to replace them.",
                                         meter_at=at("S51", "Our confidence") - t_v3,
                                         change_at=at("S51", "What would change") - t_v3,
                                         kicker="THE BIGGER QUESTION"), 1))
    shots["S52"] = E.clip_shot(C("scale_level_loaded", start=4), tag=None, fout=1.5)
    shots["S53"] = stack([("NEXT CASE", G.MONO(30, True), G.RED),
                          ("THE CENTRAL PARK FIVE · 1989", G.SANS(58, "SemiBold"), G.INK),
                          ("Should police be allowed to lie to suspects?", G.SERIF_I(46), G.DIM)],
                         [0.3, at("S53", "five teenagers"), at("S53", "Should police")])
    shots["S54"] = E1.endcard_shot()
    return shots


# ---------------------------------------------------------------- sound

def music(ctx):
    return [("S01", "S09", S.cue_open, 2), ("S10", "S18", S.cue_patient, 0), ("S19", "S29", S.cue_science, -2),
            ("S30", "S37", S.cue_tower, -1), ("S38", "S45", S.cue_law, -1), ("S46", "S54", S.cue_verdict, 0)]


def sfx(ctx):
    at = ctx.at
    ev = [("S01", 0.0, S.hum(ctx.dur["S01"], vol=0.025), -18), ("S20", 0.0, S.hum(ctx.dur["S20"]), -18),
          ("S25", 0.0, S.hum(ctx.dur["S25"], vol=0.025), -20),
          ("S09", 0.2, S.hit(), -3), ("S05", 0.4, S.hit(0.5), -10), ("S02", 0.3, S.hit(0.4), -12)]
    for sid in ("S04", "S14", "S17", "S21", "S23", "S28", "S35", "S43"):
        ev.append((sid, 0.0, S.card_drop(), -10))
    ev.append(("S14", at("S14", "Her sister"), S.card_drop(), -10))
    ev.append(("S33", at("S33", "Police DNA databases"), S.card_drop(), -10))
    ev.append(("S03", at("S03", "He wasn't found", end=True), S.marker(0.5, vol=0.2), -12))
    for sid in ("S18", "S29", "S37", "S45", "S47", "S48"):
        ev.append((sid, 0.3, S.clink(), -11))
    for sid in ("S49", "S50", "S51"):
        ev.append((sid, at(sid, "Our confidence"), S.whoosh(1.4), -12))
    for sid in ("S10", "S19", "S30", "S38", "S46"):
        ev.append((sid, 0.1, S.whoosh(1.6), -10))
    return ev


if __name__ == "__main__":
    E.main(sys.modules[__name__])
