---
layout: default
title: Getting started
nav_order: 2
description: "Install dependencies, configure data paths, and sanity check your setup."
---

# Getting started

Follow these steps to prepare a local environment capable of harmonising FinScope survey data.

## Prerequisites
- Python 3.10 or newer with `pip`
- Core libraries: `pandas`, `numpy`, `pyreadstat`, `python-dotenv`
- Access to the FinScope Consumer South Africa survey extracts (`FS_{year}.dta`)

Install the Python dependencies into a virtual environment of your choice:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt  # or pip install pandas numpy pyreadstat python-dotenv
```

> The repository keeps explicit Python dependencies lightweight. Feel free to pin versions in `requirements.txt` if you prefer reproducibility across machines.

## Configure data access
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

## Optional tooling
- **Make (recommended):** Run `make` to view available automation targets (`make single`, `make harmonise`, `make summary`).
- **Spreadsheet editor:** Update `mappings/harmonised_questions.csv` directly in Excel or LibreOffice; no specialist tooling required.
- **Jupyter/Quarto:** Use notebooks in `notebooks/` for exploratory validation before promoting cleaned logic into `scripts/`.

Next, move over to the workflow guide to generate harmonised outputs for a given wave.
