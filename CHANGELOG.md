# Changelog

Dataset versions. Coding reversals are recorded separately and in full in [CORRECTIONS.md](CORRECTIONS.md).

## v0.5 — 2026-09-21

Schema and tooling. **No substantive recoding of any state's status**; every `status_verified` value is unchanged from v0.4.

Added:

- **ISO date columns** — `date_adopted`, `date_published`, `date_in_force`, `date_first_participants`. They describe the sandbox-creating instrument specifically, so Denmark's are empty despite Denmark having an AI Act implementing statute. The `instrument_date` prose is untouched and remains the evidence.
- **`participants_count`** — normalises the prose in `participants` into an integer, `0`, `unknown` or `n/a`. Fixes an inconsistency carried since v0.1, where a sandbox with no participants and a sandbox with no published count were both recorded as `unknown`, making the `operational` / `implementing` boundary arbitrary. `0` now requires a positive statement from the authority or another primary source.
- **`derogation_power`** — whether the instrument empowers the authority to disapply otherwise-applicable national rules. Separates authority from activity. One `yes` across 27 states.
- **Three condition columns** — `suff_funding`, `suff_graduation`, `suff_recognition`, each with a `_note` giving the provision relied on. Coded from instrument text already in the rows; `unknown` where the instrument could not be read in full, which is most of them.
- **`last_checked`** — ISO date per row, doubling as the source access date.
- **`scripts/validate.py`** — controlled vocabularies, ISO date formats and ordering, the operational decision rule, and a requirement that every coded judgement carries a note and at least one source URL. Exits non-zero on failure.
- **`scripts/build_readme.py`** — regenerates every table in the README from the CSV, so the prose cannot drift from the data. The v0.4 README counts were hand-typed.
- **`scripts/make_figure.py`** — timeline of national instruments against the original and deferred Article 57 deadlines.
- **`scripts/build_anonymous.py`** — produces an anonymised build under `dist/anonymous/` for blind peer review.

Not added, deliberately: staffing levels and the timing of central guidance. Both matter and neither is reliably findable in the instruments; estimating them would have put inference into columns that are otherwise sourced.

Outstanding items from v0.4 are unchanged and still outstanding — see the closing section of [CORRECTIONS.md](CORRECTIONS.md).

## v0.4 — 2026-09-08

Three primary-source spot-checks run in the main loop rather than as agents. France and Romania corroborated against the Commission's own national-resources page (nothing listed for either). Spain's sunset clause verified verbatim from the BOE — approximately November 2026, no enacted successor — and promoted to a headline finding. Corrected v0.3's exit-report claim, which overstated the direction problem: Spain's Art. 23 is bidirectional and the real gap is conformity-assessment weight.

## v0.3 — 2026-09-08

Spain resolved as a precursor scheme. Latvia confirmed as likely the only genuine operational Art. 57 sandbox, with a paediatric medical AI case. Adversarial critique run in place of the failed critic agent.

## v0.2 — 2026-09-08

All 27 coded. Denmark refuted — a GDPR sandbox, not an Article 57 one. Headline: 24 of 27 do not name health AI.

## v0.1 — 2026-09-08

Initial run, 20 of 27, quota-limited. Not citable.
