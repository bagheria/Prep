# %%
import sys
sys.path.append("C:\\Users\\MartijnLaptop3\\Documents\\GitHub\\pyConTextNLP")

# %%
from negation import utils
from negation import context
from negation import MAGGIC_values
from negation import preproc
from negation import risk

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
context_obj = context.apply_context(
    data, modifier_path, target_path)

# %% Process Context documents
results = risk.parse_batch(context_obj)

# %%
result = results[12]
result.getOverview()

# %%
result.getMissingAtrs()
# %%
result.getConflictAtrs()
# %%
result.getModScores()

# %%
for var in result.dict:
    print(var)
    for finding in result.dict[var]:
        print(finding)
        print(finding.negation["score"])
# %%
record1 = context_obj[11]["object"]

for record in context_obj:
    # Do for every ConTextDocument 
    # that is created per patient record:
    record_obj = context_obj[record]["object"]
    section_markups = record_obj.getSectionMarkups()
    for sent_markup in section_markups:
        # print(sent_markup[1])
        targets = sent_markup[1].getMarkedTargets()
        for target in targets:
            print("\n")
            print("Target:", target.getCategory(), target.getPhrase(), target.getLiteral())
            mods = sent_markup[1].predecessors(target)
            for mod in mods:
                print("mod:", mod.getCategory(), mod.getPhrase())
 



# %%
rec1_graph = record1.getDocumentGraph()
rec1_sections = record1.getDocumentSections()
rec1_section_markup = record1.getSectionMarkups()
# %%
with open("testxml.xml", "w") as file:
            file.write(record1.getXML())


# %% Get all sentence markups:
markups = context_obj[11]["object"].getSectionMarkups()
for sent_markup in markups:
    # print(sent_markup[1])
    # print(sent_markup[1].getMarkedTargets())
    for target in sent_markup[1].getMarkedTargets():
        # print(target)
        print("literal", target.getLiteral())
        print("Category", target.getCategory())



# %%
graph = rec1_section_markup[1][1]
targets = graph.getMarkedTargets()
mods = []
for mod in graph.predecessors(targets[0]):
    mods.append(mod)
print(mods)
# %%
