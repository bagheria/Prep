# %%
import sys
sys.path.append("C:\\Users\\MartijnLaptop3\\Documents\\GitHub\\pyConTextNLP")

import pandas as pd

# %%
from negation import utils
from negation import context
from negation import MAGGIC_values
from negation import preproc
from negation import createObjects
from pprint import pprint

# %%
# Declaration of paths to modifier and target data:
modifier_path = utils.get_path_context("modifiers_nl3.yml")
target_path = utils.get_path_context("MAGGIC2.yml")
test_file = utils.import_excel("test_mod_conflicts.xlsx")

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
context_obj = context.apply_context(
    data, modifier_path, target_path)


# %% Create the batch object
batch1 = createObjects.parse_batch(context_obj, "maggic")

# Process all info
batch1.process()

# Get summary:
df = batch1.getSummary()
print(df)
utils.export_excel(df, "summary.xlsx")

##
df = batch1.getDataframe()
print(df)
utils.export_excel(df, "overview.xlsx")
# df_mod = batch1.objects[2].objects["diabetes"].objects[0]["mods"]["date"].getDataframe()
# print(df_mod)

df_mod = batch1.objects[3].objects["copd"].objects[0]["mods"]["negation"].getDataframe()
print(df_mod)


df_var = batch1.objects[2].objects["diabetes"].getDataframe()
print(df_var)

df_var = batch1.objects[3].objects["copd"].getDataframe()
print(df_var)

df_var = batch1.objects[1].objects["current smoker"].getDataframe()
print(df_var)

df = batch1.objects[4].getDataframe()
print(df)

batch1

# %%
