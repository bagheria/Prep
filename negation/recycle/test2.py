import pyConTextNLP.pyConText as pyConText
import pyConTextNLP.itemData as itemData
from textblob import TextBlob
# import networkx as nx
import pyConTextNLP.display.html as html
from IPython.display import display, HTML
from negation.preprocess_neg import import_excel
from pathlib import Path

test_df = import_excel("test_data1.xlsx")

test_df.tekst[0]

modifiers = itemData.get_items(
    "https://raw.githubusercontent.com/chapmanbe/pyConTextNLP/master/KB/lexical_kb_05042016.yml")
targets = itemData.get_items(
    "https://raw.githubusercontent.com/chapmanbe/pyConTextNLP/master/KB/utah_crit.yml")


def markup_sentence(s, modifiers, targets, prune_inactive=True):
    """ Function which executes all markup steps at once
    """
    markup = pyConText.ConTextMarkup()
    markup.setRawText(s)
    markup.cleanText()
    markup.markItems(modifiers, mode="modifier")
    markup.markItems(targets, mode="target")
    markup.pruneMarks()
    markup.dropMarks('Exclusion')
    # apply modifiers to any targets within the modifiers scope
    markup.applyModifiers()
    markup.pruneSelfModifyingRelationships()
    if prune_inactive:
        markup.dropInactiveModifiers()
    return markup


# Is used to collect multiple sentence markups. So records can be complete
context = pyConText.ConTextDocument()

# Split into sentences making use of TextBlob
blob = TextBlob(test_df.tekst[0].lower())
print(blob)
count = 0
result = []
for sentence in blob.sentences:
    m = markup_sentence(sentence.raw, modifiers=modifiers, targets=targets)
    result.append(m)
    count = count + 1
print("Number of sentences that have been marked up:", count)

for r in result:
    context.addMarkup(r)

print(result)

# Visualize results:
clrs = {
    "bowel_obstruction": "blue",
    "inflammation": "blue",
    "definite_negated_existence": "red",
    "probable_negated_existence": "indianred",
    "ambivalent_existence": "orange",
    "probable_existence": "forestgreen",
    "definite_existence": "green",
    "historical": "goldenrod",
    "indication": "pink",
    "acute": "golden"
}
display(HTML(html.mark_document_with_html(context, colors=clrs,
        default_color="black")))
print(context.getXML())

context_result = context.getXML()
with open(Path.cwd() / "negation" / "output" / "context_object.xml", "w") as f:
    f.write(context_result)

test_dict = {1 : context_result, 2 : context}