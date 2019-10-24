# %%
import negation.utils as utils
import negation.lexicon as lexicon
# import re
import pandas as pd

# %% Load lexicon from Excel
maggic1_path = utils.get_path(
    "Negation", "KB", filename="MAGGIC targets.xlsx")
maggic1 = utils.import_excel2(maggic1_path)
print(maggic1)

# %% Generate regex pattern for synonyms:
maggic2 = lexicon.gen_regex(maggic1)
# print(maggic2)
# print(maggic2.columns)

# %% SBP:
# Captures a 2 or 3 digit number

# Synonym preceding sbp:
sbp_regex1 = \
    r"\b(rr|mmhg|bloeddruk|tensie|" \
    r"riva-rocci|mm\shg|systole|systolisch)" \
    r"(.{0,20})(\d{2,3})/(\d{2})"

# sbp preceding synonym:
sbp_regex2 = \
    r"(\d{2,3})/(\d{2})(.{0,20})" \
    r"(rr|mmhg|bloeddruk|tensie|" \
    r"riva-rocci|mm\shg|systole|systolisch)\b"

# Add SBP row to MAGGIC dataframe:
maggic2.loc[len(maggic2.index)] = \
    pd.Series({"Type": "sbp", "Lex": "Systolic Blood Pressure 1",
              "Regex": sbp_regex1})
maggic2.loc[len(maggic2.index)] = \
    pd.Series({"Type": "sbp", "Lex": "Systolic Blood Pressure 2",
              "Regex": sbp_regex2})

# %% Variable Ejection Fraction

# Synonym preceding percentage
# With a margin of 10 characters between synonym and value
vef_regex1 = \
    r"\b(LVEF|EF|ejectiefractie|linkerventrikel\sejectiefractie|" \
    r"linkerventrikelejectiefractie|lv\sejectiefractie|" \
    r"linker\sventrikel\sejectie\sfractie|kamerfunctie)" \
    r"(.{0,20})\d{2}"

# Synonym folowing percentage
# With margin of 10 characters after percentage
vef_regex2 = \
    r"\d{2}%?.{0,20}" \
    r"(LVEF|EF|ejectiefractie|linkerventrikel\sejectiefractie|" \
    r"linkerventrikelejectiefractie|lv\sejectiefractie|" \
    r"linker\sventrikel\sejectie\sfractie|kamerfunctie)\b"

# Testing:
# # first synonym:
# first_syn_string = "Blabla blabla. Bla bla EF is 45 % blabla. blabla"
# print(first_syn_string)
# print(vef_regex1)
# print(re.search(pattern=vef_regex1, string=first_syn_string))

# # First value:
# first_val_string = "test test. 23% vind niet linkerventrikel ejectiefractie"
# print(first_val_string)
# print(vef_regex2)
# print(re.search(pattern=vef_regex2, string=first_val_string))

# Add VEF row to MAGGIC dataframe
maggic2.loc[len(maggic2.index)] = \
    pd.Series({"Type": "vef", "Lex": "Variabel Ejection Fraction 1",
              "Regex": vef_regex1})
maggic2.loc[len(maggic2.index)] = \
    pd.Series({"Type": "vef", "Lex": "Variabel Ejection Fraction 2",
              "Regex": vef_regex2})

# %% Add column with calc = "MAGGIC"
# maggic2["calc"] = "MAGGIC"
maggic2["Direction"] = "''"
maggic2["Comments"] = "''"

# %% Convert pandas to yaml format
yaml_path = utils.get_path(
    "Negation", "KB", "lexicon", filename="MAGGIC2.yml")
lexicon.panda_to_yaml(yaml_path, maggic2)

# # %%
# print(re.search(pattern="a.{1,3}bc", string="ddappbcddef"))

# %%
