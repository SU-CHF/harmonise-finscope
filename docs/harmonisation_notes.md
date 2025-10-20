# Harmonisation Notes

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

## Further Work

- Add observations for other years or product groups as they are harmonised.
- Note any reweights/revisions when official FinScope datasets are updated.
- Capture cross-checks (e.g. against codebooks, metadata) that justify each mapping in `mappings/harmonised_questions.csv`.
