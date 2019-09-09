# %%
import pyConTextNLP.pyConText as pyConText
import pyConTextNLP.itemData as itemData
from textblob import TextBlob
# import networkx as nx
# import pyConTextNLP.display.html as html
# from IPython.display import display, HTML
from negation.preprocess_neg import import_excel
from pathlib import Path

# %%
# Declaration of paths to modifier and target data:
modifier_path = "https://raw.githubusercontent.com/chapmanbe/pyConTextNLP/master/KB/lexical_kb_05042016.yml"
target_path = "https://raw.githubusercontent.com/chapmanbe/pyConTextNLP/master/KB/utah_crit.yml"


# %%
def markup_sentence(sentence, modifiers, targets, prune_inactive=True):
    """ Function which executes all markup steps at once
    """
    markup = pyConText.ConTextMarkup()
    markup.setRawText(sentence)
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


# %%
def markup_record(record_text, record_nr, modifiers, targets, output_dict):
    """ Takes current Patient record, applies context algorithm,
    and appends result to output_dict
    """
    # Is used to collect multiple sentence markups. So records can be complete
    context = pyConText.ConTextDocument()

    # Split record into sentences making use of TextBlob
    blob = TextBlob(record_text.lower())
    # print(blob)
    count = 0
    markup_result = []
    # Add markup per sentence
    for sentence in blob.sentences:
        m = markup_sentence(sentence.raw, modifiers=modifiers, targets=targets)
        markup_result.append(m)
        count = count + 1
    print("\nFor record number:", record_nr)
    print("Number of sentences that have been marked up:", count)

    print("\nMarkup result:")
    print(markup_result)

    # Add sentence markup to contextDocument
    for sentence_markup in markup_result:
        context.addMarkup(sentence_markup)

    # Append context object and xml to output dictionary, with as key the record number
    context_xml = context.getXML()
    output_dict.update({record_nr: {"object": context, "xml": context_xml}})

    return(output_dict)


# %%
def apply_context(input_context=input_file, modifier_path=modifier_path, target_path=target_path):
    """
    Function that applies context algorithm on patient records input.
    Returns dictionary:
    {<record number/id>:
        {
        "object" : <context document>,
        "xml" : <context as xml string>
        }
    }
    """
    print("\nNumber of patient records that will be processed:", len(input_context.index))

    # Obtain itemdata
    modifiers = itemData.get_items(modifier_path)
    targets = itemData.get_items(target_path)
    # Initialize output dictionary
    output_dict = {}

    # For each patient record in the input data file:
    for record_index in input_context.index:
        record_text = input_context.at[record_index, "text"]
        record_nr = input_context.at[record_index, "record"]
        # Apply context
        output_dict = markup_record(record_text, record_nr, modifiers, targets, output_dict)

    print("\nOutput dict contains {} context objects" .format(len(output_dict)))
    return(output_dict)


# %%
def export_context(output_dict, filename, record_nr):
    """ Writes the context XML object to an XML file in the output folder.
    Use filename = "<filename>.xml"
    """
    filepath = Path.cwd() / "negation" / "output" / filename
    with open(filepath, "w") as file:
        file.write(output_dict[record_nr]["xml"])


# %%
input_file = import_excel("test_data1.xlsx")
# %%
output_dict1 = apply_context()
export_context(output_dict=output_dict1, filename="context_output1.xml", record_nr=2)

# import pyConTextNLP.utils as contextUtils
# contextUtils.get_section_markups(output_dict1[1]["object"])

# %%
