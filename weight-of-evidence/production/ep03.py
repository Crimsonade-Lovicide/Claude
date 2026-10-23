"""Weight of Evidence, Case 03: The Mignonette. Shot definitions for edit.py.

    python ep03.py <prod_dir> --stills | --only S02,S13 | --final -j 2

Shot ids, picture notes and research IDs are in episodes/03-the-mignonette/script.md.
Care rules (research §F): no one involved is depicted; the boat is an empty reconstruction;
the killing is described in the special verdict's words and no closer.
"""

import math
import os
import random
import sys

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import edit as E  # noqa: E402
import ep01 as E1  # noqa: E402  (shared helpers: stacked words, end card, overlays, span)
import ep02 as E2  # noqa: E402  (shared helpers: dated rows, big words, lower thirds)
import gfx as G  # noqa: E402
import score as S  # noqa: E402

OUT_NAME = "weight_of_evidence_case03.mp4"
TITLE = "Weight of Evidence, Case 03: The Mignonette"

SILENT = {"S09": 6.5, "S10": 3.4, "S20": 3.4, "S31": 3.4, "S41": 3.4, "S50": 3.4, "S58": 20.0}
LEAD = {"S01": 2.0, "S02": 0.6, "S05": 0.8, "S11": 0.6, "S21": 0.6, "S32": 0.4, "S42": 0.6,
        "S51": 0.6, "S57": 0.8}
PAD = {"S01": 0.8, "S03": 1.6, "S04": 1.4, "S05": 2.4, "S06": 1.2, "S07": 1.6, "S08": 1.2,
       "S12": 1.0, "S15": 1.0, "S17": 1.0, "S18": 1.6, "S19": 1.8, "S25": 1.0, "S29": 1.0,
       "S30": 1.8, "S35": 1.4, "S37": 1.6, "S39": 2.0, "S40": 1.8, "S44": 1.0, "S45": 1.0,
       "S48": 1.0, "S49": 1.8, "S52": 1.2, "S53": 3.0, "S54": 3.0, "S55": 3.0, "S56": 2.0,
       "S57": 2.4}
FADE_IN = {"S01": 1.4, "S10": 0.6, "S20": 0.6, "S31": 0.6, "S41": 0.6, "S50": 0.6}
FADE_OUT = {"S05": 0.8, "S08": 0.4, "S09": 1.0, "S19": 1.0, "S30": 1.0, "S40": 1.2, "S49": 1.2,
            "S56": 1.5, "S58": 1.5}
CHAPTERS = [("S01", "July 25, 1884, South Atlantic"), ("S10", "I. The boat"),
            ("S20", "II. The custom of the sea"), ("S31", "III. The judges"),
            ("S41", "IV. Who decides"), ("S50", "V. The verdict"), ("S57", "Next case")]

QBD = "R v Dudley and Stephens (1884) 14 QBD 273"
SV = "Special verdict, Exeter, November 6, 1884"
COLERIDGE = "Lord Coleridge CJ, " + QBD


# ---------------------------------------------------------------- graphics

def rain(img, t, density=220, alpha=70, seed=1884):
    """Wind-driven rain streaks over a 3D plate (night storm)."""
    rng = random.Random(seed)
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for _ in range(density):
        x0, y0 = rng.uniform(-300, G.W), rng.uniform(0, G.H)
        speed, length = rng.uniform(1400, 2200), rng.uniform(40, 110)
        y = (y0 + t * speed) % (G.H + 200) - 100
        x = (x0 + t * speed * 0.28) % (G.W + 300) - 150
        a = int(alpha * rng.uniform(0.4, 1.0))
        d.line([x, y, x + length * 0.28, y + length], fill=(190, 200, 215, a), width=2)
    img.paste(Image.alpha_composite(img.convert("RGBA"), layer).convert("RGB"))


