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
    "negation" : negation_mods,
    "date" : date_mods,
    "examination" : examination_mods,
    "temporality" : temporality_mods
}
## Variables / risk factors:

# Types
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

# Factors
nyha_factors = [("NYHA class I", 1), ("NYHA class II", 2), ("NYHA class III", 3), ("NYHA class IV", 4)]

factors = {
    "nyha" : nyha_factors
}

## Calculators:
calculators = ["maggic"]

# Per calculator
maggic_vars_incl = ["vef", "sbp", "nyha", "current smoker", "diabetes", "copd"]
maggic_vars_excl = ["age", "bmi", "creatinine", "gender", "heart failure", "beta blocker", "acei"]

vars_incl = {"maggic" : maggic_vars_incl}
vars_excl = {"maggic" : maggic_vars_excl}

def add_ls(ls):
    # Add up all values from multiple dictionaries into 1 flat list
    result = []
    for i in ls.values():
        result = result + i
    return(result)
vars_comb = add_ls(vars_incl) + add_ls(vars_excl)