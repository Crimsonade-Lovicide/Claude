"""Weight of Evidence, Case 04: The Pernkopf Atlas. Shot definitions for edit.py.

    python ep04.py <prod_dir> --stills | --only S02,S13 | --final -j 2

Shot ids, picture notes and research IDs are in episodes/04-the-pernkopf-atlas/script.md.
Care rules (research §F): no plate is ever shown, not even cropped or blurred, and no
signature; the atlas appears only as a closed, untitled book (3D) or as its title in type. No
execution imagery. No name is ever put next to the atlas. Pernkopf gets no photograph.
"""

import os
import sys

from PIL import ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import edit as E  # noqa: E402
import ep01 as E1  # noqa: E402  (shared helpers: stacked words, end card, overlays, span)
import ep02 as E2  # noqa: E402  (shared helpers: dated rows, big words, lower thirds)
import gfx as G  # noqa: E402
import score as S  # noqa: E402

OUT_NAME = "weight_of_evidence_case04.mp4"
TITLE = "Weight of Evidence, Case 04: The Pernkopf Atlas"

SILENT = {"S09": 6.5, "S10": 3.4, "S17": 3.4, "S24": 3.4, "S34": 3.4, "S45": 3.4, "S53": 20.0}
LEAD = {"S01": 2.0, "S02": 0.6, "S05": 0.8, "S11": 0.6, "S18": 0.6, "S25": 0.6, "S35": 0.6,
        "S46": 0.6, "S52": 0.8}
PAD = {"S01": 0.8, "S03": 1.2, "S04": 2.0, "S05": 2.4, "S06": 1.6, "S07": 1.6, "S08": 1.2,
       "S16": 1.8, "S19": 1.6, "S22": 1.6, "S23": 1.8, "S28": 1.4, "S30": 1.0, "S31": 1.2,
       "S32": 1.4, "S33": 2.4, "S40": 1.4, "S41": 1.2, "S43": 1.2, "S44": 1.8, "S48": 3.0,
       "S49": 3.0, "S50": 3.0, "S51": 2.0, "S52": 2.4}
FADE_IN = {"S01": 1.4, "S10": 0.6, "S17": 0.6, "S24": 0.6, "S34": 0.6, "S45": 0.6}
FADE_OUT = {"S05": 0.8, "S08": 0.4, "S09": 1.0, "S16": 1.0, "S23": 1.0, "S33": 1.2, "S44": 1.2,
            "S51": 1.5, "S53": 1.5}
CHAPTERS = [("S01", "St. Louis, 2014"), ("S10", "I. The atlas"), ("S17", "II. The dean"),
            ("S24", "III. The bodies"), ("S34", "IV. The operating room"), ("S45", "V. The verdict"),
            ("S52", "Next case")]

SENATE = "Senate Project, University of Vienna, 1998 (via Angetter, Lancet 2000)"
MEDUNI = "Czech, Druml, Weninger, Müller · Medical University of Vienna · J Biocommun 2021"
POLAK = "Rabbi Joseph A. Polak, the Vienna Protocol, November 22, 2017"


# ---------------------------------------------------------------- graphics

def number_shot(num, above, below, source, colour=G.INK, label="RECORD", at=0.4):
    """One number, set large, with a mono line above and a plain-language line below."""
    def frame(t, dur):
        img = G.canvas()
        a = G.fade(t, dur, 0.4, 0.5)
        k = G.ease((t - at) / 0.8) * a
        G.centered(img, G.text_layer(above, G.MONO(30, True), fill=G.DIM, spacing=0.3), 330, a)
        G.centered(img, G.text_layer(num, G.SANS(170, "SemiBold"), fill=colour), 470, k)
        for j, ln in enumerate(G.wrap(below, G.SANS(38), 1200)):
            G.centered(img, G.text_layer(ln, G.SANS(38), fill=G.DIM), 640 + j * 52, k)
        G.paste_alpha(img, G.text_layer(source, G.MONO(22), fill=G.FAINT), (220, G.H - 140), a)
        if label:
            st = G.stamp(label, 20)
            G.paste_alpha(img, st, (G.W - 220 - st.width, 160), a)
        return G.finish(img, t)
    return frame


