import re
from abc import ABC, abstractmethod
import pandas as pd
import negation.modifiers as modifiers
import negation.risk_vars as risk_vars
from pprint import pprint

# pyreverse -o png -p classdiagram1 negation\risk.py

# %%
class Factory:
    def __init__(self):
        pass

    _numeric_vars = ["age", "vef", "sbp", "bmi", "creatinine"]
    _factorial_vars = ["nyha"]
    _binary_vars = ["gender", "current smoker", "diabetes", "copd", 
    "heart failure", "beta blocker", "acei"]

    def createVar(self, type, object):
        # print("type:", type)
        if type in self._numeric_vars:
            return(risk_vars.NumVar(object))
        elif type in self._factorial_vars:
            return(risk_vars.FactVar(object))
        elif type in self._binary_vars:
            return(risk_vars.BinVar(object))
        else:
            raise Exception("Variable type not recognized:",
            type, object)

    _examination_mods = ["indication", "hypothetical"]
    _negation_mods = [
        "definite_negated_existence", "probable_negated_existence",
        "probable_existence", "definite_existence", "ambivalent_existence",
        "pseudoneg"]
    _date_mods = ["date"]
    _temporality_mods = ["historical", "future", "acute"]

    
    def createMod(self, type, object):
        if type in self._examination_mods:
            return(modifiers.ExamMod(object))
        elif type in self._negation_mods:
            return(modifiers.NegMod(object))
        elif type in self._date_mods:
            return(modifiers.DateMod(object))
        elif type in self._temporality_mods:
            return(modifiers.TempMod(object))
        else:
            raise Exception("Modifier type not recognized:",
            type, object)



class PatientVars:
    _risk_vars = ["vef", "sbp", "nyha", "current smoker", "diabetes", "copd"]
    # i = 0
    # for var in risk_vars:
    #     risk_vars[i] = "['" + risk_vars[i] + "']"
    #     i += 1

    def __init__(self):
        # self.vef = []
        # self.sbp = []
        # self.nyha = []
        # self.current_smoker = []
        # self.diabetes = []
        # self.copd = []
        for var in self._risk_vars:
            setattr(self, var, [])
        dict = {}
        for key in self._risk_vars: 
            dict[key] = []
        self.dict = dict

    def addFinding(self, object):
        """ Adds RiskVar object to PatientVars dictionary based
        on the category of the RiskVar object
        """
        atr_list = getattr(self, object.cat)
        atr_list.append(object)
        setattr(self, object.cat, atr_list)

    def process(self):
        """Processes all findings. Must be performed before querying results
        """
        # self._detMissingAtrs()
        # self._detAbundantAtrs()
        # self._conflictAtrs()
        

    # def _detMissingAtrs(self):
    #     """Add all keys of missing attributes to list self.missing
    #     """
    #     self.missing = []
    #     self.present = []
    #     for key in self.dict:
    #         if not self.dict[key]:
    #             self.missing.append(key)
    #         else:
    #             self.present.append(key)

    # def _detAbundantAtrs(self):
    #     """Compares for each attribute the findings if multiple findings
    #     """
    #     self.abundant = []
    #     for key in self.dict:
    #         atr = self.dict[key]
    #         if len(atr) > 1:
    #             self.abundant.append(key)

    # def _conflictAtrs(self):
    #     """Keep track of all matching and conflicting findings per variable
    #     Stores them in a dictionary
    #     """
    #     # Initialize conflicts dictionary
    #     conflicts = {}
    #     for key in self.abundant: 
    #         conflicts[key] = {"match":[], "conflict":[]}
        
    #     # Loop over variable objects per variable
    #     for key in self.abundant:
    #         for i in range(len(self.dict[key])):
    #             for j in range(i+1, len(self.dict[key])):
    #                 match = self.dict[key][i] == self.dict[key][j]
    #                 if match:
    #                     conflicts[key]["match"].append((i,j))
    #                 else:
    #                     conflicts[key]["conflict"].append((i,j))
    #     self.conflicts = conflicts
            
    # def _gatherResults(self):
    #     new_dict = {}
    #     for atr in self.dict:
    #         ls = []
    #         for finding in self.dict[atr]:
    #             if finding.type == "numeric":
    #                 result = self._gatherNumResult(finding)
    #             elif finding.type == "factorial":
    #                 result = self._gatherFactResult(finding)
    #             elif finding.type == "binary":
    #                 result = self._gatherBinResult(finding)
    #             ls.append(result)
    #         new_dict.update({atr : ls})
    
    # def _gatherNumResult(self, finding):
    #     values = finding.rec_values

    # def getOverview(self):
    #     new_dict = {}
    #     for atr in self.dict:
    #         ls = []
    #         for finding in self.dict[atr]:
    #             data = finding.getOverview()
    #             ls.append(data)
    #         new_dict.update({atr : ls})
    #     return(new_dict)

    # def getMods(self):
    #     new_dict = {}
    #     for atr in self.dict:
    #         findings = self.dict[atr]
    #         if findings:
    #             ls = []
    #             for finding in findings:
    #                 mods = finding.mod
    #                 if mods:
    #                     for mod in mods:
    #                         ls.append((mod.phrase, mod.type, mod.value))
    #             new_dict.update({atr : ls})
    #     return(new_dict)

    def view(self):
        dict = {}
        for var in self._risk_vars:
            findings = getattr(self, var)
            sub_dict = {}
            for index, finding in enumerate(findings):
                # sub_dict.update({"mod" : finding.getModInfo()})
                sub_dict.update({
                    index : finding.view()})
            dict.update({var : sub_dict})
        return(dict)

    # def getMissingAtrs(self):
    #     """Returns list of missing variables"""
    #     if not self.missing:
    #         print("No missing variables")
    #         return(None)
    #     else:
    #         print("Missing variables")
    #         return(self.missing)

    # def getConflictAtrs(self):
    #     """Returns dictionary TagObjects of conflicting findings"""
    #     if not self.conflicts:
    #         print("No conflicts found")
    #         return(None)
    #     else:
    #         print("Conflicts found:")
    #         # print(self.conflicts)
    #         # Generate a dictionary that contains the conflicted objects
    #         ret_dict = {}
    #         # For every atribute check if conflicts present
    #         for atr in self.conflicts:
    #             atr_confls = self.conflicts[atr]["conflict"]
    #             if atr_confls:
    #                 ret_dict.update({atr : []})
    #                 # For every pair in conflict list
    #                 for pair_index in range(0,len(atr_confls)):
    #                     # Add object as pair te return dict
    #                     pair = atr_confls[pair_index]
    #                     obj_pair = (
    #                         self.dict[atr][pair[0]], 
    #                         self.dict[atr][pair[1]])
    #                     ret_dict[atr].append(obj_pair)

    #         for atr in ret_dict:
    #             print("\nAttribute:", atr)
    #             for confl in ret_dict[atr]:
    #                 print("1:")
    #                 print("Text:", confl[0].phrase)
    #                 print("Results:", confl[0].result)
    #                 print("2:")
    #                 print("Text:", confl[1].phrase)
    #                 print("Results:", confl[1].result)
    #                 print("\n")
                       
    #         return(ret_dict)



    # def getNegation(self):
    #     """Returns a dictionary with negation results"""
    #     dict = {}
    #     for key in self.dict:
    #         if self.dict[key]:
    #             ls = []
    #             for finding in self.dict[key]:
    #                 if not finding.negation["score"]:
    #                     ls.append((finding.negation["score"],
    #                         finding.negation["polarity"]))
    #                 else:
    #                     ls.append((finding.negation["score"],
    #                         finding.negation["polarity"], ))
    #             new = {key : ls}
    #             dict.update(new)
    #     if not dict:
    #         print("No negation scores")
    #         return(None)
    #     print("Negation scores:")
    #     return(dict)



