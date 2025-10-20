---
layout: default
title: Mappings & outputs
nav_order: 4
description: "Understand the lookup tables that drive harmonisation and the datasets they generate."
---

# Mappings & outputs

The harmonisation pipeline is intentionally spreadsheet-friendly. Lookup tables define how each survey wave feeds into the harmonised indicators, while scripted helpers generate analysis-ready datasets.

## Directory overview
- `mappings/` — CSV files that control question mappings, weight variables, and value recodes.
- `scripts/` — Python entry points (`clean_year.py`, `harmonise.py`, `summarise.py`) that apply the mappings.
- `outputs/` — Generated CSV/Parquet files containing cleaned and harmonised survey data.
- `docs/` — Narrative notes, including this documentation site and `harmonisation_notes.md` for contextual decisions.

## Key lookup tables
### `harmonised_questions.csv`
- One row per `(indicator, year)` pair.
- Columns describe the raw field(s) to extract, the comparison operator (e.g. match by prefix), the qualifying response values, and the label shown in outputs.
- Designed for editing in Excel/LibreOffice; scripts accept the CSV as-is.

### `year_weights.csv`
- Stores the survey-specific weight variable name for each wave.
- Update this table whenever a new FinScope dataset uses a different weighting column.

### Other mapping files
- Use auxiliary CSVs (e.g. response recodes) to normalise categorical values. Reference them directly from the scripts if you introduce new logic.

## Generated datasets
- `outputs/finscope_harmonised.csv` — Wide table with one row per respondent per year and harmonised indicator columns.
- `outputs/finscope_harmonised_long.csv` — Long-format version useful for dashboarding or modelling (one row per indicator per respondent).
- `outputs/finscope_{year}_clean.*` — Optional reduced extracts created by the cleaning helpers.

Outputs are overwritten on each run; commit snapshots selectively if you need to preserve historic exports.

## Extending the mappings
1. Identify raw question codes and response values for the new indicator in each survey year.
2. Append rows to `harmonised_questions.csv`, filling in the indicator name, field type, and qualifying values.
3. Run `make harmonise` to regenerate the harmonised tables.
4. Document any judgement calls in `docs/harmonisation_notes.md` so future contributors understand the rationale.