def bars_shot(header, bars, source):
    """Horizontal percentage bars that grow when the narrator says them: bars = [(label, pct, colour, t)]."""
    def frame(t, dur):
        img = G.canvas()
        a = G.fade(t, dur, 0.4, 0.4)
        d = ImageDraw.Draw(img)
        x0, full = 260, 1180
        gap = 190 if len(bars) <= 3 else 150
        G.paste_alpha(img, G.text_layer(header, G.MONO(26, True), fill=G.DIM, spacing=0.2), (x0, 210), a)
        for i, (lab, v, c, ts) in enumerate(bars):
            y = 360 + i * gap
            k = G.ease((t - ts) / 1.2) * a
            G.paste_alpha(img, G.text_layer(lab, G.SANS(34), fill=G.INK), (x0, y - 56), a * G.ease((t - ts) / 0.4))
            d.rectangle([x0, y, x0 + full, y + 50], fill=tuple(int(cc * a) for cc in (18, 20, 24)))
            if k > 0:
                d.rectangle([x0, y, x0 + full * v / 100 * k, y + 50], fill=tuple(int(cc * a) for cc in c))
                G.paste_alpha(img, G.text_layer(f"{v * k:.0f}%", G.SANS(44, "SemiBold"), fill=G.INK),
                              (x0 + full * v / 100 * k + 24, y - 2), k)
        G.paste_alpha(img, G.text_layer(source, G.MONO(22), fill=G.FAINT), (x0, G.H - 140), a)
        st = G.stamp("RECORD", 20)
        G.paste_alpha(img, st, (G.W - 220 - st.width, 160), a)
        return G.finish(img, t)
    return frame


def footnote(shot, text, at):
    """A small mono line under a card, e.g. to say whose ruling it is."""
    def frame(t, dur):
        img = shot(t, dur)
        G.centered(img, G.text_layer(text, G.MONO(24), fill=G.DIM), G.H - 110,
                   G.ramp(t, at, 0.6) * G.fade(t, dur, 0.01, 0.35))
        return img
    return frame


def lines_shot(lines, times):
    """Two or three lines of serif type for a question put on screen."""
    def frame(t, dur):
        img = G.canvas()
        a = G.fade(t, dur, 0.4, 0.5)
        for i, (ln, ts) in enumerate(zip(lines, times)):
            G.centered(img, G.text_layer(ln, G.SERIF(60), fill=G.INK), 440 + i * 90, a * G.ease((t - ts) / 0.6))
        return G.finish(img, t)
    return frame


# ---------------------------------------------------------------- the shots

