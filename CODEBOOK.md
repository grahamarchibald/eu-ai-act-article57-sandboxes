# Codebook

Definitions and coding rules for `data/article57-implementation.csv`. Read this before drawing anything from the data.

`scripts/validate.py` enforces the mechanical parts of what follows. If a rule here is not checked by that script, it is a convention rather than a constraint, and the distinction is worth keeping in mind.

---

## The central decision rule

**`operational` means the sandbox is actually admitting or hosting participants.**

Not: a law exists. Not: an authority has been designated. Not: a minister announced one. A legal framework with nobody in it is `implementing`.

This single rule produces most of the disagreement between this dataset and published counts. It is stated here so anyone who would code it differently can see exactly where they diverge.

A second rule follows from it: **a functioning sandbox is not necessarily an Article 57 sandbox.** A programme can admit participants, publish results and run for years while being constituted under some other legal basis — data protection, a pre-AI-Act pilot, a ministerial memorandum. Those carry none of Art. 57's consequences: no Art. 57(7) exit report usable in conformity assessment, no Art. 57(12) fine immunity, no Art. 58(2) mutual recognition. Conflating the two is the error this dataset was built to detect.

## Status values

| Value | Meaning |
|---|---|
| `operational` | Admitting or hosting participants under an Article 57 legal basis |
| `precursor` | Functioning scheme predating the AI Act, not constituted under Art. 57; Art. 57-native instrument absent or unenacted |
| `not_art57` | Functioning sandbox constituted under some other legal basis entirely |
| `implementing` | Instrument passed or authority designated; not yet admitting participants |
| `announced` | Public commitment, no legal instrument |
| `nothing_reported` | No measures found, including none listed by the Commission |

`status_initial` is the first-pass coding. `status_verified` is the coding after adversarial verification. Where they differ, `verification_note` says why and [CORRECTIONS.md](CORRECTIONS.md) carries the full account.

## The nine dimensions

**1 · Legal instrument** — the *national* instrument establishing the sandbox: law, royal decree, ministerial decision, cabinet regulation. Not the AI Act itself. `none found` where no national instrument exists, which is distinct from one existing but being unlocatable.

**2 · Instrument date** — adoption, publication and entry-into-force where they differ, because they often do and the gap matters. Latvia's law was adopted 6 March 2025, published 19 March, in force 20 March. Recorded twice: as prose in `instrument_date`, which is the evidence, and as ISO dates in the four date columns below, which are for sorting and plotting.

**3 · Competent authority** — the body designated to operate the sandbox. Distinguish from the market-surveillance or notifying authority designated under other AI Act provisions; several states have designated the latter and not the former.

**4 · Sectors in scope** — as stated in the instrument or the authority's published entry criteria. Not inferred from participants admitted.

**5 · Health AI in scope** — `yes` / `no` / `not specified`. **`not specified` is the common case and does not mean excluded.** Coded `yes` only where health, medical or clinical AI is explicitly named in the instrument or published scope.

**6 · Participants admitted** — count and, where published, identity. Recorded as published; where a figure and an entity count don't reconcile, both are noted rather than silently resolved. Normalised into `participants_count` per the rule below.

**7 · Entry criteria published** — whether an applicant could find out how to apply. A proxy for whether the sandbox is usable in practice rather than in principle.

**8 · Exit report required** — whether the national instrument requires the Article 57(7) exit report. The substantive question is not whether *a* report is produced but whether it carries weight in conformity assessment. Spain's Art. 23, for example, is bidirectional and produces a participation certificate plus an evaluation — documents, but not instruments usable in a conformity procedure. That distinction is the graduation mechanism, and `suff_graduation` is the column that grades it.

**9 · Confidence** — `high` / `medium` / `low`, **self-assessed at compilation, not independently checked** except where the adversarial pass ran. Not a quality score; a flag for where to look first.

## Dates

Four ISO `YYYY-MM-DD` columns, blank where the date does not exist or could not be established. **They describe the instrument that creates the sandbox, not the state's AI Act implementing law in general.** Denmark's ISO date fields are therefore empty although Denmark has an AI Act implementing statute — because that statute contains no sandbox provision. That emptiness is the finding, not a gap.

