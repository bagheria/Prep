import negation.modifiers as modifiers
from abc import ABC, abstractmethod
import re

class RiskVar(ABC):
    
    def __init__(self, object):
        self.object = object
        self.literal = object.getLiteral()
        self.cat = object.categoryString()
        self.phrase = object.getPhrase()

        self._setType()

        # Modification initialization
        self.mod = []
        self.negation = {
            "score" : [],
            "polarity" : None,
            "conflict" : None}
        self.date = []
        self.temp = []
        self.exam = []
        
        # General post_process attributes
        self.result = []

    @abstractmethod
    def __eq__(self, other):
        pass

    @abstractmethod 
    def _setType(self):
        pass

    @abstractmethod
    def getOverview(self):
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
            self._processMod()
        self._analyseNeg()
                
    # Check for modification
    def _processMod(self):
        """Processes modifier information:
        """
        for mod in self.mod:
            if isinstance(mod, modifiers.ExamMod):
                self.exam.append(mod.value)
            elif isinstance(mod, modifiers.NegMod):
                self.negation["score"].append(mod.value)
            elif isinstance(mod, modifiers.DateMod):
                self.date.append(mod.value)
            elif isinstance(mod, modifiers.TempMod):
                self.temp.append(mod.value)
            else:
                raise Exception(
                    "Mod not recognized as one of valid options",
                    mod, mod.phrase, mod.type, mod.literal)

    def _analyseNeg(self):
        """Checks negation scores of finding.
        If negation scores contradict eachother, a conflict is noted
        If no conflict, negation can be determined to be "positive" (not negated)
        or "negative" (negated).
        """
        # If the finding has no negation modifiers, 
        # we assume it is positive
        if not self.negation["score"]:
            self.negation["conflict"] = False
            self.negation["polarity"] = "positive"

        
        else:
            # Sets can't have duplicates
            set_neg = set(self.negation["score"])
            pos = any(n > 0 for n in set_neg)
            neg = any(n < 0 for n in set_neg)
            oth = any(n == 0 for n in set_neg)

            if len(set_neg) > 1 and pos and neg:
                self.negation["conflict"] = True
            else:
                self.negation["conflict"] = False

            if not self.negation["conflict"]:
                if pos:
                    self.negation["polarity"] = "positive"
                if neg:
                    self.negation["polarity"] = "negative"


class NumVar(RiskVar):

    def __init__(self, object):
        # Numeric post_process attributes
        self.rec_values = []
        self.value = None
        self.values_conflict = None
        return super().__init__(object)
    
    def __eq__(self, other):
        return(self.value == other.value)

    def _setType(self):
        self.type = "numeric"

    def processInfo(self):
        super().processInfo()
        self._getValue()
        self._conflictValue()
        self._processValue()
        self._setResult()

    def _getValue(self):
        if self.cat == "vef":
            self._getValueVef()
        elif self.cat == "sbp":
            self._getValueSbp()
        else:
            raise Exception("Numeric variable, but not recognized as vef or sbp",
                self.phrase)

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
            self.value.append(string.group())
        # Else, it is a range, so split up values
        else:
            values = re.findall(pattern = r"\d+", string=string.group())
            range_list = []
            for value in values: range_list.append(value)
            if len(range_list) != 2:
                raise Exception("Phrase recognized as range, but no 2 values",
                self.phrase, string.group(), values, range_list)
            self.value.append(range_list)

    def _getValueSbp(self):
        string = re.search(pattern = r"\d{2,3}(?=/(\d{2,3}))", string = self.phrase)
        if string is None:
            raise Exception(
                "No value found when searching in phrase of numeric variable",
                self.phrase)
        else:
            self.value.append(string.group())

    def _conflictValue(self):
        ranges = []
        ints = []
        for i in self.value:
            if isinstance(i, int):
                ints.append(i)
            elif isinstance(i, list):
                ranges.append(i)
            else:
                raise Exception("No int and no list in self.values")
        
        if len(set(ints)) > 1:
            return True
        
        if any(isinstance(i, list) for i in self.value) \
            or len(set(self.rec_values)) > 1:
            self.values_conflict = True
        else:
            self.values_conflict = False

    def _processValue(self):
        if not self.values_conflict:
            self.value = self.rec_values[0]
        else: 
            self.value = False
    
    def _setResult(self):
        self.result = {
            "negation" : self.negation["polarity"],
            "value" : self.rec_values}

    def getOverview(self):
        return({"value" : self.rec_values, "negation" : self.negation["polarity"]})
    
class BinVar(RiskVar):

    def __init__(self, object):
        return super().__init__(object)

    def __eq__(self, other):
        if self.negation["conflict"] or other.negation["conflict"]:
            return False
        elif self.negation["polarity"] == other.negation["polarity"]:
            return True
        elif self.negation["polarity"] is not other.negation["polarity"]:
            return False
        else:
            raise Exception("__eq__ evaluation unseen outcome of:\n",
                self.negation,"\n", other.negation)

    def _setType(self):
        self.type = "binary"

    def processInfo(self):
        super().processInfo()
        self._setResult()
    
    def _setResult(self):
        self.result = {"negation" : self.negation["polarity"]}

    def getOverview(self):
        return({"negation" : self.negation["polarity"]})
        

class FactVar(RiskVar):

    def __init__(self, object):
        self.factor = None
        return super().__init__(object)

    def __eq__(self, other):
        if self.negation["conflict"] or other.negation["conflict"]:
            neg = False
        elif self.negation["polarity"] == other.negation["polarity"]:
            neg = True
        elif self.negation["polarity"] is not other.negation["polarity"]:
            neg = False
        else:
            raise Exception("__eq__ evaluation unseen outcome of:\n",
                self.negation,"\n", other.negation)
        if self.factor == other.factor and neg:
            return True 
        else:
            return False
        

    def _setType(self):
        self.type = "factorial"
    
    def processInfo(self):
        super().processInfo()
        self._processFactor()
        self._setResult()

    def _processFactor(self):
        self.factor = self.literal    

    def _setResult(self):
        self.result = {
            "negation" : self.negation["polarity"],
            "factor" : self.factor}
    
    def getOverview(self):
        return({"factor" : self.factor, "negation" : self.negation["polarity"]})            
    
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

