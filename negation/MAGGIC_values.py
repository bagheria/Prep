# %% Imports:
from negation import preprocess_neg
import pandas as pd


def join_maggic(filename_vars, context_df):
    # %% load file
    mag_var_df = preprocess_neg.import_excel(filename_vars)

    # Get rid of ['xx'] quotes in category column:
    for i in context_df.index:
        replacement = context_df.at[i, "category"]
        replacement = replacement.strip("'][")
        context_df.at[i, "variable"] = replacement

    # %% Join context df and MAGGIC variable df
    df = pd.merge(mag_var_df, context_df, on='variable', how="right")
    return(df)


# %% Extract numeric values
def get_numeric_output(df):
    df_filter = df[df["type"] == "numeric"]
    rows = list(df_filter.index.values)
    for row in rows:
        string = df.at[row, "phrase"]
        # Regex pattern to get value
        value = 


# %% Extract binary values


# %% Extract factor values


# %% Combine non-textmining values


# %% Risk calculation
