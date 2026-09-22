#!/usr/bin/env python3
"""Regenerate README tables from the CSV so prose and data cannot drift.

Run from the repository root:  python3 scripts/build_readme.py
Rewrites the blocks between <!-- BEGIN:name --> and <!-- END:name --> markers.
"""
import csv, collections, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(ROOT, "data", "article57-implementation.csv")
README = os.path.join(ROOT, "README.md")

LABEL = {
    "operational": "operational",
    "precursor": "precursor scheme (not Art. 57)",
    "not_art57": "operational but not Art. 57",
    "implementing": "implementing",
    "announced": "announced",
    "nothing_reported": "nothing reported",
}
ORDER = ["operational", "precursor", "not_art57", "implementing", "announced", "nothing_reported"]


def table(header, body):
    out = ["| " + " | ".join(header) + " |", "|" + "|".join(["---"] * len(header)) + "|"]
    out += ["| " + " | ".join(r) + " |" for r in body]
    return "\n".join(out)


def block_status(rows):
    ini = collections.Counter(r["status_initial"] for r in rows)
    ver = collections.Counter(r["status_verified"] for r in rows)
    body = []
    for k in ORDER:
        if not ini[k] and not ver[k]:
            continue
        i = str(ini[k]) if ini[k] else "—"
        v = f"**{ver[k]}**" if ver[k] else "—"
        body.append([LABEL[k], i, v])
    return table(["Status", "Initial", "Verified"], body)


def block_verification(rows):
    body = [[r["member_state"], r["status_initial"], f"**{LABEL[r['status_verified']]}**"]
            for r in rows if r["status_initial"] != r["status_verified"]]
    held = [r["member_state"] for r in rows
            if r["status_verified"] == "operational" and r["adversarial_verification"].strip()]
    for m in held:
        body.insert(0, [m, "operational", "**operational** — holds"])
    return table(["State", "Initial coding", "After verification"], body)


def block_conditions(rows):
    cols = [("derogation_power", "Power to disapply national rules"),
            ("suff_funding", "Dedicated funding"),
            ("suff_graduation", "Exit report with conformity weight"),
            ("suff_recognition", "Art. 58(2) cross-border recognition")]
    keys = ["yes", "by_reference", "partial", "no", "unknown", "n-a"]
    names = {"yes": "yes", "by_reference": "by cross-reference", "partial": "partial",
             "no": "no", "unknown": "unknown", "n-a": "no instrument"}
    counts = {c: collections.Counter(r[c] for r in rows) for c, _ in cols}
    body = []
    for k in keys:
        if not any(counts[c][k] for c, _ in cols):
            continue
        body.append([names[k]] + [str(counts[c][k]) if counts[c][k] else "—" for c, _ in cols])
    return table(["", *[lbl for _, lbl in cols]], body)


def block_health(rows):
    c = collections.Counter(r["health_ai_in_scope"] for r in rows)
    named = sorted(r["member_state"] for r in rows if r["health_ai_in_scope"] == "yes")
    return (f"Health or medical AI is named in scope in **{c['yes']} of {len(rows)}** sandbox designs "
            f"({', '.join(named)}). The remaining {c['not specified']} do not specify it.")


def block_asof(rows):
    dates = sorted({r["last_checked"] for r in rows if r["last_checked"]})
    return f"**Rows last checked {dates[-1]}.**" + (
        f" Earliest row last checked {dates[0]}." if len(dates) > 1 else "")


BLOCKS = {
    "status-table": block_status,
    "verification-table": block_verification,
    "conditions-table": block_conditions,
    "health-finding": block_health,
    "asof": block_asof,
}


def main():
    rows = list(csv.DictReader(open(CSV_PATH, encoding="utf-8")))
    text = open(README, encoding="utf-8").read()
    changed = []
    for name, fn in BLOCKS.items():
        pat = re.compile(rf"<!-- BEGIN:{name} -->.*?<!-- END:{name} -->", re.S)
        if not pat.search(text):
            print(f"WARN  no marker block for {name!r} in README.md")
            continue
        repl = f"<!-- BEGIN:{name} -->\n{fn(rows)}\n<!-- END:{name} -->"
        new, n = pat.subn(lambda m: repl, text)
        if new != text:
            changed.append(name)
        text = new
    open(README, "w", encoding="utf-8").write(text)
    print("regenerated:", ", ".join(changed) if changed else "nothing changed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
