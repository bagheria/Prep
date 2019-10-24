# %% Imports:
# from negation import utils
import pandas as pd
# import re
import collections
import negation.risk_variables as risk_variables


def join_maggic(mag_var_df, context_df):
    
    # Get rid of ['xx'] quotes in category column:
    for i in context_df.index:
        replacement = context_df.at[i, "category"]
        replacement = replacement.strip("'][")
        context_df.at[i, "variable"] = replacement
    context_df = context_df.drop(columns=["category"])
    # %% Join context df and MAGGIC variable df
    df = pd.merge(mag_var_df, context_df, on='variable', how="right")
    return(df)


# %%
def get_maggic_output(df):
    # Initialize new columns
    df = df.assign(neg=None, value=None)

    row_indxs = list(df.index.values)
    for i in row_indxs:
        row = df.loc[i]

        # Do negation validation
        neg = risk_variables.get_bin_output(
            row.modifier, i)
        row.neg = neg

        # Do vef, sbp and nyha
        var = row.variable
        if var == "sbp":
            value = risk_variables.sbp(row.phrase)
            row.value = value
        elif var == "vef":
            value = risk_variables.vef(row.phrase)
            row.value = value
        # Put row back in dataframe
        df.loc[i] = row
    return(df)


# %% Risk calculation
def get_risk(df):
    # Get list of record numbers
    records = df.record.unique()
    # Initialize risk score dataframe
    risk_df = pd.DataFrame(columns=["record", "score"])
    index = 0

    # Calculate risk scores for every record
    for i in records:
        df_record = df[df.record == i]
        risk_score = calc_risk_score(df_record)
        risk_df.loc[index] = pd.Series({"record": i, "score": risk_score})
        index += 1


# %% Risk score formula:
def calc_risk_score(df):
    values = df[df.variable == "vef"].value
    index = values.index
    vector = []
    for i in index:
        vector.append(values[i])

    if len(vector) == 1:
        value = vector[0]
    elif len(vector) == 0:
        value = ""
    else:
        # If multiple options for value:
        counts = collections.Counter(vector).most_common()
        # Take the most frequent one, of second frequent one is less frequent
        if counts[0][1] != counts[1][1]:
            value = counts[0][0]
        else:
            print("Multiple options for VEF value in:\n", df)

    return(value)


def get_maggic_values(df, id):
    df = df[df.record == id]
    return()


# Function to check if the extracted variables are within the defined
# possible ranges
def MAGGIC_var_range(vef, age, sbp, bmi, creatinine, nyha, male, smoke, diabetes, 
                     copd, heart_fail_diag, betablock, acei_arb):
    return()


def calc_maggic_risk(vef, age, sbp, bmi, creatinine, nyha, male, smoke,
                     diabetes, copd, heart_fail_diag, betablock, acei_arb):

    # Variabel Ejection Fraction:
    if vef < 20:
        vef_score = 7
    elif 20 <= vef <= 24:
        vef_score = 6
    elif 25 <= vef <= 29:
        vef_score = 5
    elif 30 <= vef <= 34:
        vef_score = 3
    elif 35 <= vef <= 39:
        vef_score = 2
    elif vef >= 40:
        vef_score = 0

    # Age:
    if age < 55:
        age_score = 0
    elif 56 <= age <= 59:
        if vef < 30:
            age_score = 1
        elif 30 <= vef <= 39:
            age_score = 2
        elif age >= 40:
            age_score = 3
    elif 60 <= age <= 64:
        if vef < 30:
            age_score = 2
        elif 30 <= vef <= 39:
            age_score = 4
        elif age >= 40:
            age_score = 5
    elif 65 <= age <= 69:
        if vef < 30:
            age_score = 4
        elif 30 <= vef <= 39:
            age_score = 6
        elif age >= 40:
            age_score = 7
    elif 70 <= age <= 74:
        if vef < 30:
            age_score = 6
        elif 30 <= vef <= 39:
            age_score = 8
        elif age >= 40:
            age_score = 9
    elif 75 <= age <= 79:
        if vef < 30:
            age_score = 8
        elif 30 <= vef <= 39:
            age_score = 10
        elif age >= 40:
            age_score = 12
    elif age >= 80:
        if vef < 30:
            age_score = 10
        elif 30 <= vef <= 39:
            age_score = 13
        elif age >= 40:
            age_score = 15

    # Systolic blood pressure:
    if sbp < 110:
        if vef < 30:
            sbp_score = 5
        elif 30 <= vef <= 39:
            sbp_score = 3
        elif sbp >= 40:
            sbp_score = 2
    elif 110 <= sbp <= 119:
        if vef < 30:
            sbp_score = 4
        elif 30 <= vef <= 39:
            sbp_score = 2
        elif sbp >= 40:
            sbp_score = 1
    elif 120 <= sbp <= 129:
        if vef < 30:
            sbp_score = 3
        elif 30 <= vef <= 39:
            sbp_score = 1
        elif sbp >= 40:
            sbp_score = 1
    elif 130 <= sbp <= 139:
        if vef < 30:
            sbp_score = 2
        elif 30 <= vef <= 39:
            sbp_score = 1
        elif sbp >= 40:
            sbp_score = 0
    elif 140 <= sbp <= 149:
        if vef < 30:
            sbp_score = 1
        elif 30 <= vef <= 39:
            sbp_score = 0
        elif sbp >= 40:
            sbp_score = 0
    elif sbp >= 150:
        sbp_score = 0

    # BMI
    if bmi < 15:
        bmi_score = 6
    elif 15 <= bmi <= 19:
        bmi_score = 5
    elif 20 <= bmi <= 24:
        bmi_score = 3
    elif 25 <= bmi <= 29:
        bmi_score = 2
    elif bmi >= 30:
        bmi_score = 0

    # Creatinine
    if creatinine < 90:
        crea_score = 0
    elif 90 <= creatinine <= 109:
        crea_score = 1
    elif 110 <= creatinine <= 129:
        crea_score = 2
    elif 130 <= creatinine <= 149:
        crea_score = 3
    elif 150 <= creatinine <= 169:
        crea_score = 4
    elif 170 <= creatinine <= 209:
        crea_score = 5
    elif 210 <= creatinine <= 249:
        crea_score = 6
    elif creatinine >= 250:
        crea_score = 8

    # NYHA
    if nyha == "1":
        nyha_score = 0
    elif nyha == "2":
        nyha_score = 2
    elif nyha == "3":
        nyha_score = 6
    elif nyha == "4":
        nyha_score = 8

    # Male (sex)
    if male:
        male_score = 1
    else:
        male_score = 0

    # smoke
    if smoke:
        smoke_score = 1
    else:
        smoke_score = 0

    # Diabetes
    if diabetes:
        diab_score = 3
    else:
        diab_score = 0

    # COPD
    if copd:
        copd_score = 2
    else:
        copd_score = 0

    # Heart failure diagnosed in passed 18 months
    if heart_fail_diag:
        heart_fail_score = 2
    else:
        heart_fail_score = 0

    # Patient is not on betablockers
    if betablock:
        betablock_score = 0
    else:
        betablock_score = 3

    # Patient is not on ACEI / ARB
    if acei_arb:
        acei_arb_score = 0
    else:
        acei_arb_score = 1

    risk_score = \
        vef_score + age_score + sbp_score + bmi_score + crea_score \
        + nyha_score + male_score + smoke_score + diab_score + copd_score \
        + heart_fail_score + betablock_score + acei_arb_score

    return(risk_score)

