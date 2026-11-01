"""Pull narration out of a script.md: shot ids, spoken text (pronunciation applied), and
text blocks grouped by act for recording.

    python narration.py <script.md> <out.json>

Output: {"shots": [{"id", "act", "text", "spoken"}], "acts": [{"act", "ids", "spoken"}]}
"spoken" is what goes to the voice model; "text" is what captions use.
"""

import json
import re
import sys


def pron_table(md):
    """Rows of the markdown table under '## Pronunciation' (header and rule skipped)."""
    table = {}
    if "## Pronunciation" not in md:
        return table
    section = md.split("## Pronunciation", 1)[1].split("\n## ", 1)[0]
    rows = [l for l in section.splitlines() if l.strip().startswith("|")][2:]
    for line in rows:
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) == 2 and cells[0] != cells[1]:
            table[cells[0]] = cells[1]
    return table


def apply(text, table):
    for k, v in table.items():
        text = re.sub(re.escape(k), v, text)
    text = text.replace("*", "")
    return text


def parse(md):
    table = pron_table(md)
    shots, act = [], "COLD OPEN"
    cur = None
    for line in md.splitlines():
        if line.startswith("## ") and not line.startswith(("## Pronunciation", "## Sources")):
            act = line[3:].strip()
        m = re.match(r"### ([A-Z]\d+[a-z]?)\b", line)
        if m:
            cur = {"id": m.group(1), "act": act, "lines": []}
            shots.append(cur)
        elif line.startswith("> ") and cur is not None:
            cur["lines"].append(line[2:].strip())
    out = []
    for s in shots:
        text = " ".join(s["lines"])
        out.append({"id": s["id"], "act": s["act"], "text": text.replace("*", ""),
                    "spoken": apply(text, table)})
    acts = []
    for s in out:
        if not s["spoken"]:
            continue
        if not acts or acts[-1]["act"] != s["act"]:
            acts.append({"act": s["act"], "ids": [], "spoken": ""})
        acts[-1]["ids"].append(s["id"])
        acts[-1]["spoken"] += ("\n\n" if acts[-1]["spoken"] else "") + s["spoken"]
    return {"shots": out, "acts": acts}


if __name__ == "__main__":
    data = parse(open(sys.argv[1]).read())
    json.dump(data, open(sys.argv[2], "w"), indent=1)
    for a in data["acts"]:
        print(f'{a["act"]:<22} {len(a["ids"]):>3} shots {len(a["spoken"]):>6} chars')
