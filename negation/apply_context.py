import pyConTextNLP.pyConText as pyConText
import pyConTextNLP.itemData as itemData
from textblob import TextBlob
# import networkx as nx
# import pyConTextNLP.display.html as html
# from IPython.display import display, HTML
from negation.preprocess_neg import import_excel
from pathlib import Path

# Input files have to be in the "data" folder
input_file = "test_data1.xlsx"
modifier_path = "https://raw.githubusercontent.com/chapmanbe/pyConTextNLP/master/KB/lexical_kb_05042016.yml"
target_path = "https://raw.githubusercontent.com/chapmanbe/pyConTextNLP/master/KB/utah_crit.yml"


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

    # Append context object to output dictionary, with as key the record number
    context_result = context.getXML()
    output_dict.update({record_nr: context_result})

    return(output_dict)


def apply_context(input_file=input_file, modifier_path=modifier_path, target_path=target_path):
    """ Function that applies context algorithm on patient records input.
    Will return dictionary with as key record number, and as value ContextDocument.
    """

    input_context = import_excel(input_file)

    print("\nNumber of patient records that will be processed:", len(input_context.index))

    modifiers = itemData.get_items(modifier_path)
    targets = itemData.get_items(target_path)
    output_dict = {}

    for record_index in input_context.index:
        record_text = input_context.at[record_index, "text"]
        record_nr = input_context.at[record_index, "record"]
        # Apply context algorithm on single patient record
        output_dict = markup_record(record_text, record_nr, modifiers, targets, output_dict)

    print("\nOutput dict contains {} context objects" .format(len(output_dict)))
    return(output_dict)


def export_context(output_dict, filename, record_nr):
    """ Writes the context XML object to an XML file in the output folder.
    Use filename = "<filename>.xml"
    """
    filepath = Path.cwd() / "negation" / "output" / filename
    with open(filepath, "w") as file:
        file.write(output_dict[record_nr])


output_dict1 = apply_context()
export_context(output_dict=output_dict1, filename="context_output1.xml", record_nr=2)
