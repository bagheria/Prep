# %%
import pandas as pd
from pathlib import Path
import yaml


# %%
def yaml_to_panda(filename):
    """Converts a yaml context lexicon to a pandas dataframe
    """
    filepath = Path.cwd() / "negation" / "data" / filename
    with open(filepath) as file:
        yaml_file = yaml.load_all(file, Loader=yaml.SafeLoader)
        i = 0
        for doc in yaml_file:
            if i == 0:
                yaml_panda = pd.DataFrame(data=doc, index=[i])
            else:
                new_row = pd.DataFrame(data=doc, index=[i])
                yaml_panda = pd.concat([yaml_panda, new_row])
            i = i + 1
    return(yaml_panda)


# %%
def panda_to_yaml(filepath, obj_input):
    """Converts and exports a panda dataframe lexicon into a yaml file.
    This can be used by pyContextNLP.
    """

    # Create file to write  to
    open(filepath, "w")

    with open(filepath, "a") as stream:
        # initialize i, to skip yaml document seperator for first row
        i = True
        # Each row represents one document in the yaml file
        for row_index in obj_input.index:
            # If not first row in file writing:
            if not i:
                # Add yaml document separator followed by "\n"
                stream.write("---\n")
            # If first row for file writing:
            if i:
                # Skip yaml doc seperator and reset i
                i = False
            # Each column represents one object per document in yaml file
            for col in obj_input.columns:
                # Value corresponding to curent document and object
                value = obj_input.at[row_index, col]
                if pd.isna(value):
                    # If no value is present, we write '' as value to object
                    stream.write("{}: ''\n".format(col))

                else:
                    stream.write("{}: {}\n".format(col, value))


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
    # Remove category and literal, because these don't contain synonyms
    columns.remove("category")
    columns.remove("literal")

    # Initialize new DataFrame to store new values:
    # Two columns: literal and  regex
    new_df = pd.DataFrame(columns=["Type", "Lex", "Regex"])
    new_df_index = 0

    # Generate the regex and literal strings per row of the input df
    for row_index in df.index:
        # Literal can be copied directly
        lit = df.at[row_index, "literal"]
        cat = df.at[row_index, "category"]

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

        # Add word boundary class around regex pattern:
        regex = r"\b" + regex + r"\b"

        # Add values to new row in df
        new_df.loc[new_df_index] = \
            pd.Series({"Type": cat, "Lex": lit, "Regex": regex})
        new_df_index += 1
    return(new_df)
