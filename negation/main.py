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
    output_dict=output_dict1, filename="context_output_MAGGIC.xml", record_nr=2)

# %% Analyze context output
# Import single record from file:
# And display as dataframe:
# record2_df = context.context_df_file("context_output1.xml", 1)
# print(record2_df)
# Now for multiple records from dictionary
context_job_df = context.context_df_dict(output_dict1)
print(context_job_df)

# %%
a = MAGGIC_values.join_maggic("maggic_variables.xlsx", context_job_df)

# %%
