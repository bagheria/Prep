# %%
import pyConTextNLP.pyConText as pyConText
import pyConTextNLP.itemData as itemData
from textblob import TextBlob
# import networkx as nx
# import pyConTextNLP.display.html as html
# from IPython.display import display, HTML
from pathlib import Path
import xml.etree.ElementTree as ET
import pandas as pd


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

    # Append context object and xml to output dictionary,
    # with as key the record number
    context_xml = context.getXML()
    output_dict.update({record_nr: {"object": context, "xml": context_xml}})

    return(output_dict)


# %%
def apply_context(input_context, modifier_path, target_path):
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
    print("\nNumber of patient records that will be processed:",
          len(input_context.index))

    # Obtain itemdata
    modifiers = itemData.get_items(modifier_path)
    targets = itemData.get_items(target_path)
    # Initialize output dictionary
    output_dict = {}

    # For each patient record in the input data file:
    for record_index in input_context.index:
        record_text = input_context.at[record_index, "text"]
        record_nr = input_context.at[record_index, "record"]
    
        # check if record is string, otherwise skip markup for record
        if isinstance(record_text, str):
            # Apply context
            output_dict = \
                markup_record(record_text, record_nr,
                              modifiers, targets, output_dict)
        else:
            print(f"\nRecord number {record_nr} is no string. This record is skipped.")
        print(f"Output dict after record: {record_nr}\n{output_dict}")
    n_objects = len(output_dict)
    print(f"\nOutput object contains {n_objects} context objects\n")
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
# Imports context document from XML file
def import_context(filename):
    filepath = Path.cwd() / "negation" / "output" / filename
    with open(filepath, "r") as file:
        content = file.read()
        return(content)


# %%
def context_df_file(filename, record):
    """
    Transforms single context document record to pandas dataframe
    """
    filepath = Path.cwd() / "negation" / "output" / filename
    tree = ET.parse(filepath)
    root = tree.getroot()

    columns = ["record", "phrase", "literal", "category", "modifier"]
    index = []
    df = pd.DataFrame(index=index, columns=columns)
    i = 0

    # Collect information about all targets
    for node in root.findall(".//node"):
        cat = str.strip(node.find("./category").text)
        if cat == "target":
            phrase = str.strip(node.find(".//phrase").text)
            lit = str.strip(node.find(".//literal").text)
            cat = str.strip(node.find(".//category").text)
            # For every target, multiple modifiers can be identified:
            for mod in node.findall(".//modifyingCategory"):
                modifier = str.strip(mod.text)
                # Add every modification of a target as a row to df
                df.loc[i] = pd.Series({"phrase": phrase, "literal": lit,
                                       "category": cat, "modifier": modifier})
                i = i + 1
    return(df)


# %%
def context_df_dict(dict):
    """ Converts dictionary with context objects as values to
    dataframe containing all modifications on the targets
    """

    columns = ["record", "phrase", "literal", "category", "modifier"]
    index = []
    df = pd.DataFrame(index=index, columns=columns)
    i = 0

    for key in dict:

        # uses additional xml initialization,
        # because fromstring() doesnt return an ElementTree
        tree = ET.ElementTree(ET.fromstring(dict[key]["xml"]))
        root = tree.getroot()

        # Collect information about all targets
        for node in root.findall(".//node"):
            cat = str.strip(node.find("./category").text)
            # print(f"cat: {cat}\n")
            if cat == "target":
                phrase = str.strip(node.find(".//phrase").text)
                lit = str.strip(node.find(".//literal").text)
                cat = str.strip(node.find(".//tagObject/category").text)
                # print(f"phrase: {phrase}, literal: {lit}, cat: {cat}\n")
                # print(type(node.findall(".//modifyingCategory")))
                
                # If the modifiers have been identified for current target:
                # Make a row in output dataframe for every modifier
                if len(node.findall(".//modifyingCategory")) > 0:
                    
                    for mod in node.findall(".//modifyingCategory"):
                        # print(mod)
                        modifier = str.strip(mod.text)
                        # print(f"modifier: {modifier}\n")
                        # Add every modification of a target as a row to df
                        df.loc[i] = pd.Series({"record": key, "phrase": phrase,
                                            "literal": lit, "category": cat,
                                            "modifier": modifier})
                        i = i + 1
                
                # If no modifiers for current target:
                # Leave "modifier" column empty
                else:
                    df.loc[i] = pd.Series({"record": key, "phrase": phrase,
                                        "literal": lit, "category": cat,
                                        "modifier": ""})
                    i = i + 1
    return(df)


# %%

# import pyConTextNLP.utils as contextUtils
# contextUtils.get_section_markups(output_dict1[1]["object"])

# %%