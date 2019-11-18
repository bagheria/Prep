import re
from abc import ABC, abstractmethod

# %%
class varFactory:
    _numeric_vars = ["age", "vef", "sbp", "bmi", "creatinine"]
    _factorial_vars = ["nyha"]
    _binary_vars = ["gender", "current smoker", "diabetes", "copd", 
    "heart failure", "beta blocker", "acei"]

    def __init__(self):
        pass

    def createVar(self, type, object):
        print("type:", type)
        if type in self._numeric_vars:
            return(NumVar(object))
        elif type in self._factorial_vars:
            return(FactVar(object))
        elif type in self._binary_vars:
            return(BinVar(object))
        else:
            raise Exception("Variable type not recognized:",
            type, object)


class RiskVar(ABC):
    
    def __init__(self, object):
        self.object = object
        self.literal = object.getLiteral()
        self.mod = []
        self.cat = object.categoryString()
        self.phrase = object.getPhrase()
        self._setType()


    @abstractmethod
    def __eq__(self, other):
        pass

    @abstractmethod 
    def _setType(self):
        pass

    def addMod(self, mod):
        """Adds mod to self.mod list"""
        self.mod.append(mod)

    # All methods that must be called after object construction
    # and modifier addition
    def processInfo(self):
        """processes object and mod information after complete construction
        of object"""
        # If self.mod is not empty:
        if self.mod:
            self._modify()
            if self.negScore:
                self._processNeg()
                

    # Check for modification
    def _modify(self):
        """Processes modifier information:
        - Add negation scores to self.negScore list
        if self.negScore is None, no negations detected
        """
        self.negScore = []

        for mod in self.mod:
            string = mod.categoryString()
            # For negation modifiers:
            if "existence" in string:
                if string == "definite_negated_existence":
                    score = -2
                elif string == "probable_negated_existence":
                    score = -1
                elif string == "probable_existence":
                    score = 1
                elif string == "definite_existence":
                    score = 2
                # Pseudonegation and ambivalent negation:
                else:
                    score = 0
                self.negScore.append(score)

    def _processNeg(self):
        # Sets can't have duplicates
        set_neg = set(self.negScore)
        pos = any(n > 0 for n in set_neg)
        neg = any(n < 0 for n in set_neg)
        oth = any(n == 0 for n in set_neg)

        if len(set_neg) > 1 and pos and neg:
            self.conflict_neg = True
        else:
            self.conflict_neg = False

        if not self.conflict_neg:
            if pos and not neg:
                self.negation_polarity = "Confirmative"
            if neg and not pos:
                self.negation_polarity = "Negative"


class NumVar(RiskVar):

    def __init__(self, object):
        self.rec_values = []
        return super().__init__(object)
    
    def __eq__(self, other):
        return(self.value == other.value)

    def _setType(self):
        self.type = "numeric"

    def processInfo(self):
        super().processInfo()
        if self.cat == "vef":
            self._getValueVef()
        elif self.cat == "sbp":
            self._getValueSbp()
        else:
            raise Exception("Numeric variable, but not recognized as vef or sbp",
                self.phrase)
        self._conflictValue()
        self._processValue()

    def _getValueVef(self):
        """Collects values from target's phrase. Multiple values per 
        string are separately added to self.rec_values list
        """
        # Search for pattern with outer characters digits
        string = re.search(pattern = r"\d(.*)\d", string = self.phrase)
        if string is None:
            raise Exception(
                "No value found when searching in phrase of numeric variable",
                self.phrase)
        # If there are no other other characters within string 
        # that are no digits, value is just the string 
        if re.search(pattern=r"\D", string=string.group()) is None:
            self.rec_values.append(string.group())
        # Else, it is a range, so split up values
        else:
            values = re.findall(pattern = r"\d+", string=string.group())
            range_list = []
            for value in values: range_list.append(value)
            if len(range_list) != 2:
                raise Exception("Phrase recognized as range, but no 2 values",
                self.phrase, string.group(), values, range_list)
            self.rec_values.append(range_list)

    def _getValueSbp(self):
        string = re.search(pattern = r"\d{2,3}(?=/(\d{2,3}))", string = self.phrase)
        if string is None:
            raise Exception(
                "No value found when searching in phrase of numeric variable",
                self.phrase)
        else:
            self.rec_values.append(string.group())

    def _conflictValue(self):
        if any(isinstance(i, list) for i in self.rec_values) \
            or len(set(self.rec_values)) > 1:
            self.values_conflict = True
        else:
            self.values_conflict = False

    def _processValue(self):
        if not self.values_conflict:
            self.value = self.rec_values[0]
        else: 
            self.value = False

    
