"""
This module contains logic for reading data and returning a clean data frame.

Inspect: column names, missing values and dtypes. Check for trailing spaces in
column names and formating issues in the data.
"""

import pandas as pd

from insurance_charges_prediction.config import RAW_DATA_FILE

def load_raw_data(path=RAW_DATA_FILE) -> pd.DataFrame:
    df = pd.read_csv(path)
    # Strip trailing and leading whitespace from column names
    df.columns = df.columns.str.strip()
    return df

if __name__ == "__main__":
    # `python -m insurance_charges_prediction.load_data` -> quick sanity check from the CLI
    df = load_raw_data()
    print(df.shape)
    print(df.head())
