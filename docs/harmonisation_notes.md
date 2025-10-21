---
layout: default
title: Notes
nav_order: 3
description: "Notes on harmonisation across waves. "
---

# Harmonisation notes

Living document capturing contextual checks, questionnaire quirks, and modelling decisions made while harmonising FinScope survey waves. Extend these notes as new indicators or years are incorporated.

## General Notes

- FinScope questionnaire wording and field names change across waves, so every harmonised indicator maps the correct “have now” codes year by year.
- Weighted outputs use the provider-specific weight variable for the wave. Some files (e.g. 2005) lack weights and are excluded from weighted series.
- Survey providers shift across waves: Research Surveys (2006) altered layouts substantially, Ask Afrika (2011) renamed the weight column to `WEIGHT`, and TNS (2012) introduced another round of wording tweaks when the contract moved again.
- Rows with simultaneous nulls across key indicator fields (notably in 2015 for `I1_09`, `H1_12`, `Q5002_`) are dropped before calculating shares.
- Where proxies stand in for missing direct measures, the reasoning is captured in `mappings/harmonised_questions.csv` for future review.

## Measures

### Funeral Insurance
- Treat coverage as “any product in the section currently held”, consolidating multiple funeral product types within each wave.
- 2008 adds “don’t know what the product is” response options; treat them as non-ownership.
- 2009 precedes the product table with a direct question on funeral coverage and payer before reverting to the grid in later waves.
- 2010 funeral ownership uses a four-point response scale where code `4` indicates “have now”.
- 2015 drops rows with simultaneous nulls across `I1_09`, `H1_12`, or `Q5002_` prior to calculating shares.
- 2019 favours `i1_10` (funeral product type) over `C7_3` because it aligns with the product block and yields higher coverage. The `i1_` variables share the response scale `1=never had`, `2=used to have`, `3=have in own name`, `4=covered by someone else`, `99=don’t know`.

### Burial Society Membership
- 2007 places the burial society option at the top of the funeral block and omits the usual “not AVBOB” qualifier.
- 2016 cross-checks `I1_09` against screener `Q.A8`, useful for validation and consistency checks.
- 2019 presents both `C7_3` (personal capacity) and `i1_10` (funeral product type); we treat active membership via `i1_10` to stay coupled to the funeral products grid while capturing higher coverage.

### Life Insurance
- 2005 removes employer, trade union, and church variants to remain comparable with later waves (≈1 percentage point impact).
- 2006 stores life and funeral insurance in a single block whose naming diverges from subsequent questionnaires.
- 2007 dedicates an entire section to life products, re-labelled “insurance” in later questionnaires.
- 2009 repeats the introductory question on life coverage alongside funeral coverage before the grid.
- 2010 relies on `Q151_M`, which records whether the respondent holds the policy but omits any “covered by someone else” probe, so cross-wave comparability needs inspection.

### Bank Account In Own Name
- Before 2012 there is no single ownership screener; combine “have now” responses across `QP1`/`QB1`/`B1`/`Q25`.
- 2010 introduces a five-point scale (`4=have now`), while other waves use three- or four-point versions (`3=have now`). Later questionnaires revert to a single binary question.

### Home Has Electricity
- Direct utility questions appear from 2012 onwards.
- Earlier proxies include LSM electricity ownership (2006), electric stove ownership (2007), “items in household – electricity” (2008–2009), and primary cooking fuel being electricity (2010–2011). These proxies may undercount households with grid access but alternative cooking sources.

### Stokvel Membership
- Historic questionnaires classify stokvels as investment products (`Q67BT`, `Q162_F`, `Q193_G`, `Q202_I`, `Q65_15`) before moving them to the social group module in 2012.
- 2011 codes `1=Don’t have`, `2=Have now`, `3=DK`, `4=NA`; treat only `2` as active membership.

### Credit Card
- Ownership uses the staged product grids; in 2010 the scale expands to include “never had and need / don’t need”, but only the “have now” category (`3` or `4` depending on wave) flags ownership.

### Home Loan
- Purchase and renovation home-loan questions split in 2006–2007; aggregate both when creating the indicator.
- Response handling mirrors the credit card approach, taking the “have now” category on the grid scale.

### Borrowed From Mashonisa / Loan Shark
- 2006–2010 product grids report `Never borrowed / Borrowed before / Borrowing now`; only “Borrowing now” counts as positive.
- 2011 switches to yes/no items, later evolving into G-series 12-month borrowing questions with varying yes/no codes (see `mappings/harmonised_questions.csv` for the exact mapping).

### Retirement Annuity / Provident / Pension
- Combine the three product types via an `any` rule to capture full retirement coverage.
- 2006–2010 use a four-point scale (`never/used to/have now/don’t know`), 2011 records `1=Don’t have`, `2=Have now`, `3=Don’t have` (duplicated label), and 2012+ simplify to `1=Do not have`, `2=Have now`. Watch the 2011 labelling when inspecting raw data.

### Food Insecurity (“Often Went Without Food”)
- Afrobarometer waves (2006–2010) supply explicit frequency options; flag only `1=Often`.
- Ask Afrika (2011) replaces the scale with a binary “went without enough food” item, introducing a structural break.
- Afrobarometer wording returns from 2016 alongside the familiar frequency scale and `20=Don’t know`.

## Further Work

- Add observations for other measures as they are harmonised.
- Note any reweights or revisions when official FinScope datasets update.
- Capture cross-checks (e.g. codebook references) in `mappings/harmonised_questions.csv` to document mapping decisions.
