import pandas as pd

from sklearn.preprocessing import OneHotEncoder

# Function for encoding categorical variables in dataset.
def encode_categoricals(df, cols=("Provider State", "DRG Definition")) -> pd.DataFrame:
    encoder = OneHotEncoder(drop="first", sparse_output=False, handle_unknown="ignore")
    encoded_array = encoder.fit_transform(df[["Provider State", "DRG Definition"]])
    encoded_cols = encoder.get_feature_names_out(["Provider State", "DRG Definition"])
    encoded_df = pd.DataFrame(encoded_array, columns=encoded_cols, index=df.index)
    return encoded_df

# Function for selecting the dependent and independent variables.
def build_X_y(df, encoded_df) -> tuple[pd.DataFrame, pd.Series]:
    """
    :param df: The original DataFrame containing the data.
    :param encoded_df: The encoded DataFrame
    :return: tuple of (X, y) — X is a DataFrame of independent variables,
             y is a Series containing the target variable
    """
    X = pd.concat([df["Total Discharges"], encoded_df], axis=1)
    y = df["Average Covered Charges"]
    return X, y