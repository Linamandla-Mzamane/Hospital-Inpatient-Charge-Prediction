"""
This module cleans the DataFrame:

Strips the dollar signs from the columns with money entrys.
Converts the values stored into numeric values, deals with the
commas in the values and deals with trailing spaces in column names.
"""

import pandas as pd

# Function for dropping identifier columns
def drop_cols(df: pd.DataFrame) -> pd.DataFrame:
    cols_to_drop = ["Provider Id",
                    "Provider Name",
                    "Provider Street Address",
                    "Provider Zip Code"]

    df = df.drop(columns=cols_to_drop)
    return df

# Function for cleaning currency columns
def remove_dol_symols(value: str) -> str:
    """
    :param value: A money amount from the dataframe
    :return: A string with no dollar signs or comma separators
    """
    return value.replace("$", "").replace(",", "")


# Function for converting strings to numeric values
def convert_to_numeric(value: str) -> float:
    """
    :param value: A string representing an amount of money
    :return: A numeric version of that string
    """
    return float(value)

# Function for cleaning data
def clean_raw_data(df: pd.DataFrame) -> pd.DataFrame:
    for col in ["Average Covered Charges",
                "Average Total Payments",
                "Average Medicare Payments"]:

        df[col] = df[col].apply(remove_dol_symols)
        df[col] = df[col].apply(convert_to_numeric)
    return df

