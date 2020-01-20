import pandas as pd


def binary(sub_df):
    ls_found = list(set(sub_df['isFound'].values))
    if len(ls_found) > 1:
        raise Exception("isFound can only have 1 value per record, var combination", ls_found)

    # if not found any finding for var:
    if not ls_found[0]:
        result = "blank"
        ls_result = []
        return(result, ls_result)

    # if found a finding for var
    elif ls_found[0]:
        ls_result = list(sub_df['neg_isNegated'].values)
        ls_neg = list(set(ls_result))
        if len(ls_neg) > 1:
            result = "conflict"
        elif len(ls_neg) == 1:
            if ls_neg[0]:
                result = "negated"
            elif not ls_neg[0]:
                result = "affirmative"
            else:
                raise Exception("isNegated must be True or False", ls_neg[0])

        return(result, ls_result)
    else:
        raise Exception("isFound must be true or false:", ls_found)


def factorial(sub_df):
    ls_found = list(set(sub_df['isFound'].values))
    if len(ls_found) > 1:
        raise Exception("isFound can only have 1 value per record, var combination", ls_found)

    # if not found any finding for var:
    if not ls_found[0]:
        result = "blank"
        ls_result = []
        return(result, ls_result)

    # if found a finding for var
    elif ls_found[0]:
        ls_result = list(sub_df['factInt'].values)
        ls_fact = list(set(ls_result))
        # Multiple varying values:
        if len(ls_fact) > 1:
            result = "conflict"
        # 1 type of value
        elif len(ls_fact) == 1:
            result = ls_fact[0]

        return(result, ls_result)
    else:
        raise Exception("isFound must be true or false:", ls_found)


def numeric(sub_df):
    ls_found = list(set(sub_df['isFound'].values))
    if len(ls_found) > 1:
        raise Exception("isFound can only have 1 value per record, var combination", ls_found)

    # if not found any finding for var:
    if not ls_found[0]:
        result = "blank"
        ls_result = []
        return(result, ls_result)

    # if found a finding for var
    elif ls_found[0]:
        ls_result = [value[0] for value in sub_df['values'].values]
        ls_fact = list(set(ls_result))
        # Multiple varying values:
        if len(ls_fact) > 1:
            result = "conflict"
        # 1 type of value
        elif len(ls_fact) == 1:
            result = ls_fact[0]

        return(result, ls_result)
    else:
        raise Exception("isFound must be true or false:", ls_found)


def summarize_summary(df):
    """Summarizes the information to 1 row per patient"""
    records = df['patID']
    vars = df['var']
    master_dict = {}
    # filter per record:
    for rec in records:
        sub_dict = {}
        # filter per var:
        for var in vars:
            sub_df = df[(df['patID'] == rec) & (df['var'] == var)]

            # Binary
            if list(sub_df['varType'])[0] == 'binary':
                res, ls = binary(sub_df)
                # output = pd.DataFrame([[res, ls]], columns=[var, var+"Values"])

            # Numeric
            elif list(sub_df['varType'])[0] == 'numeric':
                res, ls = numeric(sub_df)
                # output = pd.DataFrame([[res, ls]], columns=[var, var+"Values"])

            # Factorial
            elif list(sub_df['varType'])[0] == 'factorial':
                res, ls = factorial(sub_df)
                # output = pd.DataFrame([[res, ls]], columns=[var, var+"Values"])

            else:
                raise Exception("varType not recognized:", sub_df['varType'])

            name2 = var+"Values"
            sub_dict.update({var: res, name2: ls})

        # Add subdict to master_dict
        master_dict.update({rec: sub_dict})

    result = pd.DataFrame.from_dict(master_dict, orient="index")
    result.insert(0, "index", result.index)

    return(result)
