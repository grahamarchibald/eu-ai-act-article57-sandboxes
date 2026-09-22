#!/usr/bin/env python3
"""Produce an anonymised build of the dataset for blind peer review.

Run from the repository root:  python3 scripts/build_anonymous.py
Writes dist/anonymous/ and then scans the result for residual identifiers,
exiting non-zero if any survive. The attributed repository is unchanged.

dist/anonymous is cleared and rebuilt on every run, so a file removed upstream
cannot survive into a submission package.

ACM FAccT requires anonymised submission: "Authors must omit their names and
affiliations from the submission." Submit the anonymised build, cite it as
withheld for review, and publish the attributed repository after decisions.
"""
import os, re, shutil, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST = os.path.join(ROOT, "dist", "anonymous")

COPY = ["README.md", "CODEBOOK.md", "CORRECTIONS.md", "CHANGELOG.md", "LICENSE",
        "data", "figures", "scripts"]

# Applied longest-first so that "David M. Liu" is replaced before "Liu".
REDACTIONS = [
    ("Archibald, G. (2026)", "Author (2026)"),
    ("Copyright (c) 2026 Graham Archibald", "Copyright (c) 2026 the author"),
    ("Compiled as the empirical component of *The Healthcare AI Trilemma*, with "
     "Dr. David M. Liu (UBC School of Biomedical Engineering).",
     "Compiled as the empirical component of a manuscript under review. Author "
     "and affiliation withheld for anonymous review."),
    ("David M. Liu", "[author]"),
    ("David Liu", "[author]"),
    ("Graham Archibald", "[author]"),
    ("Archibald", "[author]"),
    ("The Healthcare AI Trilemma", "[manuscript title withheld]"),
    ("Healthcare AI Trilemma", "[manuscript title withheld]"),
    ("University of British Columbia", "[affiliation withheld]"),
    ("UBC", "[affiliation withheld]"),
    ("gramarchibald@gmail.com", "[contact withheld]"),
]

# Anything matching these in the output is a failure.
FORBIDDEN = re.compile(
    r"archibald|\bgraham\b|david\s+m?\.?\s*liu|\bUBC\b|University of British Columbia"
    r"|healthcare ai trilemma|gramarchibald",
    re.I,
)

TEXT_EXT = {".md", ".csv", ".py", ".txt", ""}


def redact(text):
    for old, new in REDACTIONS:
        text = text.replace(old, new)
    return text


def main():
    if os.path.isdir(DIST):
        shutil.rmtree(DIST)          # so a file removed upstream cannot linger
    os.makedirs(DIST)
    skip = shutil.ignore_patterns(os.path.basename(__file__), "__pycache__")

    for item in COPY:
        src = os.path.join(ROOT, item)
        dst = os.path.join(DIST, item)
        if not os.path.exists(src):
            print(f"WARN  {item} not found, skipped")
            continue
        if os.path.isdir(src):
            shutil.copytree(src, dst, ignore=skip, dirs_exist_ok=True)
        else:
            shutil.copy2(src, dst)

    touched = 0
    for dirpath, _, files in os.walk(DIST):
        for name in files:
            path = os.path.join(dirpath, name)
            if os.path.splitext(name)[1].lower() not in TEXT_EXT:
                continue
            raw = open(path, encoding="utf-8").read()
            new = redact(raw)
            if new != raw:
                open(path, "w", encoding="utf-8").write(new)
                touched += 1

    # -- verification scan --------------------------------------------------
    hits = []
    for dirpath, _, files in os.walk(DIST):
        for name in files:
            path = os.path.join(dirpath, name)
            if os.path.splitext(name)[1].lower() not in TEXT_EXT:
                continue
            for i, line in enumerate(open(path, encoding="utf-8"), 1):
                for m in FORBIDDEN.finditer(line):
                    hits.append(f"{os.path.relpath(path, ROOT)}:{i}: {m.group(0)!r}")

    print(f"built dist/anonymous/ — {touched} file(s) redacted")
    if hits:
        print("\nFAIL  identifiers survive in the anonymous build:")
        for h in hits:
            print("  " + h)
        return 1
    print("scan clean — no residual identifiers")
    print("\nNote: binary files (figures) are copied unmodified. Check PDF metadata "
          "separately if the figure is embedded in the submission.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
