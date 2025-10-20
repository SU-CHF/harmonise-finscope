---
layout: default
title: Workflow
nav_order: 3
description: "Run the cleaning, harmonisation, and summary steps for FinScope surveys."
---

# Workflow

Use the make targets and scripts in this repository to harmonise one or more FinScope survey waves into a consistent time series.

## 1. Point to the raw files
Ensure the `DATA_PATH` environment variable references the directory that hosts `finscope/dta/FS_{year}.dta`. All scripts resolve raw inputs relative to this path.

## 2. (Optional) Clean a single wave
Generate reduced extracts or narrower column subsets when you want to explore a particular survey year:

```bash
make single
# or run non-interactively:
python scripts/clean_year.py 2019 --keep-columns H3a_13 i1_10 --output-format parquet
```

Outputs are written to `outputs/` by default, alongside the harmonised tables.

## 3. Review or extend mappings
- Open `mappings/harmonised_questions.csv` in your spreadsheet editor.
- Each row specifies a survey year, indicator ID, field selection rule (single column vs prefix), and any value recodes.
- Capture rationale or quirks in `docs/harmonisation_notes.md` as you tweak mappings.

When adding a new indicator, populate a row per year and re-run the harmonisation step.

## 4. Generate the harmonised tables

```bash
make harmonise
# or:
python scripts/harmonise.py --output-dir outputs
```

This command:
- Reads the mappings and weight configuration (`mappings/year_weights.csv`)
- Loads each survey wave from `DATA_PATH`
- Produces both wide (`finscope_harmonised.csv`) and long (`finscope_harmonised_long.csv`) outputs under `outputs/`
- Regenerates the homepage summary JSON used by the documentation chart

## 5. Inspect the result

```bash
make summary
```

The summary target refreshes descriptive tables (weighted shares by year) to spot-test your indicators.

## Troubleshooting
- **Missing raw files:** Double-check `DATA_PATH` and confirm `FS_{year}.dta` exists for the year you are processing.
- **New weight variables:** Update `mappings/year_weights.csv` if a wave uses a different weight column name.
- **Unexpected nulls:** Review the mapping instructions to ensure the correct response codes are included in the harmonised indicator.