# %%
def parse_batch(context_dict):
    """Go over all patient context documents and create a 
    patient var object per patient, put in a returned dictionary.
    """
    result = {}
    for pat_id in context_dict:
        patient_vars = parse_object(context_dict[pat_id]["object"])
        patient_vars.process()
        result.update({pat_id : patient_vars})
    print(len(result), "patient objects have been created.")
    return(result)



def parse_object(context_doc):
    """
    Go over all targets in a patient ContextDocument and add
    These findings to the patient_vars object
    """
    patient_vars = PatientVars()
    section_markups = context_doc.getSectionMarkups()
    for sent_markup in section_markups:
        # print(sent_markup[1])
        targets = sent_markup[1].getMarkedTargets()
        for target in targets:
            finding = parse_findings(target, sent_markup)
            patient_vars.addFinding(finding)
    return(patient_vars)
    

def parse_findings(target, sent_markup):
    """
    Create risk variable object for every finding found,
    add modifiers to these objects, process the information in the object,
    and return it to be added to patient object
    """
    # print(target.categoryString())
    risk_var = factory.createVar(target.categoryString(), target)
    # print("\n")
    # print("Target:", target.getCategory(), target.getPhrase(), target.getLiteral())
    mods = sent_markup[1].predecessors(target)
    for mod in mods:
        # print("mod:", mod.getCategory(), mod.getPhrase())
        mod_obj = factory.createMod(mod.categoryString(), mod)
        risk_var.addMod(mod_obj)
    # risk_var.processInfo()
    return(risk_var)
            
factory = Factory()
# # %% Check vefs (getValue method)
# context_doc = context_obj[11]["object"]
# pat3 = parse_object(context_doc)'
# vefs = pat3.dict['vef']
# vef1 = vefs[0]

# var1 = NumVar(vef1.object)
# var1.object.getPhrase()
# var1.processInfo()
# var1.phrase
# var1.getValue()

# # %% Check mods (modify method)
# smoke_var = pat3.dict['current smoker'][0]
# # # %%
# # result1 = parse_batch(context_obj)

# # %%
