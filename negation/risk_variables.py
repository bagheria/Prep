import re


# %% Extract binary values from modifier column
def get_bin_output(mod, row_number):
    no_neg_rank = 1
    if isinstance(mod, str):
        if mod == "['definite_negated_existence']":
            rank = -2
        elif mod == "['probable_negated_existence']":
            rank = -1
        elif mod == "['ambivalent_existence']":
            rank = 0
        elif mod == "['pseudoneg']":
            rank = 0
        elif mod == "['probable_existence']":
            rank = 1
        elif mod == "['definite_existence']":
            rank = 2
        else:
            raise Exception(
                "Error in scoring the negation tag of binary",
                "MAGGIC variables.",
                f"Modifier for row {row_number} was '{mod}' and is string,",
                "but is not recognized as valid negation tag")

    else:
        rank = no_neg_rank
    return(rank)


# Variabel Ejection Fraction
def vef(phrase):
    pattern = r"\d+"
    value = re.search(pattern, phrase).group()
    return(value)


# Systolic Blood Pressure
def sbp(phrase):
    pattern = r"(\d{2,3}(?=/\d{2,3}))"
    value = re.search(pattern, phrase).group()
    return(value)