| Column | Meaning |
|---|---|
| `date_adopted` | Adoption or enactment of the sandbox-creating instrument |
| `date_published` | Publication in the official gazette |
| `date_in_force` | Entry into force **of the sandbox provision**, which may postdate the rest of the act (Hungary's §10 commenced 2 August 2026, nine months after the Act) |
| `date_first_participants` | First formal admission of participants, where a date is published |

Blank ≠ zero. A blank `date_in_force` on a row coded `implementing` means the sandbox provision is not in force *or* the date could not be established; the `instrument_date` prose says which.

## Participant counts

`participants_count` normalises the prose in `participants`. The prose is the evidence and is never overwritten.

| Value | Meaning |
|---|---|
| integer | Participants formally admitted. Latvia is `2`: three projects were selected in the first call, two were admitted by administrative act |
| `0` | A sandbox exists and the operating authority or another primary source confirms none have been admitted |
| `unknown` | A sandbox exists in law and the public record is silent either way |
| `n/a` | No sandbox exists to admit to |

The `0` / `unknown` distinction is deliberate and was a correction: an earlier version used the two interchangeably, which made the boundary between `operational` and `implementing` arbitrary. `0` is a positive finding sourced to the authority — Ireland's AI Office stating that eligibility details will follow "when the Sandbox has been developed" is a `0`. `unknown` is an absence of evidence.

## Authority and the conditions for using it

Four columns, each paired with a `_note` column giving the provision relied on. They are coded **from instrument text as recorded in this dataset's own rows**, which means a row whose instrument could not be read in full is `unknown` by construction. `unknown` therefore means *not established from the public record*, never *absent*.

**`derogation_power`** — `yes` / `no` / `unknown` / `n-a`. Does the instrument empower the authority to disapply otherwise-applicable national rules? This is the variable that separates *authority* from *activity*, and collapsing the two is what lets a data-protection sandbox read as an Article 57 one. Latvia is the only `yes`: Article 8 of the AI Centre Law has the Centre issue administrative acts permitting derogation.

**`suff_funding`** — `yes` / `partial` / `no` / `unknown` / `n-a`. Dedicated funding for sandbox operation, as a named budget line, an assigned programme allocation, or a stated fee model. `partial` covers a costed-but-unfunded allocation and a fee-financed model. Almost entirely `unknown`, which is itself the result: for most member states you cannot tell from the public record whether the sandbox is resourced.

**`suff_graduation`** — `yes` / `partial` / `no` / `unknown` / `n-a`. Does an exit report carry weight in conformity assessment? `yes` requires a provision tracking Art. 57(7). `partial` means a report exists but does not demonstrably carry conformity weight — Spain's participation certificate and evaluation, Lithuania's completion report described in a programme page rather than located in the instrument. `no` is a documented negative, not an absence of evidence.

**`suff_recognition`** — `yes` / `by_reference` / `no` / `unknown` / `n-a`. Does the instrument provide for Art. 58(2) mutual recognition? `by_reference` means the instrument cross-refers to Article 58 or to Chapter VI without restating the effect, which is the most common positive form and a weaker one than express provision.

**Two conditions are deliberately not coded.** Staffing levels and whether central guidance preceded national design both matter to whether a sandbox functions, and neither is reliably findable in the instruments. They are left out rather than estimated.

## Provenance

`last_checked` is an ISO date per row: the day the row's claims and its source URLs were last verified. It doubles as the source access date. A row's substantive content should be read as a statement about that date and nothing later.

## Source hierarchy

1. The national instrument itself, in the official gazette
2. The competent authority's own publications
3. EUR-Lex; the European Commission's AI Act Service Desk national-resources page
4. Official government announcements

Tracker sites, law-firm summaries and aggregators: **orientation only, never a source of record.** Many carry pre-Digital-Omnibus dates. Regulation (EU) 2026/1744 moved the Art. 57 deadline from 2 August 2026 to 2 August 2027; any source implying the 2026 date is still live predates it.

`nothing_reported` was corroborated against the Commission's own national-resources page where possible — an absence confirmed by an EU-level source is stronger than an absence from a search.

## Verification protocol

Applied to every `operational` claim:

1. The second pass is briefed to **refute**, not confirm.
2. **Default to refuted** where primary-source confirmation cannot be found.
3. Check the competent authority's own site and the national instrument directly, not the summary that generated the claim.
4. Report the corrected status and the primary source relied on.

Where a claim survives that, `adversarial_verification` records what was checkable and what was not.

## Columns

| Column | Notes |
|---|---|
| `member_state` | |
| `status_initial` | First-pass coding |
| `status_verified` | Post-verification coding |
| `verification_note` | Why the two differ |
| `confidence` | Self-assessed, see dimension 9 |
| `date_adopted` · `date_published` · `date_in_force` · `date_first_participants` | ISO dates, see **Dates** |
| `participants_count` | Normalised, see **Participant counts** |
| `derogation_power` + `_note` | See **Authority and the conditions for using it** |
| `suff_funding` + `_note` · `suff_graduation` + `_note` · `suff_recognition` + `_note` | As above |
| `last_checked` | ISO date; also the source access date |
| `legal_instrument` · `instrument_date` · `competent_authority` · `sectors_in_scope` · `health_ai_in_scope` · `participants` · `entry_criteria_published` · `exit_report_required` | The nine dimensions |
| `adversarial_verification` | Full text of the verification pass, where run |
| `notes` | |
| `source_urls` | |