def build(ctx):
    P = ctx.prod
    C = lambda name, **kw: E.Clip(P, name, **kw)
    at = ctx.at
    doc = G.document_shot
    rows = E2.rows_shot
    big = E2.big_words
    stack = E1.stacked_words_shot
    cap = E1.caption_overlay
    weight = E1.scale_overlay
    lower = E2.lower
    card = G.card_shot
    shots = {}

    # COLD OPEN
    shots["S01"] = E.clip_shot(C("or_lamp"), overlay=lower("St. Louis, Missouri", "2014", 2.4))
    shots["S02"] = big("ONE PAGE", 110, colour=G.BRASS, sub="from an atlas printed in 1963",
                       sub_at=at("S02", "an old anatomy atlas"))
    shots["S03"] = big("TOPOGRAPHISCHE ANATOMIE DES MENSCHEN", 60, sub="Vienna · 1937–1960",
                       sub_at=at("S03", "between"))
    shots["S04"] = number_shot("1,377", "AT LEAST",
                               "people executed by the Nazi regime whose bodies went to his institute, 1938–1945",
                               "University of Vienna, Senate Project, 1998", at=at("S04", "at least"))
    shots["S05"] = stack([("NO ONE IN ANY PAINTING", G.SANS(64, "SemiBold"), G.INK),
                          ("HAS EVER BEEN IDENTIFIED", G.SANS(64, "SemiBold"), G.INK)],
                         [at("S05", "No one in any"), at("S05", "has ever been")])
    shots["S06"] = card("The patient was not told at the time that the atlas had been used.",
                        "INFERENCE", "STAT, May 30, 2019")
    shots["S07"] = E.clip_shot(C("scale_empty"), tag=None)
    shots["S08"] = G.words_shot("We'll give you a verdict, and tell you how sure we are.", size=64,
                                emphasis={"how", "sure"}, per_word=0.3, start=at("S08", "At the end"))
    shots["S09"] = G.title_shot("THE PERNKOPF ATLAS", "Should surgeons use it?", "WEIGHT OF EVIDENCE · CASE 04")

    # I. THE ATLAS
    shots["S10"] = G.title_shot("I · THE ATLAS")
    shots["S11"] = E.clip_shot(C("book_closed"), overlay=cap("VIENNA · 1933", at("S11", "full professor")))
    shots["S12"] = rows([("", "Erich Lepier"), ("", "Ludwig Schrott"), ("", "Karl Endtresser"), ("", "Franz Batke")],
                        [at("S12", "painters"), at("S12", "Ludwig"), at("S12", "Entresser", offset=-0.6),
                         at("S12", "Entresser", offset=0.6)],
                        header="THE PAINTERS", source="D. J. Williams, J Biomed Commun 1988")
    shots["S13"] = rows([("1937", "Volume 1"), ("1941", "Volume 2"), ("1952", "Volume 3"), ("1957–60", "Volume 4")],
                        [at("S13", "The first volume"), at("S13", "The first volume", offset=0.7),
                         at("S13", "The first volume", offset=1.4), at("S13", "The last")],
                        header="TOPOGRAPHISCHE ANATOMIE DES MENSCHEN", label="RECORD",
                        source="Deutsche Nationalbibliothek · Williams 1988 · Czech et al. 2021")
    shots["S14"] = card("“…the standard by which all other illustrated anatomic works are measured.”",
                        "ARGUMENT", "D. J. Williams, J Biomed Commun, 1988")
    shots["S15"] = card("“…undisputed that Lepier repeatedly included a swastika in his signature.”",
                        "RECORD", SENATE)
    shots["S16"] = E.clip_shot(C("scale_tip_left"), tag=None, overlay=weight("EVIDENCE · A GREAT BOOK, SIGNED WITH A SWASTIKA"))

    # II. THE DEAN
    shots["S17"] = G.title_shot("II · THE DEAN")
    shots["S18"] = E.clip_shot(C("corridor"), overlay=lower("Vienna", "MARCH 1938", 1.2))
    address = ["…die Ausschaltung der Erbminderwertigen,", "durch Sterilisation und andere Mittel.", "",
               "…the exclusion of the hereditarily inferior,", "by sterilisation and other means."]
    shots["S19"] = doc(address, header="E. PERNKOPF · ADDRESS AS DEAN · APRIL 1938", size=42, width=1300,
                       highlight=E1.span(address, "the exclusion of the hereditarily inferior,"),
                       hi_at=at("S19", "the exclusion"),
                       footer="Wien Klin Wochenschr 1938;51:545 · excerpt recreated, with translation")
    shots["S20"] = number_shot("153 OF 197", "TEACHERS DISMISSED",
                               "from the medical faculty, 1938 · the most cited count",
                               "E. Ernst, Ann Intern Med 1995", at=at("S20", "The most cited"))
    shots["S21"] = rows([("1943", "Rector of the university"), ("1945", "Removed from every post"),
                         ("1945–47", "Interned near Salzburg")],
                        [at("S21", "In 1943"), at("S21", "When the war ended"), at("S21", "the American army")],
                        label="RECORD", source="University of Vienna, 650 plus · Angetter, Lancet 2000")
    shots["S22"] = E.clip_shot(C("book_night"))
    shots["S23"] = E.clip_shot(C("scale_tip_right"), tag=None, overlay=weight("EVIDENCE · THE MAN WHO MADE IT RAN A NAZI FACULTY"))

    # III. THE BODIES
    shots["S24"] = G.title_shot("III · THE BODIES")
    shots["S25"] = rows([("1985", "First questions in print"), ("1994", "Howard Israel · William Seidelman"),
                         ("MAR 1995", "Yad Vashem writes to Vienna"), ("1996", "Israel and Seidelman in JAMA")],
                        [at("S25", "In the 1980s"), at("S25", "In 1994"), at("S25", "In March"),
                         at("S25", "asking for an inquiry")],
                        label="RECORD", source="Hildebrandt 2006 · Seidelman 2012 · JAMA 1996;276:1633")
    shots["S26"] = big("SENATE PROJECT · UNIVERSITY OF VIENNA", 60, sub="1997–1998", sub_at=at("S26", "set up a commission"))
    shots["S27"] = card("“…the true number of executed citizens must be higher than 1377.”", "RECORD", SENATE)
    shots["S28"] = rows([("", "Resistance"), ("", "“High treason”"), ("", "Black-marketeering"), ("", "Pickpocketing"),
                         ("", "Listening to enemy broadcasts")],
                        [at("S28", "More than half"), at("S28", "high treason"), at("S28", "Others were put"),
                         at("S28", "for pickpocketing"), at("S28", "for listening")],
                        header="CONVICTED OF", label="RECORD", source=SENATE)
    shots["S29"] = big("NO EVIDENCE OF BODIES FROM THE CAMPS", 60, sub="Mauthausen · Gusen",
                       sub_at=at("S29", "concentration camps"))
    t_41 = at("S30", "For those")
    shots["S30"] = G.seq((number_shot("41 OF 791", "PAINTINGS", "signed with dates from 1938 to 1945",
                                      SENATE, at=at("S30", "The commission counted")), t_41),
                         (card("“…it must be assumed that the models probably came from the group of 1377.”",
                               "RECORD", SENATE), 1))
    shots["S31"] = G.seq((card("“…can neither be confirmed nor negated.”", "RECORD", SENATE), at("S31", "In 2021")),
                         (card("“…a considerable number of the paintings produced during and after the war are based on the bodies of these victims.”",
                               "RECORD", "Medical University of Vienna, 2021 (“it is to be assumed”) · J Biocommun"), 1))
    t_reg = at("S32", "own register")
    shots["S32"] = G.seq((stack([("98 SPECIMENS", G.SANS(72, "SemiBold"), G.INK),
                                 ("labelled as from the court · removed for burial", G.SERIF_I(44), G.DIM)],
                                [0.6, at("S32", "They were taken")]), t_reg),
                         (stack([("2019", G.MONO(32, True), G.BRASS),
                                 ("THE INSTITUTE'S BODY REGISTERS ARE FOUND", G.SANS(52, "SemiBold"), G.INK),
                                 ("war-years entries not yet published", G.SERIF_I(44), G.DIM)],
                                [at("S32", "In 2019", offset=-t_reg), at("S32", "turned up", offset=-t_reg),
                                 at("S32", "The entries", offset=-t_reg)]), 1))
    shots["S33"] = E.clip_shot(C("scale_tip_right", start=2), tag=None, overlay=weight("EVIDENCE · SOME OF THEM ARE PROBABLY IN ITS PAGES"))

    # IV. THE OPERATING ROOM
    shots["S34"] = G.title_shot("IV · THE OPERATING ROOM")
    shots["S35"] = rows([("1963–64", "English edition"), ("1989", "Third edition"), ("MID-1990s", "Printing stops"),
                         ("2019", "Originals given to Vienna")],
                        [0.4, 0.9, at("S35", "the publisher stopped"), at("S35", "In 2019")],
                        label="RECORD", source="Czech et al., J Biocommun 2021 · Elsevier donation, 2019")
    shots["S36"] = bars_shot("STILL IN USE",
                             [("Nerve surgeons, 2019 · know it", 59, G.DIM, at("S36", "more than half")),
                              ("Nerve surgeons, 2019 · use it", 13, G.BRASS, at("S36", "were using")),
                              ("Oral and facial surgeons, 2021 · know it", 49, G.DIM, at("S36", "Among oral")),
                              ("Oral and facial surgeons, 2021 · use it", 9, G.BRASS, at("S36", "Among oral", offset=1.6))],
                             "Yee et al., Neurosurgery 2019 · Yee et al., Ann Anat 2021")
    shots["S37"] = number_shot("69%", "NERVE SURGEONS · 2019", "still comfortable using it, once told its history",
                               "Yee et al., Neurosurgery 2019", colour=G.BRASS, at=at("S37", "history"))
    shots["S38"] = bars_shot("MEDICAL STUDENTS · ONE US SCHOOL · 2017",
                             [("Had never heard of it", 95, G.DIM, at("S38", "of the students")),
                              ("Found it more complete and accurate", 71, G.INK, at("S38", "most found")),
                              ("Found a modern atlas more useful for learning", 76, G.BRASS, at("S38", "said the modern"))],
                             "Coombs & Peitzman, Ann Anat 2017")
    shots["S39"] = card("“…their use would certainly be permitted by most authorities to help save lives (piku'ah nefesh)…”",
                        "RECORD", POLAK)
    shots["S40"] = footnote(card("“…making it known to one and all just exactly what these drawings are. In this way, the dead are accorded at least some of the dignity to which they are entitled.”",
                                 "RECORD", "Rabbi Joseph A. Polak, the Vienna Protocol, 2017"),
                            "a rabbinic ruling, first presented at a Yad Vashem symposium; not a ruling of Yad Vashem",
                            at("S40", "His ruling"))
    t_obj = at("S41", "But when it really")
    t_hild = at("S41", "Not everyone agrees")
    shots["S41"] = G.seq((card("“…far from irreplaceable.”", "RECORD", MEDUNI), t_obj),
                         (card("“…nobody will reasonably object to such an ultima ratio.”", "RECORD", MEDUNI), t_hild - t_obj),
                         (rows([("2006", "With its history: “not only justifiable but desirable”"),
                                ("2019", "No longer uses it in her own lectures")],
                               [at("S41", "once argued", offset=-t_hild), at("S41", "By 2019", offset=-t_hild)],
                               header="SABINE HILDEBRANDT · HISTORIAN OF ANATOMY", label="ARGUMENT",
                               source="Hildebrandt, Clin Anat 2006 · STAT, May 30, 2019"), 1))
    shots["S42"] = rows([("1", "Stop and think"), ("2", "Call a colleague"), ("3", "Try another atlas"),
                         ("4", "Only then, Pernkopf")],
                        [at("S42", "stop and think"), at("S42", "call a colleague"), at("S42", "try another"),
                         at("S42", "Only then")],
                        header="MACKINNON'S STEPS", label="RECORD", source="Mackinnon & Yee, J Biocommun 2021")
    shots["S43"] = stack([("SOBOTTA · CLEMENTE · SPALTEHOLZ", G.MONO(36, True), G.DIM),
                          ("DACHAU · 1942", G.MONO(36, True), G.DIM)],
                         [at("S43", "Some of its images"), at("S43", "freezing experiments")])
    shots["S44"] = E.clip_shot(C("scale_tip_left"), tag=None, overlay=weight("EVIDENCE · THE LINE IS DRAWN AT A LIFE"))

    # V. THE VERDICT
    shots["S45"] = G.title_shot("V · THE VERDICT")
    shots["S46"] = E.clip_shot(C("scale_tip_left"), tag=None, overlay=weight("THE STRONGEST CASE: USE IT"))
    shots["S47"] = E.clip_shot(C("scale_tip_right"), tag=None, overlay=weight("THE STRONGEST CASE: LEAVE IT ON THE SHELF"))
    shots["S48"] = G.verdict_shot("Use it as a last resort, when it can save a life or end real suffering, and tell the patient where it came from.", 80,
                                  "Evidence that other atlases or modern imaging now match it in the cases where surgeons still reach for it.",
                                  meter_at=at("S48", "Our confidence"), change_at=at("S48", "What would change"),
                                  kicker="IN THE OPERATING ROOM")
    shots["S49"] = G.verdict_shot("Don't teach anatomy from it. Teach its history instead.", 75,
                                  "Evidence that students taught from it, with its history, become more careful doctors, not less.",
                                  meter_at=at("S49", "Our confidence"), change_at=at("S49", "What would change"),
                                  kicker="IN THE CLASSROOM")
    t_v3 = at("S50", "verdict we may", offset=-0.3)
    shots["S50"] = G.seq((lines_shot(["May we use knowledge taken from people", "who were killed and never agreed?"],
                                     [0.4, at("S50", "who were killed")]), t_v3),
                         (G.verdict_shot("Knowledge taken from people a regime killed may be used to save a life, but never in silence.", 70,
                                         "If the people in it could be named, and their families asked that it not be used.",
                                         meter_at=at("S50", "Our confidence") - t_v3, change_at=at("S50", "What would change") - t_v3,
                                         kicker="THE BIGGER QUESTION"), 1))
    shots["S51"] = E.clip_shot(C("scale_level_loaded", start=4), tag=None, fout=1.5)
    shots["S52"] = stack([("NEXT CASE", G.MONO(30, True), G.RED),
                          ("THE GOLDEN STATE KILLER · 2018", G.SANS(58, "SemiBold"), G.INK),
                          ("Should police search your family's DNA?", G.SERIF_I(46), G.DIM)],
                         [0.3, at("S52", "a serial killer"), at("S52", "Should police")])
    shots["S53"] = E1.endcard_shot()
    return shots


