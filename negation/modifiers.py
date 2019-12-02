from abc import ABC, abstractmethod
from datetime import datetime
import pandas as pd


class Modifier(ABC):
    def __init__(self, object):
        self._object = object
        self.phrase = object.getPhrase()
        self.type = object.categoryString()
        self.literal = object.getLiteral()
        self._setSubClass()
        self._process()

    def __eq__(self, other):
        if self.value == other.value:
            return(True)
        else:
            return(False)
    
    @abstractmethod
    def _process(self):
        pass
    
    # def __str__(self):
    #     return(str(vars(self)))

    @abstractmethod
    def _setSubClass(self):
        pass

    def view(self):
        dict = {
            "phrase" : self.phrase,
            "type" : self.type,
            "literal" : self.literal,
            "value" : self.value,
            "subClass" : self.subClass
        }
        return(dict)

    def getDataframe(self):
        # Initialize dataframe
        df = pd.DataFrame()

        # # Approach: via view()
        # dictionary = self.view()
        # for key, value in dictionary.items():
        #     mod_series = pd.Series(data=value, name=key)
        #     df.insert(0, mod_series.name, mod_series, True)

        # Approach: via atributes
        var_ls = vars(self)
        for var in var_ls:
            # Skip "private" variables
            if var[0] != "_":
                mod_series = pd.Series(data=getattr(self, var), name=var)
                df.insert(0, mod_series.name, mod_series, True)
        
        df = df.add_prefix("mod_")
        return(df)


class ExamMod(Modifier):
    def __init__(self, object):

        return super().__init__(object)

    def _setSubClass(self):
        self.subClass = "examination"

    def _process(self):
        self.value = self.type

class NegMod(Modifier):
    def __init__(self, object):

        return super().__init__(object)
    
    def _setSubClass(self):
        self.subClass = "negation"

    def _process(self):
        string = self.type
        if string == "definite_negated_existence":
            score = -2
        elif string == "probable_negated_existence":
            score = -1
        elif string == "probable_existence":
            score = 1
        elif string == "definite_existence":
            score = 2
        # ambivalent negation:
        elif string == "ambivalent_existence":
            score = 0
        elif string == "pseudoneg":
            score = 0
        else:
            raise Exception(
                "Negation category not recognized. \nCategory:",
                string)
        self.value = score


class DateMod(Modifier):
    def __init__(self, object):

        return super().__init__(object)

    def _setSubClass(self):
        self.subClass = "date"

    def _process(self):
        string = self.phrase
        # 19xx
        if self.literal == "20st century year":
            result = datetime.strptime(
                string, '%Y').date()
        # 20xx
        elif self.literal == "21st century year":
            result = datetime.strptime(
                string, '%Y').date()
        # dd/mm/yyyy
        elif self.literal == "day-month-year":
            try:
                result = datetime.strptime(
                    string, '%d-%m-%Y').date()
            except ValueError:
                try:
                    result = datetime.strptime(
                        string, '%d/%m/%Y').date()
                except ValueError:
                    raise Exception(
                        "Date string could not be converted to datetime object",
                        string, self.literal)
        # yyyy/mm/dd
        elif self.literal == "year-month-day":
            try:
                result = datetime.strptime(
                    string, '%Y-%m-%d').date()
            except ValueError:
                try:
                    result = datetime.strptime(
                        string, '%Y/%m/%d').date()
                except ValueError:
                    raise Exception(
                        "Date string could not be converted to datetime object",
                        string, self.literal)
        # mm/dd/yyy
        elif self.literal == "month-day-year":
            try:
                result = datetime.strptime(
                    string, '%m-%d-%Y').date()
            except ValueError:
                try:
                    result = datetime.strptime(
                        string, '%m/%d/%Y').date()
                except ValueError:
                    raise Exception(
                        "Date string could not be converted to datetime object",
                        string, self.literal)
        # yyyy/dd/mm
        elif self.literal == "year-day-month":
            try:
                result = datetime.strptime(
                    string, '%Y-%d-%m').date()
            except ValueError:
                try:
                    result = datetime.strptime(
                        string, '%Y/%d/%m').date()
                except ValueError:
                    raise Exception(
                        "Date string could not be converted to datetime object",
                        string, self.literal)        
        self.value = result

class TempMod(Modifier):
    def __init__(self, object):

        return super().__init__(object)

    def _setSubClass(self):
        self.subClass = "temporality"

    def _process(self):
        self.value = self.type
