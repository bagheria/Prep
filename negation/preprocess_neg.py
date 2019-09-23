import pandas as pd
from pathlib import Path


def get_path(filename):
    """
    Takes a filename as input (string). Returns path to file.
    """
    filepath = Path.cwd() / "negation" / "data" / filename
    return(filepath)


def get_path_context(filename):
    """
    Takes a filename as input (string).
    Returns path to file. Path is preceded by "file:\\"
    """
    filepath = Path.cwd() / "negation" / "data" / filename
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


def import_excel2(folder, filename):
    """
    Takes a filename as input (string). Imports it from 'negation/data' folder.
    """
    filepath = Path.cwd() / "negation" / folder / filename
    df = pd.read_excel(filepath)
    return(df)


# %%
def export_excel(df, filename):
    filepath = Path.cwd() / "negation" / "output" / filename
    df.to_excel(filepath, index=False)
    print(f"Excel file '{filename}' was created in {filepath}")
