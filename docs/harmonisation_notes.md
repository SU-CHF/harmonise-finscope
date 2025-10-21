---
layout: default
title: Harmonisation notes
nav_order: 5
description: "Contextual checks, questionnaire quirks, and modelling decisions by survey year."
---

# Harmonisation notes

Living document capturing contextual checks, questionnaire quirks, and modelling decisions made while harmonising FinScope survey waves. Extend these notes as new indicators or years are incorporated.

## Overview

- FinScope questionnaire wording changes across waves, including shifts in field names, response codes, and survey providers. Each harmonised indicator must therefore map the correct variable(s) and “have now” codes per year.
- Funeral insurance is often split into multiple product types. Harmonisation treats the indicator as “any product in the section currently held”.
- Weighted outputs use the provider-specific weight variable for the wave. Some files (e.g. 2005) lack weights and are excluded from the weighted series.

## Year-specific Highlights

### 2005
- Multiple life cover variants (employer, trade union, church) were excluded to maintain comparability with later waves—impact roughly one percentage point.

### 2006
- Survey administered by Research Surveys; question layout differs markedly from 2007 onward.
- Life and funeral insurance captured in a single block of variables, so field references depart from later naming conventions.

### 2007
- Entire section devoted to life insurance as a group of products; re-labelled “insurance” in later waves.
- Burial society option appears first in the funeral block and omits the “not AVBOB” qualifier seen elsewhere.

### 2008
- Funeral-insurance block introduces “don’t know what the product is” response options; ensure codes are handled appropriately.

### 2009
- Includes an introductory question asking directly about funeral/life coverage and who pays. Later questionnaires embed similar content inside product tables.

### 2010
- Life insurance question (`Q151_M`) does not ask if coverage is via someone else; review comparability when combining with later waves.
- Funeral insurance response scale differs (`1` = “never had and need”, `4` = “have now”); mapping uses code `4`.

### 2011
- Provider switches to Ask Afrika; weights column `WEIGHT` differs from earlier naming.

### 2012
- Provider switches to TNS; verify transitions in question wording when comparing 2011 to 2012 onwards.

### 2015
- High missingness around indicators; rows with nulls across `I1_09`, `H1_12`, and `Q5002_` dropped prior to computing shares.

### 2016
- Burial society item (`I1_09`) explicitly cross-checks against an earlier screener question (`Q.A8`); note for potential validation.

### 2019
- Burial societies captured by `C7_3` (personal capacity) and `i1_10` (funeral insurance type). `i1_10` chosen because it yields higher coverage and aligns with the funeral products block.
- `i1_` variables share a response scale: `1` “never had”, `2` “used to have”, `3` “have it in my name”, `4` “covered by somebody else”, `99` “don’t know”.

## Indicator-specific assumptions (2006–2011 extensions)

- **Bank account in own name**: No single ownership screener exists before 2012. We OR the “have now” responses across the bank product grids (`QP1`/`QB1`/`B1`/`Q25`). Note that 2010 introduces a five-point scale (`4 = have now`), while other years use three- or four-point versions (`3 = have now`). Later waves revert to a single binary question.
- **Home has electricity**: Direct utility questions only appear from 2012 onward. Earlier mappings rely on proxies—LSM electricity ownership in 2006, electric stove ownership in 2007, “items in household – electricity” in 2008–2009, and electricity as the primary cooking fuel in 2010–2011. These proxies may under-count households that use non-electric cooking but have grid supply.
- **Stokvel membership**: Historic questionnaires treat stokvels as investment products (`Q67BT`, `Q162_F`, `Q193_G`, `Q202_I`, `Q65_15`) before moving them into the social group module from 2012. Coding shifts in 2011 (`1=Don’t have`, `2=Have now`, `3=DK`, `4=NA`); only `2` is treated as active membership.
- **Credit card & home loan**: The same staged product grids capture ownership, with 2010 adding “never had and need / don’t need” disaggregation. We continue to take only the “have now” category (`3` or `4`, depending on the wave) and aggregate across purchase/renovation home-loan questions in 2006–2007.
- **Borrowed from mashonisa/loan shark**: Product usage grids provide `Never borrowed / Borrowed before / Borrowing now` for 2006–2010; only `Borrowing now` is positive. From 2011 the questionnaire switches to yes/no items, and later to G-series 12-month borrowing questions with different yes/no codes (captured in the mapping notes).
- **Retirement annuity / provident / pension**: All three product types are combined via an `any` rule. Response scales vary—2006–2010 use a 4-point “never/used to/have now/don’t know”, 2011 records `1=Don’t have`, `2=Have now`, `3=Don’t have` (duplicated label in the codebook), and 2012+ simplify to `1=Do not have`, `2=Have now`. Analysts should be aware of the inconsistent labelling in 2011 when inspecting raw data.
- **Food insecurity (“Often went without food”)**: The Afrobarometer crying questions (2006–2010) provide explicit frequency options; we flag only `1=Often`. Ask Afrika (2011) replaces the scale with a binary “went without enough food” item, introducing a potential structural break in the time series. The Afrobarometer LPI resurfaces from 2016 with the familiar scale plus `20=Don’t know`.
- **General coding**: Where proxies replace direct measures (e.g. electricity access), the rationale is recorded in `mappings/harmonised_questions.csv`. Future access to richer household services variables should trigger a review of these assumptions.

## Further Work

- Add observations for other years or product groups as they are harmonised.
- Note any reweights/revisions when official FinScope datasets are updated.
- Capture cross-checks (e.g. against codebooks, metadata) that justify each mapping in `mappings/harmonised_questions.csv`.
