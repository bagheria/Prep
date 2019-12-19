from abc import ABC, abstractmethod
import re
import pandas as pd
from pprint import pprint
from collections import abc
from datetime import datetime

from negation.structure2 import batch, constants, factory, patientObject, varObject


# Master Class
class modObject(abc.Collection):
    def __init__(self):
        self.objects = []
    
    def _addModifierTag(self, tagObject):
        """Adds tagObject to end of self.objects list"""
        self.objects.append(tagObject)

    def isEmpty(self):
        if self.objects: return False
        else: return True

    def getDataframe(self):
        if self.isEmpty():
            return(pd.DataFrame())

        ls = []
        for index, instance in enumerate(self.objects):
            # Set name of series to "<Classname><index>"
            instance.update({"index" : str(self)+str(index)})
            serie = pd.Series(instance)
            df = pd.DataFrame([serie])
            ls.append(df)

        # concat all separate dataframes:
        df = pd.concat(ls, ignore_index=True, sort=False)#.reset_index()
        df = df.add_prefix("mod_")
        return(df)

    def getSummary(self):
        # Get summary dictionary
        data = self._summarize()
        return(pd.DataFrame([data]))

    def __contains__(self, x):
        """Checks if value x is in instances
        (Should be specified per subtype)
        """
        for i in self.objects:
            if x in i.values():
                return(True)

        return(False)

    def __iter__(self):
        yield from self.objects

    def __str__(self):
        """Returns name of class"""
        return(type(self).__name__)

    def __repr__(self):
        return(repr(self.objects))
    # def __next__(self):
    #     if self._n <= len(self.objects):
    #         result = self.objects[1]
    #         self.n += 1
    #         return result
    #     else:
    #         raise StopIteration        

    def __len__(self):
        return(len(self.objects))

    def process(self):
        if not self.isEmpty():
            self._addInfo()

    @abstractmethod
    def _addInfo(self):
        pass

    # @abstractmethod
    # def _addInfo(self):
    #     pass
    #     # for instance in self.objects:
    #     #     x = instance[inp_key]
    #     #     result = func(x)
    #     #     instance.update({outp_key : x})
    
    # @abstractmethod
    # def _summarize(self):
    #     pass


# Negation
class negMod(modObject):
    def __init__(self):
        super().__init__()

    def _addInfo(self):
        """Adds negation score and isNegated property
        to dictionary"""
        for i in self.objects:
            score = self._processNegation(i["category"])
            if score > 0:
                isNegated = False
            elif score < 0:
                isNegated = True
            else:
                isNegated = None
            i.update({
                "score" : score,
                "isNegated" : isNegated
            })

    def _processNegation(self, string):
        """Converts negation type into negation score"""
        if string == "definite_negated_existence":
            return(-2)
        elif string == "probable_negated_existence":
            return(-1)
        elif string == "probable_existence":
            return(1)
        elif string == "definite_existence":
            return(2)
        # ambivalent negation:
        elif string == "ambivalent_existence":
            return(0)
        elif string == "pseudoneg":
            return(0)
        else:
            raise Exception(
                "Negation category not recognized. \nCategory:",
                string)


    def _summarize(self):
        """Processes summary information for this modObject"""
        findings = self.objects

        # Number of observations
        n = len(findings)

        # Put main values of findings in a list:
        ls = []
        key = "isNegated"
        if n > 0:
            for i in findings:
                ls.append(i[key])
        # Transform list into set
        ls = set(ls)

        # Conflicting values
        if len(ls) > 1: conflict = True
        else: conflict = False

        # conflict = not any(dict[key] > otherDict[key] for key in dict)
        # If less then 2 observations, no conflict possible

        # isNegated
        if len(ls) == 1:
            isNegated = list(ls)[0]
        else: isNegated = None

        # return as dictionary
        prefix = "neg_"
        return({
            f"{prefix}n" : n,
            f"{prefix}conflict" : conflict,
            f"{prefix}isNegated" : isNegated
        })




