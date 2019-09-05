from pathlib import Path
import xml.etree.ElementTree as ET
import pandas as pd


def import_context(filename):
    filepath = Path.cwd() / "negation" / "output" / filename
    with open(filepath, "r") as file:
        content = file.read()
        return(content)


def context_df_file(filename, record):
    filepath = Path.cwd() / "negation" / "output" / filename
    tree = ET.parse(filepath)
    root = tree.getroot()

    columns = ["record", "phrase", "literal", "modifier"]
    index = []
    df = pd.DataFrame(index=index, columns=columns)
    i = 0

    # Collect information about all targets
    for node in root.findall(".//node"):
        cat = str.strip(node.find("./category").text)
        if cat == "target":
            phrase = str.strip(node.find(".//phrase").text)
            lit = str.strip(node.find(".//literal").text)
            for mod in node.findall(".//modifyingCategory"):
                modifier = str.strip(mod.text)
                # Add every modification of a target as a row to df
                df.loc[i] = pd.Series({"phrase": phrase, "literal": lit, "modifier": modifier})
                i = i + 1
    return(df)


def context_df_dict(dict):
    """ Converts dictionary with context objects as values to
    dataframe containing all modifications on the targets
    """

    columns = ["record", "phrase", "literal", "modifier"]
    index = []
    df = pd.DataFrame(index=index, columns=columns)
    i = 0

    for key in dict:

        # uses additional xml initialization,
        # because fromstring() doesnt return an ElementTree
        tree = ET.ElementTree(ET.fromstring(dict[key]))
        root = tree.getroot()

        # Collect information about all targets
        for node in root.findall(".//node"):
            cat = str.strip(node.find("./category").text)
            if cat == "target":
                phrase = str.strip(node.find(".//phrase").text)
                lit = str.strip(node.find(".//literal").text)
                for mod in node.findall(".//modifyingCategory"):
                    modifier = str.strip(mod.text)
                    # Add every modification of a target as a row to df
                    df.loc[i] = pd.Series({"record": key, "phrase": phrase, "literal": lit, "modifier": modifier})
                    i = i + 1
    return(df)


# Import single record from file:
output = context_df_file("context_output1.xml", 1)
# Import multiple records from dictionary (apply_context.py)
output2 = context_df_dict(output_dict1)


# # To show the root tag:
# root.tag
# # Shows root attributes:
# root.attrib

# for child in root:
#     print(child.tag, child.attrib)

# # shows all elements in the document
# for elem in root.iter():
#     print(elem.tag)

# # to print the entire document as string:
# print(ET.tostring(root, encoding='utf8').decode('utf8'))

# for elem in root.iter('edge'):
#     print(elem.text)

# for movie in root.findall("./genre/decade/movie/[year='1992']"):
#     print(movie.attrib)

# for sent in root.iter("sentenceNumber"):
#     sent_nr = sent.text
#     for child in root.findall("sentenceNumber='{}'".format(sent_nr)):
#         print(child.text)

# a = root.find(".//[sentenceNumber]")
# a.tag

# for a in root.find("../[sentenceNumber='1']"):
#     print(a.tag)

# for elem in a.iter():
#     print(elem.tag)

# for category in root.iter("category"):
#     print(category.text)


# for movie in root.findall(".//tagObject/"):
#     print(movie.text)

# for node in root.findall(".//node"):
#     cat = str.strip(node.find("./category").text)
#     if cat == "target":
#         phrase = str.strip(node.find(".//phrase").text)
#         lit = str.strip(node.find(".//literal").text)
#         for mod in node.findall(".//modifyingCategory"):
#             modifier = str.strip(mod.text)
#             print(phrase, lit)

#         if cat.text == "target":
#             for target in cat.findall("../")
#     # for type in node.findall("./tagObject/category"):
#     #     print("Type:", type.text)
