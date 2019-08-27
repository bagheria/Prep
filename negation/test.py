import pyConTextNLP.pyConText as pyConText
import pyConTextNLP.itemData as itemData
import networkx as nx

reports = [
    """IMPRESSION: Evaluation limited by lack of IV contrast; however, no evidence of
     sbowel obstruction or mass identified within the abdomen or pelvis.
     Non-specific interstitial opacities and bronchiectasis seen at the right
     base, suggestive of post-inflammatory changes.""",
    """IMPRESSION: Evidence of early pulmonary vascular congestion and interstitial edema. 
     Probable scarring at the medial aspect of the right lung base, with no
     definite consolidation."""
    ,
    """IMPRESSION:
     
     1.  2.0 cm cyst of the right renal lower pole.  Otherwise, normal appearance
     of the right kidney with patent vasculature and no sonographic evidence of
     renal artery stenosis.
     2.  Surgically absent left kidney.""",
    """IMPRESSION:  No pneumothorax.""",
    """IMPRESSION: No definite pneumothorax"""
    """IMPRESSION:  New opacity at the left lower lobe consistent with pneumonia."""
]

modifiers = itemData.get_items(
    "https://raw.githubusercontent.com/chapmanbe/pyConTextNLP/master/KB/lexical_kb_05042016.yml")
targets = itemData.get_items(
    "https://raw.githubusercontent.com/chapmanbe/pyConTextNLP/master/KB/utah_crit.yml")

reports[3]

# Instance of context markup class
markup = pyConText.ConTextMarkup()
# Should be true if indeed an instance:
isinstance(markup, nx.DiGraph)

# Setting raw text which will be processed later on
markup.setRawText(reports[3].lower())
print(markup)
print(len(markup.getRawText()))

# Clean text from multiple white spaces
markup.cleanText()
print(markup)
print(len(markup.getText()))

# Identify concepts in the sentence
markup.markItems(modifiers, mode="modifier")
print(markup.nodes(data=True))
print(type(list(markup.nodes())[0]))

# Markup targets
markup.markItems(targets, mode="target")
for node in markup.nodes(data=True):
    print(node)

# Pruning: checking for subsets of other concepts
markup.pruneMarks()
for node in markup.nodes(data=True):
    print(node)

# show relationships between target and modifier nodes
# This is called an edge
print(markup.edges())

# Call function to apply modification to create edges
markup.applyModifiers()
for edge in markup.edges():
    print(edge)
    