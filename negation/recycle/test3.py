# %%
nl_mod = yaml_to_panda("lexical_kb_05042016_nl.yml")
print("Types of modifiers for nl_mod lexicon:")
categories = nl_mod.Type.value_counts()
print(categories)
# pd.DataFrame.to_clipboard(categories)

# %%
en_mod = yaml_to_panda("en_lex.yml")
print("Types of modifiers for en_mod lexicon:")
categories = en_mod.Type.value_counts()
print(categories)
pd.DataFrame.to_clipboard(categories)


# %%
raw_targets = import_excel("target_test1.xlsx")
regex_df = gen_regex(raw_targets)
print(regex_df)
panda_to_yaml("targets1.yml", regex_df)