# Date
class dateMod(modObject):
    def __init__(self):
        super().__init__()


    def _addInfo(self):
        for i in self.objects:
            date = self._processDate(i["phrase"], i["term"])
            year = int(date.year)
            i.update({
                "date" : date,
                "year" : year
            })

    def _processDate(self, phrase, date_type):
        """Gets the phrase from the TagObject and converts it into a datetime object
        Stores this object into self._date"""
        string = phrase
        # 19xx
        if date_type == "20st century year":
            result = datetime.strptime(
                string, '%Y').date()
            return(result)
        # 20xx
        elif date_type == "21st century year":
            result = datetime.strptime(
                string, '%Y').date()
            return(result)
        # dd/mm/yyyy
        elif date_type == "day-month-year":
            try:
                result = datetime.strptime(
                    string, '%d-%m-%Y').date()
                return(result)
            except ValueError:
                try:
                    result = datetime.strptime(
                        string, '%d/%m/%Y').date()
                    return(result)
                except ValueError:
                    raise Exception(
                        "Date string could not be converted to datetime object",
                        string, date_type)
        # yyyy/mm/dd
        elif date_type == "year-month-day":
            try:
                result = datetime.strptime(
                    string, '%Y-%m-%d').date()
                return(result)
            except ValueError:
                try:
                    result = datetime.strptime(
                        string, '%Y/%m/%d').date()
                    return(result)
                except ValueError:
                    raise Exception(
                        "Date string could not be converted to datetime object",
                        string, date_type)
        # mm/dd/yyy
        elif date_type == "month-day-year":
            try:
                result = datetime.strptime(
                    string, '%m-%d-%Y').date()
                return(result)
            except ValueError:
                try:
                    result = datetime.strptime(
                        string, '%m/%d/%Y').date()
                    return(result)
                except ValueError:
                    raise Exception(
                        "Date string could not be converted to datetime object",
                        string, date_type)
        # yyyy/dd/mm
        elif date_type == "year-day-month":
            try:
                result = datetime.strptime(
                    string, '%Y-%d-%m').date()
                return(result)
            except ValueError:
                try:
                    result = datetime.strptime(
                        string, '%Y/%d/%m').date()
                    return(result)
                except ValueError:
                    raise Exception(
                        "Date string could not be converted to datetime object",
                        string, date_type)        

    def _summarize(self):
        """Processes summary information for this modObject"""
        findings = self.objects

        # Number of observations
        n = len(findings)

        # Put main values of findings in a list:
        ls = []
        key = "year"
        if n > 0:
            for i in findings:
                ls.append(i[key])
        # Transform list into set
        ls = set(ls)

        # Conflicting values
        if len(ls) > 1: conflict = True
        else: conflict = False

        # conflict = not any(dict[key] > otherDict[key] for key in dict)
        # If less then 2 observations, no conflict possible

        # min, median and max
        try:
            mini = min(ls)
        except ValueError:
            mini = None
        try:
            maxi = max(ls)
        except ValueError:
            maxi = None

        # return as dictionary
        prefix = "date_"
        return({
            f"{prefix}n" : n,
            f"{prefix}conflict" : conflict,
            f"{prefix}min" : mini,
            f"{prefix}max" : maxi
        })


# Temporality
class tempMod(modObject):
    def __init__(self):
        super().__init__()

    def _addInfo(self):
        pass

    def _summarize(self):
        findings = self.objects

        # Number of observations
        n = len(findings)

        # Put main values of findings in a list:
        ls = []
        key = "concl"
        if n > 0:
            for i in findings:
                ls.append(i[key])
        # Transform list into set
        ls = set(ls)

        # Conflicting values
        if len(ls) > 1: conflict = True
        else: conflict = False

        # conflict = not any(dict[key] > otherDict[key] for key in dict)
        # If less then 2 observations, no conflict possible

        if len(ls) != 1:
            concl = None
        else: concl = list(ls)[0] 

        prefix = "date_"
        return({
            f"{prefix}n" : n,
            f"{prefix}conflict" : conflict,
            f"{prefix}concl" : concl
        })

# Examination
class examMod(modObject):
    def __init__(self):
        super().__init__()

    def _addInfo(self):
        pass    def _summarize(self):
        findings = self.objects

        # Number of observations
        n = len(findings)

        # Put main values of findings in a list:
        ls = []
        key = "concl"
        if n > 0:
            for i in findings:
                ls.append(i[key])
        # Transform list into set
        ls = set(ls)

        # Conflicting values
        if len(ls) > 1: conflict = True
        else: conflict = False

        # conflict = not any(dict[key] > otherDict[key] for key in dict)
        # If less then 2 observations, no conflict possible

        if len(ls) != 1:
            concl = None
        else: concl = list(ls)[0] 

        prefix = "date_"
        return({
            f"{prefix}n" : n,
            f"{prefix}conflict" : conflict,
            f"{prefix}concl" : concl
        })