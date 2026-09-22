# Corrections

Every conclusion this dataset reversed, and what reversed it.

This file exists because a dataset that reports no errors is either trivial or not looking. The gap between `status_initial` and `status_verified` in the CSV is the visible part; this is the account.

---

## 1 · Denmark — refuted

**Was:** `operational`, confidence `high`.
**Now:** `not_art57`.

Denmark does run a genuine AI regulatory sandbox. Three rounds, seven projects, real participants including a health and elderly-care documentation project. Every surface signal said operational.

It was established **administratively in March 2024** under the national digitalisation strategy, as a **GDPR / data-protection sandbox**. Checking the Danish instruments directly: neither Lov nr. 467 af 14. maj 2025 (in force 2 August 2025) nor the AI-loven (L 111, in force 2 August 2026) contains a sandbox provision. Lov nr. 467 designates authorities and sets sanctions. That is all.

So there is no Danish instrument creating an Article 57 sandbox. What exists carries no Art. 57(7) exit-report obligation and no Art. 57(9) legal certainty.

**What caught it:** the verification pass was briefed to refute rather than confirm, and to check the national instrument directly rather than the summary that generated the claim. A pass briefed to confirm would have found the three rounds of participants and stopped.

**Why it generalises:** if a data-protection sandbox can be counted as an Art. 57 sandbox in one widely-cited case, published counts of "operational AI sandboxes" are probably inflated in the same way elsewhere. That is the dataset's most transferable finding and it came out of a correction.

## 2 · Spain — reclassified

**Was:** `operational`, confidence `medium`, flagged `UNVERIFIED — verify agent did not run`.
**Now:** `precursor`.

Spain's scheme runs under **Real Decreto 817/2023** (BOE-A-2023-22767, published 9 November 2023) — a **pre-AI-Act instrument**, drafted against the *proposed* Regulation. Twelve high-risk systems from 44 applications, cohort from April 2025, two of them medical devices.

The RD's own *vigencia* clause, verbatim from the BOE:

> *"Este real decreto tendrá una vigencia de máximo treinta y seis meses desde su entrada en vigor o, en su caso, hasta que sea aplicable en el Reino de España el Reglamento… en materia de inteligencia artificial."*

Thirty-six months from entry into force, **or** until the Regulation becomes applicable in Spain, whichever is first. The Article 57-native successor — *Proyecto de Ley Orgánica para el buen uso y la gobernanza de la IA*, approved by the Consejo de Ministros 26 May 2026 — **is still a bill**.

The EU's most-cited operational AI sandbox is a precursor scheme approaching sunset with no enacted replacement.

⚠️ **Outstanding:** the exact entry-into-force date in the RD's *disposición final* has not been confirmed, so no sunset month is stated as fact here.

## 3 · The exit-report claim — my own error, corrected

An earlier draft asserted that Spain's Art. 23 reporting obligation runs in the **opposite direction** to Art. 57(7) — that participants report to the authority rather than the authority producing a report for the participant.

Reading the BOE text directly, that was wrong. Spain's Art. 23 is **bidirectional**: participants submit a report to the Subdirección General, *and* the authority issues the participant *"un documento acreditativo de su participación en el mismo junto con un informe de valoración de los resultados obtenidos"* — a participation certificate plus an evaluation report.

The real distinction is narrower and more interesting. Art. 57(7) makes the authority's exit report **usable as evidence in conformity assessment**. Spain's produces documents, but not instruments carrying weight in a conformity procedure. The graduation gap survives the correction; the original framing of it did not.

**What caught it:** reading the primary text instead of the earlier characterisation of it.

## 4 · A dating error reproduced from a tracker page

Regulation (EU) 2026/1744 (the Digital Omnibus on AI, adopted 8 July 2026) moved the Article 57 deadline from **2 August 2026 to 2 August 2027**, before the original date took effect.

Widely mirrored tracker pages still carry the superseded date. This compilation's own pipeline reproduced that error from one such page, and it reached a working draft before a primary-source check caught it.

**What caught it:** checking the amending instrument rather than a page describing it.

**What changed as a result:** the source hierarchy in [CODEBOOK.md](CODEBOOK.md) — trackers for orientation only, never as a source of record — is written down *because* of this, not as a general principle stated in advance.

---

## Still outstanding

Listed rather than quietly carried:

- **Exact entry-into-force date of RD 817/2023** (*disposición final*), before any sunset month is printed.
- **Moncloa entity counts** (18 SMEs, 6 startups) do not reconcile with the published "12 systems" — probably consortium members. Not cited until resolved.
- **Latvia's third selected project** (Process-as-Code): two of three were formally admitted by administrative act on 17 August 2026, both high-risk. What happened to the third is unconfirmed. Do not assert it was not high-risk.
- **Confidence values on the other 24 states** are self-reported desk research, presented as such. The decision taken was to spot-check the weak points and label the rest honestly rather than claim verification that did not happen.