class BinVar(RiskVar):

    def __init__(self, object):
        return super().__init__(object)

    def __eq__(self, other):
        return(self.negation_polarity == other.negation_polarity)

    def _setType(self):
        self.type = "binary"

    def processInfo(self):
        super().processInfo()
        

class FactVar(RiskVar):

    def __init__(self, object):
        return super().__init__(object)

    def __eq__(self, other):
        return(self.negation_polarity == other.negation_polarity
            and self.factor == other.factor)

    def _setType(self):
        self.type = "factorial"
    
    def processInfo(self):
        super().processInfo()
        self._processFactor()

    def _processFactor(self):
        self.factor = self.literal        
            
    
# class NumVar(RiskVar):

# %%
# class PatientVars:
#     def __init__(self):
#         self.vef = []
#         self.sbp = []
#         self.nyha = []
#         self.current_smoker = []
#         self.diabetes = []
#         self.copd = []

#     def setVef(self, vef):
#         self.vef.append(vef)

# %%
# i = 0
# risk_vars = ["vef", "sbp", "nyha", "current_smoker", "diabetes", "copd"]
# for var in risk_vars:
#     risk_vars[i] = "['" + risk_vars[i] + "']"
#     i += 1


class PatientVars:
    _risk_vars = ["vef", "sbp", "nyha", "current smoker", "diabetes", "copd"]
    # i = 0
    # for var in risk_vars:
    #     risk_vars[i] = "['" + risk_vars[i] + "']"
    #     i += 1

    def __init__(self):
        self.vef = []
        self.sbp = []
        self.nyha = []
        self.current_smoker = []
        self.diabetes = []
        self.copd = []
        dict = {}
        for key in self._risk_vars: 
            dict[key] = []
        self.dict = dict

    def addFinding(self, object):
        """ Adds RiskVar object to PatientVars dictionary based
        on the category of the RiskVar object
        """
        self.dict[object.cat].append(object)

    def process(self):
        """Processes all findings. Must be performed before querying results
        """
        self._detMissingAtrs()
        self._detAbundantAtrs()
        self._conflictAtrs()
        

    def _detMissingAtrs(self):
        """Add all keys of missing attributes to list self.missing
        """
        self.missing = []
        for key in self.dict:
            if not self.dict[key]:
                self.missing.append(key)

    def _detAbundantAtrs(self):
        """Compares for each attribute the findings if multiple findings
        """
        self.abundant = []
        for key in self.dict:
            atr = self.dict[key]
            if len(atr) > 1:
                self.abundant.append(key)

    def _conflictAtrs(self):
        """Keep track of all matching and conflicting findings per variable
        Stores them in a dictionary
        """
        # Initialize conflicts dictionary
        conflicts = {}
        for key in self.abundant: 
            conflicts[key] = {"match":[], "conflict":[]}

        if not self.abundant:
            self.conflicts = None
        
        else: 
            # Loop over variable objects per variable
            for key in self.abundant:
                for i in range(len(self.dict[key])):
                    for j in range(i+1, len(self.dict[key])):
                        match = self.dict[key][i] == self.dict[key][j]
                        if match:
                            conflicts[key]["match"].append(i,j)
                        else:
                            conflicts[key]["conflict"].append(i,j)
            self.conflicts = conflicts
            

    def getMissingAtrs(self):
        """Returns list of missing variables"""
        if not self.missing:
            print("No missing variables")
            return(None)
        else:
            print("Missing variables:")
            return(self.missing)

    def getConflictAtrs(self):
        """Returns dictionary with indices of conflicting findings"""
        if not self.conflicts:
            print("No conflicts found")
            return(None)
        else:
            print("Conflicts found. Dict is returned")
            return(self.conflicts)

    def getModScores(self):
        for key in self.dict:
            print(key)
            for finding in self.dict[key]:
                print(finding.negScore)



# %%
def parse_batch(context_dict):
    """Go over all patient context documents and create a 
    patient var object per patient, put in a returned dictionary.
    """
    result = {}
    for pat_id in context_dict:
        patient_vars = parse_object(context_dict[pat_id]["object"])
        result.update({pat_id : patient_vars})
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
    print(target.categoryString())
    risk_var = var_factory.createVar(target.categoryString(), target)
    # print("\n")
    # print("Target:", target.getCategory(), target.getPhrase(), target.getLiteral())
    mods = sent_markup[1].predecessors(target)
    for mod in mods:
        # print("mod:", mod.getCategory(), mod.getPhrase())
        risk_var.addMod(mod)
    risk_var.processInfo()
    return(risk_var)
            
var_factory = varFactory()
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
