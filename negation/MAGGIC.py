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

# SBP synonyms:
sbp_syn = r"(rr|mmhg|bloeddruk|tensie|" \
    r"riva-rocci|mm\shg|systole|systolisch)" 

# Spacer between synonym and value
# Non greedy so only closed value will be captured
sbp_spacer = r"(.{0,20}?)"

# Value:
# e.g. 120/80 or 80/60 
sbp_value = r"(\d{2,3})/(\d{2})"

# Lookahead: 
# no slash after pattern: To prevent date notations to be captured
# no digit after pattern: To prevent longer values to be captured
sbp_ahead = r"(?!(/|\d))"

# Pattern compiling:
# First synonym, then value:
sbp_regex1 = (r"\b" + sbp_syn + r"(|" + r"\b" + sbp_spacer + r")"
    + sbp_value + sbp_ahead)

# First value, then synonym:
sbp_regex2 = (sbp_value + sbp_ahead + r"(|" + sbp_spacer + r"\b)" +
    sbp_syn + r"\b")

# First syn, than value, then syn again:
# With PyConTextNLP will only keep this catch,
# Preventing multiple captures of same value
sbp_regex3 = (sbp_regex1 + r"(|" + sbp_spacer + r"\b)" +
    sbp_syn + r"\b")

# Old:
# Synonym preceding sbp:
# sbp_regex1 = \
#     r"\b(rr|mmhg|bloeddruk|tensie|" \
#     r"riva-rocci|mm\shg|systole|systolisch)" \
#     r"(.{0,20})(\d{2,3})/(\d{2})"

# # sbp preceding synonym:
# sbp_regex2 = \
#     r"(\d{2,3})/(\d{2})(.{0,20})" \
#     r"(rr|mmhg|bloeddruk|tensie|" \
#     r"riva-rocci|mm\shg|systole|systolisch)\b"

# Add SBP row to MAGGIC dataframe:
maggic2.loc[len(maggic2.index)] = \
    pd.Series({"Type": "sbp", "Lex": "Systolic Blood Pressure 1",
              "Regex": sbp_regex1})
maggic2.loc[len(maggic2.index)] = \
    pd.Series({"Type": "sbp", "Lex": "Systolic Blood Pressure 2",
              "Regex": sbp_regex2})
maggic2.loc[len(maggic2.index)] = \
    pd.Series({"Type": "sbp", "Lex": "Systolic Blood Pressure 3",
              "Regex": sbp_regex3})

# %% Variable Ejection Fraction

# Synonyms
vef_syn = r"(LVEF|EF|ejectiefractie|linkerventrikel\sejectiefractie|" \
            r"linkerventrikelejectiefractie|lv\sejectiefractie|" \
            r"linker\sventrikel\sejectie\sfractie|kamerfunctie)"

# Lookahead no alphabetic character
# Used to prevent catching "efficient" with 'ef' synonym
# No word boundary used here, since value can be next to synonym
# without whitespace separating them
# vef_aggr = r"(?![a-z])"
# This is now fixed better by a OR pattern in the compiling code. 
# Syn and val must be directly next to each other (no whitespace) OR
# The spacer must be in between, with word boundary flanking the synonym

# Spacer between synonym and value
# Non greedy: so only closed value will be captured
vef_spacer = r"(\D{0,20}?)"
vef_range_spacer = r"(.{0,20}?)"

# Before value exlcusion:
# Alternative for vef_behind
# vef_before = r"[^,\d]"
# Currently not used

# Value: 2 digits
vef_value = r"\d{2}"

# Value: range of 2 values
vef_range_sep = r"(\s?)-(\s?)"

# Lookahead no digit after two digit value:
# To prevent capture of other values such as years
vef_ahead = r"(?!\d)"

# Lookbehind no digit or komma before 2 digit value:
# To prevent caputure of other values such as years
# and decimal part of percentages
vef_behind = r"(?<=([^,\d])(\d{2}))"

# regex pattern compiling:
# First synonym, then value:
vef_regex1 = (r"\b" + vef_syn + r"(|" + r"\b" + vef_spacer + r")"
    + vef_value + vef_ahead + vef_behind + r"(%?)")

# First value, then synonym:
vef_regex2 = (vef_value + vef_ahead + vef_behind + r"(%?)"
    r"(|" + vef_spacer + r"\b)" + vef_syn + r"\b")

# First syn, than value, then syn again:
# With PyConTextNLP will only keep this catch,
# Preventing multiple captures of same value
vef_regex3 = (vef_regex1 + r"(|" + vef_spacer + r"\b)" +
    vef_syn + r"\b")

# Pattern compiling of range vef values
vef_range_reg1 = (r"\b" + vef_syn + r"(|" + r"\b" + vef_range_spacer + r")"
    + vef_value + vef_behind + r"(%?)" + vef_range_sep + vef_value + vef_ahead + r"(%?)")

vef_range_reg2 = (vef_value + vef_behind + r"(%?)"+ vef_range_sep + vef_value + 
    vef_ahead + r"(%?)" + r"(|" + vef_range_spacer + r"\b)" + vef_syn + r"\b")

vef_range_reg3 = (vef_range_reg1 + r"(|" + vef_range_spacer + r"\b)" +
    vef_syn + r"\b")

# Old:
# vef_regex1 = (r"\b" + vef_syn + vef_aggr + vef_spacer +
#     vef_value + vef_ahead + vef_behind)


# Add VEF row to MAGGIC dataframe
maggic2.loc[len(maggic2.index)] = \
    pd.Series({"Type": "vef", "Lex": "Variabel Ejection Fraction 1",
              "Regex": vef_regex1})
maggic2.loc[len(maggic2.index)] = \
    pd.Series({"Type": "vef", "Lex": "Variabel Ejection Fraction 2",
              "Regex": vef_regex2})
maggic2.loc[len(maggic2.index)] = \
    pd.Series({"Type": "vef", "Lex": "Variabel Ejection Fraction 3",
              "Regex": vef_regex3})
maggic2.loc[len(maggic2.index)] = \
    pd.Series({"Type": "vef", "Lex": "Variabel Ejection Fraction Range 1",
              "Regex": vef_range_reg1})
maggic2.loc[len(maggic2.index)] = \
    pd.Series({"Type": "vef", "Lex": "Variabel Ejection Fraction Range 2",
              "Regex": vef_range_reg2})
maggic2.loc[len(maggic2.index)] = \
    pd.Series({"Type": "vef", "Lex": "Variabel Ejection Fraction Range 3",
              "Regex": vef_range_reg3})
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