def compare_shot(ctx, sid):
    """The custom of the sea against what happened in the Mignonette's boat."""
    t_r = ctx.at(sid, "There were no lots")
    cols = [("THE CUSTOM", G.DIM, 0.4, ["Lots drawn", "Everyone at risk", "The loser dies"]),
            ("THE MIGNONETTE", G.BRASS, t_r, ["No lots", "The boy not asked", "The weakest chosen"])]

    def frame(t, dur):
        img = G.canvas()
        a = G.fade(t, dur, 0.4, 0.5)
        d = ImageDraw.Draw(img)
        for i, (head, col, ts, lines) in enumerate(cols):
            x = 260 + i * 760
            k = G.ease((t - ts) / 0.6) * a
            d.line([x, 300, x, 700], fill=tuple(int(c * k) for c in col), width=4)
            G.paste_alpha(img, G.text_layer(head, G.MONO(32, True), fill=col, spacing=0.25), (x + 40, 300), k)
            for j, ln in enumerate(lines):
                kj = G.ease((t - ts - 0.5 - 0.5 * j) / 0.5) * a
                G.paste_alpha(img, G.text_layer(ln, G.SERIF(48), fill=G.INK), (x + 40, 410 + j * 90), kj)
        G.paste_alpha(img, G.text_layer(SV + " · U.S. v. Holmes (1842)", G.MONO(22), fill=G.FAINT), (260, G.H - 140), a)
        st = G.stamp("RECORD", 20)
        G.paste_alpha(img, st, (G.W - 220 - st.width, 160), a)
        return G.finish(img, t)
    return frame


def memorial_shot(ctx, sid):
    """Release and Dudley's death as dated rows, then the memorial inscription as text only."""
    t_mem = ctx.at(sid, "In Southampton")
    t_lord = ctx.at(sid, "Lord lay not", offset=-t_mem)
    rows = E2.rows_shot([("1885", "Released after six months"),
                         ("1900", "Dudley dies in Sydney, in a plague outbreak")],
                        [ctx.at(sid, "They were released"), ctx.at(sid, "died there")],
                        source="Home Office file HO 144/141 · Sydney press, 1900")
    words = E1.stacked_words_shot([("LORD LAY NOT THIS SIN TO THEIR CHARGE", G.SANS(54, "SemiBold"), G.INK),
                                   ("Acts 7:60", G.MONO(28), G.DIM),
                                   ("Memorial to Richard Parker · Southampton", G.MONO(26), G.DIM)],
                                  [t_lord, t_lord + 1.0, 0.6])
    return G.seq((rows, t_mem), (words, 1))


def lower(text, sub=None, at=1.2):
    return E2.lower(text, sub, at)


# ---------------------------------------------------------------- the shots

