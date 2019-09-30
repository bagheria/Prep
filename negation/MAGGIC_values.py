# %% Imports:
from negation import preprocess_neg
import pandas as pd
import re
import collections



def join_maggic(mag_var_df, context_df):
    # Get rid of ['xx'] quotes in category column:
    for i in context_df.index:
        replacement = context_df.at[i, "category"]
        replacement = replacement.strip("'][")
        context_df.at[i, "variable"] = replacement

    # %% Join context df and MAGGIC variable df
    df = pd.merge(mag_var_df, context_df, on='variable', how="right")
    return(df)


# %% Extract variabel ejection fraction values
def get_vef_output(df):
    rows = list(df.index.values)
    new_df = df
    for row in rows:
        if (df.at[row, "variable"]) == "vef":
            string = df.at[row, "phrase"]
            # Regex pattern to get value
            value = re.search(r"\d+", string).group()
            print(type(value))
            new_df.at[row, "value"] = value

    return(new_df)


# %% Extract systolic blood pressure values
def get_sbp_output(df):
    rows = list(df.index.values)
    new_df = df
    for row in rows:
        if (df.at[row, "variable"]) == "sbp":
            string = df.at[row, "phrase"]
            # Regex pattern to get value
            pattern = r"(\d{2,3}(?=/\d{2,3}))"
            value = re.search(pattern, string).group()
            print(type(value))
            new_df.at[row, "value"] = value

    return(new_df)


# %% Extract binary values from modifier column
def get_bin_output(df):
    rows = list(df.index.values)
    new_df = df
    for row in rows:
        if (df.at[row, "type"]) == "binary":
            mod = df.at[row, "modifier"]

            new_df.at[row, "value"] = mod

    return(new_df)
# %% Extract factor values


# %% Combine non-textmining values


# %% Risk calculation

def get_values(df):
    df = get_vef_output(df)
    df = get_sbp_output(df)

    return(df)


def get_risk(df):
    # Get list of record numbers
    records = df.record.unique()
    # Initialize risk score dataframe
    risk_df = pd.DataFrame(columns=["record", "score"])
    index = 0

    # Calculate risk scores for every record
    for i in records:
        df_record = df[df.record == i]
        risk_score = calc_risk_score(df_record)
        risk_df.loc[index] = pd.Series({"record": i, "score": risk_score})
        index += 1


# %% Risk score formula:
def calc_risk_score(df):
    values = df[df.variable == "vef"].value
    index = values.index
    vector = []
    for i in index:
        vector.append(values[i])

    if len(vector) == 1:
        value = vector[0]
    elif len(vector) == 0:
        value = ""
    else:
        # If multiple options for value:
        counts = collections.Counter(vector).most_common()
        # Take the most frequent one, of second frequent one is less frequent
        if counts[0][1] != counts[1][1]:
            value = counts[0][0]
        else:
            print("Multiple options for VEF value in:\n", df)




    return(value)


def get_value(variable):


def test():
    print(abc)
    return()