# %%
# from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktLanguageVars
import re
from negation import utils
# import pandas as pd


# %%
test_split = utils.import_excel("test_split.xlsx")

# # %%
# class UMCULangVars(PunktLanguageVars):
#     sent_end_chars = ('.', '?', '!', '..', '...')

# # %%
# tokenizer = PunktSentenceTokenizer(lang_vars=UMCULangVars())
# tokenizer.tokenize(u"• I am a sentence • I am another sentence")

# %%
for sent in test_split.index:
    sentence = test_split.at[sent, "text"]
    new = re.sub(r'\.{1,3}|…', 'XXX', string=sentence)
    print(new)

#%%