def build(ctx):
    P = ctx.prod
    C = lambda name, **kw: E.Clip(P, name, **kw)
    at = ctx.at
    doc = G.document_shot
    span = E1.span
    rows = E2.rows_shot
    big = E2.big_words
    cap = E1.caption_overlay
    weight = E1.scale_overlay
    shots = {}

    # COLD OPEN
    shots["S01"] = E.clip_shot(C("sea_dawn"), overlay=lower("South Atlantic", "JULY 25, 1884", 2.4))
    shots["S02"] = rows([("", "2 TINS OF TURNIPS"), ("", "1 SMALL TURTLE"), ("", "8 DAYS · NOTHING")],
                        [at("S02", "two tins"), at("S02", "On the fourth day"), at("S02", "For the last eight days")],
                        label="RECORD", source=SV)
    shots["S03"] = big("Richard Parker, 17", 84, sub="cabin boy", sub_at=at("S03", "the cabin boy"))
    prayer = ["…Dudley offered a prayer asking forgiveness",
              "for them all if either of them should be",
              "tempted to commit a rash act, and that",
              "their souls might be saved."]
    shots["S04"] = doc(prayer, header="SPECIAL VERDICT · EXETER, NOVEMBER 6, 1884", type_secs=4.5,
                       footer=QBD + " · excerpt recreated", size=42, width=1300)
    shots["S05"] = big("4 days", 110, colour=G.DIM)
    shots["S06"] = rows([("SEPT 1884", "They tell the authorities everything"),
                         ("DEC 1884", "Sentenced to death for murder"),
                         ("1885", "Released after six months")],
                        [at("S06", "When they reached England"), at("S06", "Three months later"), at("S06", "They served six months")],
                        source="Falmouth depositions, 1884 · " + QBD + " · HO 144/141")
    shots["S07"] = E.clip_shot(C("scale_empty"), tag=None)
    shots["S08"] = G.words_shot("We'll give you a verdict, and tell you how sure we are.", size=64,
                                emphasis={"how", "sure"}, per_word=0.3, start=at("S08", "At the end"))
    shots["S09"] = G.title_shot("THE MIGNONETTE", "Is killing to survive murder?", "WEIGHT OF EVIDENCE · CASE 03")

    # I. THE BOAT
    shots["S10"] = G.title_shot("I · THE BOAT")
    shots["S11"] = E.clip_shot(C("sea_swell", speed=0.8), overlay=cap("SOUTHAMPTON → SYDNEY · MAY 19, 1884", 1.0))
    storm = E.clip_shot(C("sea_storm"))
    shots["S12"] = lambda t, dur: storm_frame(storm, t, dur)
    title = ["THE QUEEN v. DUDLEY AND STEPHENS", "", "SPECIAL VERDICT", "",
             "Exeter Assizes", "November 6, 1884"]
    shots["S13"] = doc(title, font_fn=G.SERIF, size=46, width=1200, footer="Title recreated")
    food = ["…no supply of water and no supply of food,",
            "except two 1 lb. tins of turnips…",
            "…a small turtle…",
            "…for the next eight days they had nothing to eat…",
            "…caught in their oilskin capes…"]
    t_rain = at("S14", "When it rained")
    shots["S14"] = G.seq((doc(food, header="SPECIAL VERDICT", size=38, width=1450, font_fn=G.SERIF,
                              highlight=span(food, "two 1 lb. tins of turnips"), hi_at=at("S14", "two one pound tins"),
                              footer=QBD + " · excerpts recreated"), t_rain),
                         (doc(food, header="SPECIAL VERDICT", size=38, width=1450, font_fn=G.SERIF,
                              highlight=span(food, "caught in their oilskin capes"), hi_at=0.3,
                              footer=QBD + " · excerpts recreated", drift=0.0), 1))
    shots["S15"] = E.clip_shot(C("dinghy_close"), overlay=cap("THE EIGHTEENTH DAY", 0.8))
    shots["S16"] = G.card_shot("“…Brooks refused to consent, and it was not put to the boy, and in point of fact there was no drawing of lots.”",
                               "RECORD", SV)
    shots["S17"] = E.clip_shot(C("sea_dusk"), overlay=cap("JULY 24 · EVENING", 1.0))
    helpless = ["…the boy was lying at the bottom of the boat, quite helpless,",
                "and extremely weakened by famine and by drinking sea water,",
                "and unable to make any resistance, nor did he ever assent",
                "to his being killed."]
    shots["S18"] = doc(helpless, header="SPECIAL VERDICT", size=38, width=1500, font_fn=G.SERIF,
                       highlight=span(helpless, "nor did he ever assent"), hi_at=at("S18", "he never agreed"),
                       footer=QBD + " · excerpt recreated")
    t_w1 = at("S19", "So the first weight")
    rescue = E1.stacked_words_shot([("THE MOCTEZUMA", G.SANS(64, "SemiBold"), G.INK),
                                    ("German barque, bound for Hamburg", G.SERIF_I(46), G.DIM),
                                    ("JULY 29, 1884 · THREE MEN ALIVE", G.MONO(28, True), G.BRASS)],
                                   [0.3, at("S19", "bound for Hamburg"), at("S19", "picked them up")])
    shots["S19"] = G.seq((rescue, t_w1),
                         (E.clip_shot(C("scale_tip_left"), tag=None, overlay=weight("EVIDENCE · NO LOTS, NO CONSENT, NO GREATER NECESSITY")), 1))

    # II. THE CUSTOM OF THE SEA
    shots["S20"] = G.title_shot("II · THE CUSTOM OF THE SEA")
    shots["S21"] = G.card_shot("“Photograph of Yacht ‘Mignonettes’ Boat later at the Polytechnic Hall, Falmouth.”",
                               "RECORD", "Copyright form, September 17, 1884 · The National Archives, COPY 1/370/21")
    shots["S22"] = big("THE CUSTOM OF THE SEA", 84, colour=G.BRASS, sub="lots drawn · the loser dies · the others live",
                       sub_at=at("S22", "they drew lots"))
    shots["S23"] = G.card_shot("“…reduced to the necessity of casting lots. It fell upon Owen Coffin to die…”",
                               "RECORD", "Owen Chase, Narrative of the Shipwreck of the Whale-Ship Essex, 1821")
    shots["S24"] = G.card_shot("“…the selection is by lot. This mode is resorted to as the fairest mode, and, in some sort, as an appeal to God…”",
                               "RECORD", "Baldwin J, United States v. Holmes, 26 F. Cas. 360 (1842)")
    shots["S25"] = compare_shot(ctx, "S25")
    shots["S26"] = G.card_shot("“Stephens agreed to the act, but Brooks dissented from it.”",
                               "RECORD", SV + " · Dudley later said all three agreed")
    shots["S27"] = E.clip_shot(C("sea_swell", start=8, speed=0.8), overlay=cap("FALMOUTH · SEPTEMBER 1884", 0.8))
    shots["S28"] = G.card_shot("No one had been convicted in England for killing to survive at sea.",
                               "INFERENCE", "A.W.B. Simpson, Cannibalism and the Common Law (1984), as cited")
    shots["S29"] = G.card_shot("In Poe's 1838 novel, the man who draws the short splinter, and is killed and eaten, is named Richard Parker.",
                               "RECORD", "Edgar Allan Poe, The Narrative of Arthur Gordon Pym of Nantucket, 1838")
    shots["S30"] = E.clip_shot(C("scale_swing"), tag=None, overlay=weight("EVIDENCE · A CUSTOM THEY BELIEVED IN, AND DIDN'T FOLLOW"))

    # III. THE JUDGES
    shots["S31"] = G.title_shot("III · THE JUDGES")
    shots["S32"] = rows([("NOV 6, 1884", "Exeter · the jury returns a special verdict"),
                         ("DEC 9, 1884", "London · five judges decide")],
                        [at("S32", "The trial opened"), at("S32", "five judges")],
                        label="RECORD", source=QBD)
    report = ["(1884) 14 Q.B.D. 273", "", "THE QUEEN v. DUDLEY AND STEPHENS", "",
              "…the prisoners' act in this case was wilful murder…"]
    shots["S33"] = doc(report, font_fn=G.SERIF, size=42, width=1400, highlight=span(report, "was wilful murder"),
                       hi_at=at("S33", "The killing was"), footer="Law report · recreated")
    shots["S34"] = G.card_shot("“To preserve one's life is generally speaking a duty, but it may be the plainest and the highest duty to sacrifice it.”",
                               "RECORD", COLERIDGE)
    shots["S35"] = G.card_shot("“Who is to be the judge of this sort of necessity? By what measure is the comparative value of lives to be measured? Is it to be strength, or intellect, or what?”",
                               "RECORD", COLERIDGE)
    shots["S36"] = G.card_shot("“…the principle leaves to him who is to profit by it to determine the necessity… In this case the weakest, the youngest, the most unresisting, was chosen.”",
                               "RECORD", COLERIDGE)
    shots["S37"] = G.card_shot("“We are often compelled to set up standards we cannot reach ourselves, and to lay down rules which we could not ourselves satisfy.”",
                               "RECORD", COLERIDGE)
    shots["S38"] = G.card_shot("“SENTENCE: Death – Commuted to 6 months”", "RECORD",
                               "Home Office file HO 144/141/A36934 · The National Archives")
    shots["S39"] = memorial_shot(ctx, "S39")
    shots["S40"] = E.clip_shot(C("scale_tip_right"), tag=None, overlay=weight("EVIDENCE · NO ONE MAY DECIDE WHOSE LIFE COUNTS LESS"))

    # IV. WHO DECIDES
    shots["S41"] = G.title_shot("IV · WHO DECIDES")
    shots["S42"] = rows([("1884", "Dudley and Stephens"), ("1987", "R v Howe · not even a threat of death"),
                         ("TODAY", "No necessity defence to murder")],
                        [at("S42", "The rule still stands"), at("S42", "In 1987"), at("S42", "relied on this case")],
                        source=QBD + " · R v Howe [1987] AC 417")
    shots["S43"] = big("JODIE AND MARY · 2000", 72, colour=G.BRASS, sub="Court of Appeal · Re A (Conjoined Twins)",
                       sub_at=at("S43", "The Court of"))
    t_tests = at("S44", "He set out three tests")
    shots["S44"] = G.seq((G.card_shot("“Mary is, sadly, self-designated for a very early death.”", "RECORD",
                                      "Brooke LJ, Re A (Conjoined Twins: Surgical Separation) [2001] Fam 147"), t_tests),
                         (rows([("1", "Needed to avoid inevitable, irreparable evil"),
                                ("2", "No more than is reasonably necessary"),
                                ("3", "Not out of proportion to the evil avoided")],
                               [at("S44", "The act must be needed", offset=-t_tests), at("S44", "No more must be done", offset=-t_tests),
                                at("S44", "And the harm done", offset=-t_tests)],
                               header="BROOKE LJ'S THREE TESTS", label="RECORD", source="Re A [2001] Fam 147, after Stephen's Digest"), 1))
    shots["S45"] = G.card_shot("A young man, “petrified by cold or fear,” blocked the ladder for at least ten minutes. “He was never seen again.”",
                               "RECORD", "Zeebrugge inquest, October 1987, as recounted by Brooke LJ in Re A (2000)")
    shots["S46"] = G.card_shot("“…treated as mere objects, which denies them the value that is due to a human being for his or her own sake.”",
                               "RECORD", "Federal Constitutional Court of Germany, 1 BvR 357/05, February 15, 2006")
    shots["S47"] = G.card_shot("“…could be used to justify the taking of life to avoid a far greater loss of life… the life of every individual is assumed to be of equal value.”",
                               "RECORD", "Hawaii Revised Statutes §703-302, commentary (Model Penal Code §3.02)")
    shots["S48"] = E1.stacked_words_shot([("THE CASE OF THE SPELUNCEAN EXPLORERS", G.SANS(54, "SemiBold"), G.INK),
                                          ("Lon L. Fuller · Harvard Law Review · 1949", G.MONO(28), G.DIM),
                                          ("day 23 · the dice · rescue on day 32", G.SERIF_I(46), G.BRASS),
                                          ("The trolley problem · 1967", G.SANS(40, "SemiBold"), G.DIM)],
                                         [0.3, at("S48", "In 1949"), at("S48", "five explorers"), at("S48", "The trolley problem")])
    shots["S49"] = E.clip_shot(C("scale_bottom_left"), tag=None, overlay=weight("EVIDENCE · THE LAW BENDS ONLY WHEN NO ONE CHOOSES"))

    # V. THE VERDICT
    shots["S50"] = G.title_shot("V · THE VERDICT")
    shots["S51"] = E.clip_shot(C("scale_tip_left"), tag=None, overlay=weight("THE STRONGEST CASE: IT WASN'T MURDER"))
    shots["S52"] = E.clip_shot(C("scale_tip_right"), tag=None, overlay=weight("THE STRONGEST CASE: IT WAS MURDER"))
    shots["S53"] = G.verdict_shot("It was murder. The six-month sentence was mercy, and the mercy was right.", 85,
                                  "Evidence Parker was hours from death and beyond saving, so killing him cost him hours, not days.",
                                  meter_at=at("S53", "Our confidence"), change_at=at("S53", "What would change"),
                                  kicker="DUDLEY AND STEPHENS")
    shots["S54"] = G.verdict_shot("Coleridge was right about this boat, but “never” is too strong a rule.", 70,
                                  "Evidence that narrow exceptions like the twins case get stretched to excuse killings like this one.",
                                  meter_at=at("S54", "Our confidence"), change_at=at("S54", "What would change"),
                                  kicker="THE COURT")
    t_v3 = at("S55", "Our verdict")
    shots["S55"] = G.seq((big("Is killing to survive murder?", 72), t_v3),
                         (G.verdict_shot("Killing an innocent person to save yourself is never justified. Sometimes it can be forgiven.", 65,
                                         "A case where everyone agreed to a fair lottery in advance, and all would certainly have died without it.",
                                         meter_at=at("S55", "Our confidence") - t_v3, change_at=at("S55", "What would change") - t_v3,
                                         kicker="THE BIGGER QUESTION"), 1))
    shots["S56"] = E.clip_shot(C("scale_level_loaded", start=4), tag=None, fout=1.5)
    shots["S57"] = E1.stacked_words_shot([("NEXT CASE", G.MONO(30, True), G.RED),
                                          ("THE PERNKOPF ATLAS · VIENNA", G.SANS(58, "SemiBold"), G.INK),
                                          ("Should doctors keep using it?", G.SERIF_I(46), G.DIM)],
                                         [0.3, at("S57", "an anatomy atlas"), at("S57", "Should doctors")])
    shots["S58"] = E1.endcard_shot()
    return shots


