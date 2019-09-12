# %%
import pandas as pd
from pathlib import Path
# import yaml
from negation.preprocess_neg import import_excel


# %%
def panda_to_yaml(filename, obj_input):
    """Converts and exports a panda dataframe lexicon into a yaml file.
    This can be used by pyContextNLP.
    Use filename with .yml extension"""

    filepath = Path.cwd() / "negation" / "output" / filename

    open(filepath, "w")

    with open(filepath, "a") as stream:
        # Each row represents one document in the yaml file
        for row_index in obj_input.index:
            # Each column represents one object per document in yaml file
            for col in obj_input.columns:
                # Value corresponding to curent document and object
                value = obj_input.at[row_index, col]
                if pd.isna(value):
                    # If no value is present, we write '' as value to object
                    stream.write("{}: ''\n".format(col))

                else:
                    stream.write("{}: {}\n".format(col, value))
            # Add yaml document separator followed by "\n"
            stream.write("---\n")


# %%
def gen_regex(df):
    """
    Function to transform dataframe with synonyms into regex patterns.
    First column should be literals, subsequent columns should be synonyms
    """
    # Save synonym columns in list, to loop over synonyms per target
    columns = []
    for column in df.columns:
        columns.append(column)
    # Remove first string, because this is the literal, no synonym
    del(columns[0])

    # Initialize new DataFrame to store new values:
    # Two columns: literal and  regex
    new_df = pd.DataFrame(columns=["literal", "regex"])
    new_df_index = 0

    # Generate the regex and literal strings per row of the input df
    for row_index in df.index:
        # Literal can be copied directly
        lit = df.iat[row_index, 0]

        synonyms = []
        # Synonyms extracted from the columns
        for syn_col in columns:
            synonym = df.at[row_index, syn_col]
            # If particular cell is empty, don't append to list
            if pd.isna(synonym):
                # print("empty string")
                pass
            else:
                synonyms.append(synonym)

        # Generate regex pattern including all synonyms:
        regex = ""
        i = 0
        n = len(synonyms)
        for synonym in synonyms:
            i += 1
            # If current loop is last synonym of list:
            if i == n:
                # Don't add another | <or> operator to regex pattern
                addition = f"({synonym})"
            else:
                # Include '|' to pattern, for following additions
                addition = f"({synonym})|"

            regex = regex + addition
        # Add values to new row in df
        new_df.loc[new_df_index] = pd.Series({"literal": lit, "regex": regex})
        new_df_index += 1
    return(new_df)


# %%
raw_targets = import_excel("target_test1.xlsx")
regex_df = gen_regex(raw_targets)
print(regex_df)

# # %%
# # nl_mod comes from lexicon_to_df.py
# obj_input = nl_mod
# # replace all empty values with NaN
# obj_input = obj_input.replace("", np.nan, regex=False)

# panda_to_yaml("output.yml", obj_input)

# %%