# ---------------------------------------------------------------- sound

def music(ctx):
    return [("S01", "S09", S.cue_open, 2), ("S10", "S16", S.cue_science, -2), ("S17", "S23", S.cue_law, -1),
            ("S24", "S33", S.cue_patient, 0), ("S34", "S44", S.cue_tower, -1), ("S45", "S53", S.cue_verdict, 0)]


def sfx(ctx):
    at = ctx.at
    ev = [("S01", 0.0, S.hum(ctx.dur["S01"]), -16), ("S11", 0.0, S.hum(ctx.dur["S11"], vol=0.025), -20),
          ("S22", 0.0, S.hum(ctx.dur["S22"], vol=0.025), -20),
          ("S09", 0.2, S.hit(), -3), ("S05", 0.4, S.hit(0.5), -10), ("S04", at("S04", "at least"), S.hit(0.4), -12)]
    for sid in ("S06", "S14", "S15", "S27", "S31", "S39", "S40", "S41"):
        ev.append((sid, 0.0, S.card_drop(), -10))
    ev.append(("S30", at("S30", "For those"), S.card_drop(), -10))
    for sid in ("S16", "S23", "S33", "S44", "S46", "S47"):
        ev.append((sid, 0.3, S.clink(), -11))
    ev.append(("S19", at("S19", "the exclusion"), S.marker(), -14))
    for sid in ("S48", "S49", "S50"):
        ev.append((sid, at(sid, "Our confidence"), S.whoosh(1.4), -12))
    for sid in ("S10", "S17", "S24", "S34", "S45"):
        ev.append((sid, 0.1, S.whoosh(1.6), -10))
    return ev


if __name__ == "__main__":
    E.main(sys.modules[__name__])
