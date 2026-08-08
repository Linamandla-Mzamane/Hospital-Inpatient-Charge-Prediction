# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project status

This repository is currently just a scaffold: a `.venv` (Python 3.14, only `pip` installed — no
project dependencies yet) and two reference PDFs. There is no source code, no git repository, no
`pyproject.toml`, and no dataset checked in yet. Treat the two PDFs in the repo root as the
authoritative spec for what to build:

- `Project1_Insurance_Charges_Prediction.pdf` — the task brief (what to build, in what order).
- `ml_project_setup_playbook.pdf` — the project-structure/tooling checklist to follow while building it.

## What this project is

A portfolio data-science project: build a multiple linear regression model that predicts what a
hospital charges for an inpatient procedure (DRG), using real CMS billing data. The deliverable is a
single Jupyter notebook, **`hospital_charges_prediction.ipynb`**.

**Dataset**: "Hospital Charges for Inpatients" (CMS data via Kaggle,
`kaggle.com/datasets/speedoheck/inpatient-hospital-charges`), ~163k rows, one row per
hospital/DRG. Key columns: `DRG Definition` (~100 categories), `Provider State`,
`Hospital Referral Region Description`, `Total Discharges`, `Average Covered Charges`,
`Average Total Payments`, `Average Medicare Payments`. The three charge/payment columns arrive as
currency strings (e.g. `"$32,963.07"`) and must be cleaned to floats.

### Required notebook flow (in order)

1. Load CSV, inspect shape/dtypes, strip whitespace from column names.
2. Clean currency columns (`Average Covered Charges`, `Average Total Payments`,
   `Average Medicare Payments`) → strip `$`/commas, cast to float.
3. Drop identifier columns that aren't useful predictors: `Provider Id`, `Provider Name`,
   `Provider Street Address`, `Provider Zip Code`. Keep `Provider State` and `DRG Definition` as
   categorical predictors.
4. EDA: distribution of `Average Covered Charges`; charges by top 10-15 DRG categories and by state.
5. Handle missing values / duplicates, with reasoning documented in a markdown cell.
6. One-hot encode `Provider State`; for `DRG Definition` either one-hot encode directly or bucket
   rare categories into `"Other"` first (explain the choice in markdown).
7. Build `X` (Total Discharges + encoded categoricals) and `y` (`Average Covered Charges`). **Do not**
   include `Average Total Payments` or `Average Medicare Payments` in `X` — they leak the target.
8. 80:20 train/test split.
9. Fit `sklearn.linear_model.LinearRegression`; print intercept + coefficients.
10. Predict on the test set; evaluate with RMSE and R² (`sklearn.metrics`); residual plot
    (predicted vs. actual − predicted).
11. Interpret coefficients in plain language (markdown) — which DRG/state drives cost variation.
12. Engineer a `charge-to-payment ratio` (`Average Covered Charges / Average Medicare Payments`);
    identify the 5 DRGs/states with the largest markups.
13. Refit the same features against `Average Medicare Payments` as an alternate target; compare
    RMSE/R²/coefficients to the original model.
14. Refit with `Ridge` and `Lasso` (`sklearn.linear_model`); compare RMSE/R² against plain OLS and
    note whether regularisation changes which features dominate.
15. Write a 5-8 sentence summary of findings plus one recommendation for a healthcare payer.

## Intended project structure

No code exists yet, but the setup playbook prescribes a standard **src layout** for this and future
ML portfolio projects — follow it when scaffolding files rather than putting scripts in the repo root:

```
├── .gitignore
├── LICENSE
├── README.md
├── pyproject.toml
├── data/
│   ├── raw/            # original CSV, untouched — treat read-only
│   └── processed/      # cleaned data produced by code in src/
├── notebooks/
│   └── hospital_charges_prediction.ipynb
├── src/insurance_charges_prediction/
│   ├── __init__.py
│   ├── config.py       # shared constants: paths, random seed, split size
│   ├── data_loader.py  # reads data/raw, returns a cleaned DataFrame
│   ├── features.py     # feature engineering, shared by training and inference
│   ├── train.py        # fits the model, saves it to models/
│   └── evaluate.py     # RMSE/R², residual plots -> outputs/figures
├── models/              # trained .pkl/.joblib — gitignored
├── tests/               # pytest, files named test_*.py
└── outputs/figures/     # saved plots (small enough to commit)
```

Key conventions from the playbook:
- Production logic belongs in `src/insurance_charges_prediction/`, importable via
  `pip install -e .` (editable install from `pyproject.toml`). Notebooks are for exploration only —
  they should import from the package, not redefine logic.
- `data/raw/` is never hand-edited; `data/processed/` is regenerable from `data/raw/` + code in `src/`.
- Model binaries (`models/*.pkl`) and raw data are gitignored, not committed.
- Commit in small, descriptive increments rather than one large dump.

## Commands

No dependencies are installed yet. Once `pyproject.toml` exists, the expected workflow (per the
playbook) is:

```powershell
# install the project in editable mode (reads pyproject.toml)
pip install -e .

# run the notebook
jupyter lab      # or: jupyter notebook

# run tests (once tests/ exists)
pytest
pytest tests/test_data_loader.py -k some_case   # single test
```

Minimum dependencies implied by the brief: `pandas`, `numpy`, `scikit-learn`, `matplotlib` (and/or
`seaborn` for the EDA plots), `jupyter`.

This is not yet a git repository — run `git init` before making commits, and write `.gitignore`
(covering `__pycache__/`, `.venv/`, `.idea/`, `data/raw/*`, `models/*.pkl`, `*.ipynb_checkpoints/`)
before the first commit, per the playbook.