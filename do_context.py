# %%
from negation import preprocess_neg
from negation import context
from negation import MAGGIC_values


# %%
# Declaration of paths to modifier and target data:
modifier_path = preprocess_neg.get_path_context("modifiers_nl.yml")
target_path = preprocess_neg.get_path_context("MAGGIC.yml")
test_file = preprocess_neg.import_excel("test_data_maggic.xlsx")

# %% Generate Context output
# Apply context algorithm on data
# Save context documents in output_dict1
output_dict1 = context.apply_context(
    test_file, modifier_path, target_path)
# # Export context document of record 2
context.export_context(
    output_dict=output_dict1, subfolder="attempt1")

# %% Analyze context output
# # Import single record from file:
# # And display as dataframe:
# record2_df = context.file_to_df("context_output1.xml", 1)
# print(record2_df)
# Now for multiple records from dictionary
context_job_df = context.dict_to_df(output_dict1, incl_mod=True)
print(context_job_df)
context_job_df.to_excel(
    preprocess_neg.get_path("negation", "output", filename="df1.xlsx"))

# %%
mag_var_df = preprocess_neg.import_vars("maggic_variables.xlsx")
a = MAGGIC_values.join_maggic(mag_var_df, context_job_df)
b = MAGGIC_values.get_maggic_output(a)
b.to_excel(
    preprocess_neg.get_path("negation", "output", filename="df2.xlsx"))


# MAGGIC_values.test()
# %%
