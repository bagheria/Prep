import pandas as pd
from pathlib import Path, PurePath


# %%
def get_path(*folders, filename):
    """
    Takes a filename as input (string). Returns path to file.
    """
    filepath = PurePath(Path.cwd()).joinpath(*folders, filename)
    return(filepath)


# %%
def get_path_context(filename):
    """
    Takes a filename as input (string).
    Returns path to file. Path is preceded by "file:\\"
    """
    filepath = Path.cwd() / "negation" / "KB" / "lexicon" / filename
    filepath = "file:\\" + str(filepath)
    return(filepath)


# %%
def import_excel(filename):
    """
    Takes a filename as input (string). Imports it from 'negation/data' folder.
    """
    filepath = Path.cwd() / "negation" / "data" / filename
    df = pd.read_excel(filepath)
    return(df)


def import_vars(filename):
    """
    Takes a filename as input (string). Imports it from 'negation/data' folder.
    """
    filepath = Path.cwd() / "negation" / "kb" / filename
    df = pd.read_excel(filepath)
    return(df)


def import_excel2(filepath):
    """
    Takes a filepath as input (use get_path()).
    """
    df = pd.read_excel(filepath)
    return(df)


# %%
def export_excel(df, filename):
    filepath = Path.cwd() / "negation" / "output" / filename
    df.to_excel(filepath, index=False)
    print(f"Excel file '{filename}' was created in {filepath}")


def df_dict_hack(master_dict):
    # Write function that appends every item to a dataframe
    # and returns the dataframe eventually but
    # if a dictionary is among the items, this should be included 
    # in the dataframe, and the dataframe should be expanded accordingly
    
    # For every subdict in a dict, make a row per subdict, and copy dict values
    # to every row
    subdicts = []
    for value in master_dict.value():
        if isinstance(value, dict()):
            subdicts.append(value)
    
    df = pd.DataFrame()

    for j in range(10):
        df = df.append({'key_%s'%random.choice('abcde'): j}, ignore_index=True)
    
    # for key, value in dictionary.items():
    #     insertion = pd.Series(data=value, name=key)
    #     df.insert(0, insertion.name, insertion, True)

    return(df)

def df_reorder_cols(df, contains_str, pos):
    if pos != "first" or "last":
        raise Exception("'pos' argument should be 'first' or 'last'") 
   
    # identify column types:
    all_cols = df.columns.values
    spec_cols = [col for col in all_cols if contains_str in col]
    other_cols = [col for col in all_cols if contains_str not in col]

    # change column order:
    if pos == "last":
        return(df.reindex(columns=other_cols + spec_cols))
    else:
        return(df.reindex(columns=spec_cols + other_cols))