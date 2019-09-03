import pandas as pd
from pathlib import Path

# filename = "test_data1.xlsx"

# print("Current working directory:", Path.cwd())

# filepath = Path.cwd() / "negation" / "data" / filename
# print(filepath)
# df = pd.read_excel(filepath)
# print(df)

# test_record = df.tekst[0]
# print(test_record)


def import_excel(filename):
    filepath = Path.cwd() / "negation" / "data" / filename
    df = pd.read_excel(filepath)
    return(df)


test_df = import_excel("test_data1.xlsx")
print(test_df)