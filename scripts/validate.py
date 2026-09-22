#!/usr/bin/env python3
"""Schema and consistency checks for data/article57-implementation.csv.

Run from the repository root:  python3 scripts/validate.py
Exits non-zero if any check fails. Intended to be run after every edit.
"""
import csv, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(ROOT, "data", "article57-implementation.csv")

MEMBER_STATES = {
    "Austria","Belgium","Bulgaria","Croatia","Cyprus","Czechia","Denmark","Estonia",
    "Finland","France","Germany","Greece","Hungary","Ireland","Italy","Latvia",
    "Lithuania","Luxembourg","Malta","Netherlands","Poland","Portugal","Romania",
    "Slovakia","Slovenia","Spain","Sweden",
}

ENUMS = {
    "status_initial":   {"operational","precursor","not_art57","implementing","announced","nothing_reported"},
    "status_verified":  {"operational","precursor","not_art57","implementing","announced","nothing_reported"},
    "confidence":       {"high","medium","low"},
    "health_ai_in_scope": {"yes","no","not specified"},
    "entry_criteria_published": {"yes","no","unknown"},
    "exit_report_required": {"yes","no","unknown"},
    "derogation_power": {"yes","no","unknown","n-a"},
    "suff_funding":     {"yes","partial","no","unknown","n-a"},
    "suff_graduation":  {"yes","partial","no","unknown","n-a"},
    "suff_recognition": {"yes","by_reference","no","unknown","n-a"},
}

DATE_COLS = ["date_adopted","date_published","date_in_force","date_first_participants","last_checked"]
ISO = re.compile(r"^\d{4}-\d{2}-\d{2}$")

errors, warnings = [], []


def err(ms, msg):
    errors.append(f"{ms}: {msg}")


def warn(ms, msg):
    warnings.append(f"{ms}: {msg}")


def main():
    rows = list(csv.DictReader(open(CSV_PATH, encoding="utf-8")))

    # -- coverage ---------------------------------------------------------
    seen = {r["member_state"] for r in rows}
    if seen != MEMBER_STATES:
        for m in MEMBER_STATES - seen:
            errors.append(f"missing row for {m}")
        for m in seen - MEMBER_STATES:
            errors.append(f"unexpected row {m!r}")
    if len(rows) != len(seen):
        errors.append("duplicate member_state rows present")

    for r in rows:
        ms = r["member_state"]

        # -- controlled vocabularies --------------------------------------
        for col, allowed in ENUMS.items():
            v = r.get(col, "").strip()
            if v not in allowed:
                err(ms, f"{col}={v!r} not in {sorted(allowed)}")

        # -- date formats -------------------------------------------------
        for col in DATE_COLS:
            v = r.get(col, "").strip()
            if v and not ISO.match(v):
                err(ms, f"{col}={v!r} is not ISO YYYY-MM-DD")

        # -- date ordering ------------------------------------------------
        a, p, f = r["date_adopted"], r["date_published"], r["date_in_force"]
        if a and p and p < a:
            err(ms, f"date_published {p} precedes date_adopted {a}")
        if p and f and f < p:
            err(ms, f"date_in_force {f} precedes date_published {p}")

        # -- participants_count -------------------------------------------
        pc = r["participants_count"].strip()
        if pc not in {"unknown", "n/a"} and not pc.isdigit():
            err(ms, f"participants_count={pc!r} is not an integer, 'unknown' or 'n/a'")

        # -- the central decision rule ------------------------------------
        # operational requires (a) admitted participants and (b) an Art. 57 basis
        if r["status_verified"] == "operational":
            if not (pc.isdigit() and int(pc) > 0):
                err(ms, "status_verified=operational but participants_count is not a positive integer")
            if not r["date_in_force"]:
                err(ms, "status_verified=operational but no date_in_force for a sandbox instrument")
        if pc.isdigit() and int(pc) > 0 and r["status_verified"] in {"implementing", "announced", "nothing_reported"}:
            err(ms, f"participants_count={pc} contradicts status_verified={r['status_verified']}")
        if r["status_verified"] in {"announced", "nothing_reported"} and r["date_in_force"]:
            err(ms, f"status_verified={r['status_verified']} but a sandbox instrument is coded in force")

        # -- health scope needs textual support ----------------------------
        if r["health_ai_in_scope"] == "yes" and len(r["sectors_in_scope"]) < 40:
            err(ms, "health_ai_in_scope=yes but sectors_in_scope carries no supporting text")

        # -- verification bookkeeping --------------------------------------
        if r["status_initial"] != r["status_verified"] and not r["verification_note"].strip():
            err(ms, "status changed in verification but verification_note is empty")
        if r["status_verified"] == "operational" and not r["adversarial_verification"].strip():
            err(ms, "coded operational without an adversarial_verification record")

        # -- coded judgements need their note ------------------------------
        for col in ("derogation_power", "suff_funding", "suff_graduation", "suff_recognition"):
            note = r.get(col + "_note", "").strip()
            if r[col] in {"yes", "no", "partial", "by_reference"} and not note:
                err(ms, f"{col}={r[col]} but {col}_note is empty")

        # -- sourcing -------------------------------------------------------
        if len(re.findall(r"https?://", r["source_urls"])) == 0:
            err(ms, "no source URLs")
        if not r["last_checked"].strip():
            err(ms, "last_checked is empty")

        # -- warnings (not failures) ----------------------------------------
        if r["confidence"] == "low":
            warn(ms, "confidence=low — treat as a flagged gap, not a data point")
        if r["status_verified"] == "implementing" and r["date_in_force"] and r["date_in_force"] < "2026-01-01":
            warn(ms, f"sandbox instrument in force since {r['date_in_force']} and still not operational — re-check")

    # -- report -------------------------------------------------------------
    for w in warnings:
        print(f"WARN  {w}")
    for e in errors:
        print(f"FAIL  {e}")
    print(f"\n{len(rows)} rows checked — {len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
