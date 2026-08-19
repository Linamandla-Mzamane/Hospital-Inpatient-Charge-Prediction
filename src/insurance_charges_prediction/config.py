"""
Central place for constants and paths.

Every module imports from here instead of hardcoding paths.
This is done so that I only need to edit this file if I ever
move parts of the project or rename them.
"""

from pathlib import Path

# This module is two levels down from the root. (src/insurance_charges_prediction/config.py -> project root)
ROOT_DIR = Path(__file__).resolve().parents[2]

# Data paths
DATA_DIR = ROOT_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

# Data files
RAW_DATA_FILE = RAW_DATA_DIR / "inpatientCharges.csv"
CLEANED_DATA_FILE = PROCESSED_DATA_DIR / "cleanedInpatientCharges.csv"

# Constant variable for model instantiation
RANDOM_STATE = 4
TEST_SIZE = 0.2