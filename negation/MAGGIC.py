# %%
import negation.preprocess_neg
import negation.lexicon


# %% Load lexicon from Excel
maggic1 = negation.preprocess_neg.import_excel("MAGGIC targets.xlsx")
print(maggic1)

# %% Generate regex pattern for synonyms:
maggic2 = negation.lexicon.gen_regex(maggic1)
print(maggic2)

# %% Add column with calc = "MAGGIC"
maggic2["calc"] = "MAGGIC"
# %% Convert pandas to yaml format
negation.lexicon.panda_to_yaml("MAGGIC.yml", maggic2)

# %% Manual numeric variables:
# Systolic blood pressure:

# Capture two numbers separated by
# a forward slash with 1 or 0 whitespace flanking the sbp:
sys = r"(?<=\s)\d{2,3}(?=/\d{2,3}\s?(aap))"
dias = r"/\d{2,3}"
prec = r"\s"
fol = r""
sbp_syns = r""
sbp_tot = r"(?<=)"

# capture the systolic blood pressure when noted in 120/80 format
# With possible whitespaces surounding the forward slash
sbp2 = r"(\d{2,3})(?=/(\d{2})"

# Variable Ejection Fraction
# Percentage:
perc = r"\s\d{2}%?\s"

# %%