def storm_frame(shot, t, dur):
    """The storm plate with rain laid over it (finish() has already graded the plate)."""
    img = shot(t, dur)
    rain(img, t, alpha=int(70 * G.fade(t, dur, 0.4, 0.4)))
    return img


# ---------------------------------------------------------------- sound

def music(ctx):
    return [("S01", "S09", S.cue_open, 2), ("S10", "S19", S.cue_tower, -1), ("S20", "S30", S.cue_patient, 0),
            ("S31", "S40", S.cue_law, -1), ("S41", "S49", S.cue_science, -2), ("S50", "S58", S.cue_verdict, 0)]


def sfx(ctx):
    at = ctx.at
    ev = [("S01", 0.0, S.sea(ctx.dur["S01"], 0.05), -16), ("S11", 0.0, S.sea(ctx.dur["S11"], 0.045), -18),
          ("S12", 0.0, S.sea(ctx.dur["S12"], 0.06, rough=1.0), -14), ("S15", 0.0, S.sea(ctx.dur["S15"], 0.04), -18),
          ("S17", 0.0, S.sea(ctx.dur["S17"], 0.045), -18), ("S27", 0.0, S.sea(ctx.dur["S27"], 0.035), -20),
          ("S09", 0.2, S.hit(), -3), ("S05", 0.4, S.hit(0.5), -10)]
    for sid in ("S16", "S21", "S23", "S24", "S26", "S28", "S29", "S34", "S35", "S36", "S37", "S38",
                "S44", "S45", "S46", "S47"):
        ev.append((sid, 0.0, S.card_drop(), -10))
    for sid in ("S30", "S40", "S49", "S51", "S52"):
        ev.append((sid, 0.3, S.clink(), -11))
    ev.append(("S19", at("S19", "So the first weight") + 0.3, S.clink(), -11))
    for sid, ph in (("S14", "two one pound tins"), ("S18", "he never agreed"), ("S33", "The killing was")):
        ev.append((sid, at(sid, ph), S.marker(), -14))
    ev.append(("S04", 0.2, S.typing(4.3), -16))
    for sid in ("S53", "S54", "S55"):
        ev.append((sid, at(sid, "Our confidence"), S.whoosh(1.4), -12))
    for sid in ("S10", "S20", "S31", "S41", "S50"):
        ev.append((sid, 0.1, S.whoosh(1.6), -10))
    return ev


if __name__ == "__main__":
    E.main(sys.modules[__name__])
