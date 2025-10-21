---
layout: default
title: Code explained
nav_order: 2
description: "How the conde produces the harmonised series."
---

# Code explained

## Mappings & outputs

The harmonisation pipeline is based on two key spreadsheets that control how the measure each year is harmonised. 

### Key lookup tables
#### `harmonised_questions.csv`
- One row per `(indicator, year)` pair.
- Columns describe the raw field(s) to extract, the comparison operator (e.g. match by prefix), the qualifying response values, and the label shown in outputs.
- Designed for editing in Excel/LibreOffice; scripts accept the CSV as-is.

#### `year_weights.csv`
- Stores the survey-specific weight variable name for each wave.
- Update this table whenever a new FinScope dataset uses a different weighting column.

### Directory overview
- `mappings/` — CSV files that control question mappings, weight variables, and value recodes.
- `scripts/` — Python entry points (`clean_year.py`, `harmonise.py`, `summarise.py`) that apply the mappings.
- `outputs/` — Generated CSV/Parquet files containing cleaned and harmonised survey data.
- `docs/` — Narrative notes, including this documentation site and `harmonisation_notes.md` for contextual decisions.

### Generated datasets
- `outputs/finscope_harmonised.csv` — Wide table with one row per respondent per year and harmonised indicator columns.
- `outputs/finscope_harmonised_long.csv` — Long-format version useful for dashboarding or modelling (one row per indicator per respondent).

### Extending the mappings
1. Identify raw question codes and response values for the new indicator in each survey year.
2. Append rows to `harmonised_questions.csv`, filling in the indicator name, field type, and qualifying values.
3. Document any judgement calls in `docs/harmonisation_notes.md` so future contributors understand the rationale.


## Run the harmonisation on your own computer

Follow these steps to prepare a local environment capable of harmonising FinScope survey data.

### Prerequisites
- Python 3.10 or newer with `pip`
- Core libraries: `pandas`, `numpy`, `pyreadstat`, `python-dotenv`
- Access to the FinScope Consumer South Africa survey extracts (`FS_{year}.dta`)

### Configure data access
1. Identify the directory that stores your FinScope `.dta` files. The loaders expect them under `finscope/dta/FS_{year}.dta`.
2. Create a `.env` file in the project root (or set the variable globally) that points to this location:

   ```bash
   echo "DATA_PATH=/path/to/shared/data" >> .env
   ```

3. Confirm the environment variable resolves correctly:

   ```bash
   source .env
   echo $DATA_PATH
   ```

The scripts use `DATA_PATH` to locate raw surveys without hard-coding shared drive paths.

### Run the harmonisation
- **Make (recommended):** Run `make harmonise` to produce the harmonised series.

This command:
- Reads the mappings and weight configuration (`mappings/year_weights.csv`)
- Loads each survey wave from `DATA_PATH`
- Produces both wide (`finscope_harmonised.csv`) and long (`finscope_harmonised_long.csv`) outputs under `outputs/`
- Regenerates the homepage summary JSON used by the documentation chart

### Inspect the result

```bash
make summary
```

The summary target refreshes descriptive tables (weighted shares by year) to spot-test your indicators.

