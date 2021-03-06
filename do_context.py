# %%
import sys
sys.path.append("C:\\Users\\MartijnLaptop3\\Documents\\GitHub\\pyConTextNLP")

# %%
from negation import utils
from negation import context
from negation import MAGGIC_values
from negation import preproc


# %%
# Declaration of paths to modifier and target data:
modifier_path = utils.get_path_context("modifiers_nl3.yml")
target_path = utils.get_path_context("MAGGIC2.yml")
test_file = utils.import_excel("test_pre_att4.xlsx")

# %% Preprocess and data checks:
# Remove rows with empty values:
data = preproc.drop_empty(test_file)
# Check if data is in right format
preproc.check_data(data)
# Preprocess record text:
data = preproc.preproc_text(data, dot=True, ASCII=True)

# %% Generate Context output
# Apply context algorithm on data
# Save context documents in output_dict1
output_dict1 = context.apply_context(
    data, modifier_path, target_path)
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
    utils.get_path("negation", "output", filename="df1.xlsx"))

# %%
mag_var_df = utils.import_vars("maggic_variables.xlsx")
a = MAGGIC_values.join_maggic(mag_var_df, context_job_df)
b = MAGGIC_values.get_maggic_output(a)
b.to_excel(
    utils.get_path("negation", "output", filename="df2.xlsx"))


# MAGGIC_values.test()
# %%
