# %%
import re
import numpy as np


# %% Remove empty rows:
def drop_empty(df):
    new_df = df.dropna(axis=0)
    print("\nIndexes removed from data because of missing data:\n",
          set(df.index).symmetric_difference(set(new_df.index)))
    return(new_df)


# %% Check data:
def check_data(df):
    if len(df.columns) != 2:
        raise Exception("Provided data contains more than 2 columns")

    if df.columns.values.tolist() != ['record', 'text']:
        raise Exception(
            "Provided data does not contain columns named 'record' and 'text'")

    if df["record"].dtype != np.int64:
        raise Exception(
            "Record column has no numeric values")

    if df["text"].dtype != object:
        raise Exception(
            "Text column has no object type: strings")
    print("Checked data input. No problems found.")


# %%
string1 = "Zin 1 zin zin..Zin twee zin."
string2 = "Zin 1 zin zin.. .. .Zin twee zin."


# # %% Remove multiple dot-whitespace combinations
# # Change it into one dot-whitespace
# def cor_dot_whitesp1(string):
#     # First, concatentate dots separated by whitespaces:
#     # two dots separated by whitespace:
#     pat = r"\.\s\.{1,5}"
#     string = re.sub(pat, ".", string)
#     print("string1:", string)
#     # Then, simplify multiple dots and whitespaces
#     # multiple dots with possible multiple whitespaces:
#     pat = r"\.{1,4}\s{0,5}"
#     string = re.sub(pat, ". ", string)
#     print("string2:", string)
#     return(string)

# %%
def cor_dot_whitesp(string):
    # First, concatentate multiple dots to single dots
    pat = r"\.{2,5}"
    string = re.sub(pat, ".", string)
    # print("string1:", string)
    # Then, simplify dot and whitespace combinations
    pat = r"(\.(\s{0,5})){1,5}"
    string = re.sub(pat, ". ", string)
    # print("string2:", string)
    return(string)


# %%
cor_dot_whitesp(string1)
cor_dot_whitesp(string2)

# %% ASCI characters:
import unicodedata
string = u"ëáí–μ"
unicodedata.normalize('NFKD', string).encode('ascii', 'ignore')


def cor_unicode(string):
    # correct utf8 to asci

    # Check if type is string again
    return(string)


# %%
def preproc_text(df):
    for i in df.index:
        # print(df.text[i])
        # print(type(df.text[i]))
        cor1 = cor_dot_whitesp(df.text[i])
        cor2 = cor_unicode(cor1)
        df.at[i, "text"] = cor2
    return(df)


# %%
