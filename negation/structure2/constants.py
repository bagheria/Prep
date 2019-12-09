## Modifiers:

mod_types = ["negation", "date", "temporality", "examination"]

examination_mods = ["indication", "hypothetical"]
negation_mods = [
"definite_negated_existence", "probable_negated_existence",
"probable_existence", "definite_existence", "ambivalent_existence",
"pseudoneg"]
date_mods = ["date"]
temporality_mods = ["historical", "future", "acute"]

mod_type_dict = {
    "neg" : negation_mods,
    "date" : date_mods,
    "exam" : examination_mods,
    "temp" : temporality_mods
}
## Variables / risk factors:
var_types = ["numeric", "factorial", "binary"]

numeric_vars = ["age", "vef", "sbp", "bmi", "creatinine"]
factorial_vars = ["nyha"]
binary_vars = ["gender", "current smoker", "diabetes", "copd", 
"heart failure", "beta blocker", "acei"]

var_type_dict = {
    "numeric" : numeric_vars,
    "factorial" : factorial_vars,
    "binary" : binary_vars
}

## Calculators:
calculators = ["maggic"]

# Per calculator
maggic_vars_incl = ["vef", "sbp", "nyha", "current smoker", "diabetes", "copd"]
maggic_vars_excl = ["age", "bmi", "creatinine", "gender", "heart failure", "beta blocker", "acei"]

vars_incl = {"maggic" : maggic_vars_incl}
vars_excl = {"maggic" : maggic_vars_excl}

def add_ls(ls):
    result = []
    for i in ls.values():
        result = result + i
    return(result)
vars_comb = add_ls(vars_incl) + add_ls(vars_excl)