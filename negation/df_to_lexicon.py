import pandas as pd
from pathlib import Path
# import yaml
import numpy as np


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


# nl_mod comes from lexicon_to_df.py
obj_input = nl_mod
# replace all empty values with NaN
obj_input = obj_input.replace("", np.nan, regex=False)

panda_to_yaml("output.yml", obj_input)
