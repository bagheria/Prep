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

# Synonyms
vef1_syn = r"(LVEF|EF|ejectiefractie|linkerventrikel\sejectiefractie|" \
            r"linkerventrikelejectiefractie|lv\sejectiefractie|" \
            r"linker\sventrikel\sejectie\sfractie|kamerfunctie)"
# Lookahead no alphabetic character
# Used to prevent catching "efficient" with 'ef' synonym
# No word boundary used here, since value can be next to synonym
# without whitespace separating them
vef1_aggr = r"(?![a-z])"
vef2_aggr = r"()"
# Spacer between synonym and value
vef1_spacer = r"(.{0,20}?)"
# Value: 2 digits
vef1_value = r"\d{2}"
# Lookahead no digit after two digit value:
# To prevent capture of other values such as years
vef1_ahead = r"(?!\d)"
# Lookbehind no digit or komma before 2 digit value:
# To prevent caputure of other values such as years
# and decimal part of percentages
vef1_behind = r"(?<=([^,\d])(\d{2}))"

vef_regex1 = (r"\b" + vef1_syn + vef1_aggr + vef1_spacer +
    vef1_value + vef1_ahead + vef1_behind)

# Synonym folowing percentage
# With margin of 10 characters after percentage
vef_regex2 = \
    r"\d{2}(?<=\D(\d){2})\D(.{0,20})[^a-z]" \
    r"(LVEF|EF|ejectiefractie|linkerventrikel\sejectiefractie|" \
    r"linkerventrikelejectiefractie|lv\sejectiefractie|" \
    r"linker\sventrikel\sejectie\sfractie|kamerfunctie)\b"

vef_regex2 = (vef1_value + vef1_ahead + vef1_behind +
    r"(|" + vef1_spacer + r"\b)" + vef1_syn + r"\b")
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
