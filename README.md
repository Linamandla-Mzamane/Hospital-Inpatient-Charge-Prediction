# Hospital Inpatient Charges Prediction

A data-science portfolio project that models what U.S. hospitals charge for inpatient
procedures, using real CMS billing data. Covers the full pipeline: cleaning, exploratory
analysis, multiple linear regression, coefficient interpretation, a business-facing markup
metric, an alternate target, and a regularization comparison (Ridge/Lasso vs. OLS)..

## Dataset

**Hospital Charges for Inpatients** — U.S. Centers for Medicare & Medicaid Services (CMS)
billing data, ~163,000 rows, one row per hospital/DRG (diagnosis-related group). Key columns:
`DRG Definition` (~100 procedure/condition categories), `Provider State`, `Total Discharges`,
`Average Covered Charges` (what the hospital billed — the primary target), `Average Total
Payments`, and `Average Medicare Payments`.

Source: [Kaggle — speedoheck/inpatient-hospital-charges](https://www.kaggle.com/datasets/speedoheck/inpatient-hospital-charges)

## Project structure

```
├── data/
│   ├── raw/            # original CSV (gitignored, not committed)
│   └── processed/      # cleaned data written by the EDA notebook (gitignored)
├── notebooks/
│   ├── hospital_charges_eda.ipynb          # load, clean, explore
│   └── hospital_charges_prediction.ipynb   # encode, model, evaluate, interpret
├── src/insurance_charges_prediction/
│   ├── config.py       # shared paths, random seed, split size
│   ├── load_data.py    # reads data/raw, strips column whitespace
│   ├── clean_data.py   # currency cleaning, identifier-column dropping
│   └── features.py     # one-hot encoding, X/y assembly
└── pyproject.toml
```

The two notebooks are the deliverable. Production logic (loading, cleaning, feature
engineering) lives in the package under `src/` and is imported into the notebooks rather than
redefined inline.

## Setup

```powershell
# from the project root
pip install -e .

# place the raw CSV at data/raw/inpatientCharges.csv, then:
jupyter lab
```

Run `notebooks/hospital_charges_eda.ipynb` first — its last cell writes the cleaned dataset to
`data/processed/cleanedInpatientCharges.csv`, which `notebooks/hospital_charges_prediction.ipynb`
reads as its starting point.

## Key findings

- **Procedure type, not geography, is the dominant cost driver.** `DRG Definition` explains
  ~54% of the variance in `Average Covered Charges` (η²), about four times what `Provider
  State` explains (~14%). The regression's largest coefficients confirm this directly — the
  biggest positive effects are all high-acuity DRGs (e.g. Sepsis with mechanical ventilation,
  +$132,866 vs. the reference category).
- **A model on `Total Discharges` + one-hot `Provider State`/`DRG Definition` explains about
  67% of the variance in billed charges** (R² = 0.67, RMSE ≈ $20,022), and systematically
  underpredicts the most expensive cases — consistent with the heavily right-skewed target
  (skew ≈ 4.0).
- **Biggest dollar impact and biggest markup are different questions.** The DRGs with the
  largest charge-to-Medicare-payment ratio (Chest Pain, 6.2x; Dysequilibrium, 5.8x) are
  low-acuity, high-volume procedures — not the high-cost DRGs above. Sepsis, despite having
  the single largest dollar coefficient, ranks just 89th of 100 DRGs by ratio (3.9x).
- **Medicare's own reimbursement is far more predictable than what hospitals bill.** The same
  features predict `Average Medicare Payments` far better (R² = 0.88) than `Average Covered
  Charges` (R² = 0.67) — consistent with Medicare's formula-driven payments leaving hospitals
  more discretion in what they list as charges.
- **Regularization doesn't change the story here.** OLS, Ridge, and Lasso (fit on standardized
  features) land within 0.00001 of each other on R², and Lasso doesn't zero out a single one
  of 150 coefficients at default strength — not much evidence of overfitting to correct for.

**Recommendation:** payers should target contract negotiations and billing audits using the
DRG/state-level charge-to-Medicare-payment ratio rather than raw charge levels — it isolates
hospital pricing behavior on clinically comparable cases instead of reflecting legitimate
differences in patient severity.

## License

MIT — see [LICENSE.txt](LICENSE.txt).
