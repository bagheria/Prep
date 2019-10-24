# %%
import re
import numpy as np
import unidecode


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

# %% Convert non-ASCII characters to ASCII
def convert_ascii(string):
    string = unidecode.unidecode(string)
    return(string)


# %%
def preproc_text(df, dot = True, ASCII = False):
    """Function to preprocess the patient records for interpunction
    (dots and whitespaces) and convert to ASCII (replace special characters)
     Args:
        df (pandas dataframe): Patient records in pandas dataframe
        dot (Bool): If true, will preprocess dots and whitespaces
        ASCII (Bool): If true, will convert special characters to ASCII

    Returns:
        df: Returns processed dataframe
    """
    if not dot | ASCII:
        print("No preprocessing. Set dot or ASCII args to True")
        return
    for i in df.index:
        # print(df.text[i])
        # print(type(df.text[i]))
        string = df.text[i]
        if dot:
            string = cor_dot_whitesp(string)
        if ASCII:
            string = convert_ascii(string)
        df.at[i, "text"] = string
    print("Preprocessing done:")
    if dot:
        print("Whitespaces and dots are preprocessed")
    if ASCII:
        print("Special characters are converted to ASCII")
    return(df)



