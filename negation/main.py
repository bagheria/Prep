# %%
import negation.preprocess_neg
import negation.context


# %%
# Declaration of paths to modifier and target data:
modifier_path = negation.preprocess_neg.get_path_context("modifiers.yml")
target_path = negation.preprocess_neg.get_path_context("targets.yml")
test_file = negation.preprocess_neg.import_excel("test_data1.xlsx")

# %% Generate Context output
# Apply context algorithm on data
# Save context documents in output_dict1
output_dict1 = negation.context.apply_context(
    test_file, modifier_path, target_path)
# Export context document of record 2
negation.context.export_context(
    output_dict=output_dict1, filename="context_output1.xml", record_nr=2)

# %% Analyze context output
# Import single record from file:
# And display as dataframe:
record2_df = negation.context.context_df_file("context_output1.xml", 1)
print(record2_df)
# Now for multiple records from dictionary
context_job_df = negation.context.context_df_dict(output_dict1)
print(context_job_df)


# %%
