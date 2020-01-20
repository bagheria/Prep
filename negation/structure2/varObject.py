from abc import ABC, abstractmethod
import re
import pandas as pd
from pprint import pprint
from collections import abc

from negation.structure2 import batch, constants, factory, modObject, patientObject


# Master Class
class varObject(abc.Collection):
    def __init__(self):
        self.objects = []
        # self.objects_tag = []
        # self.objects_mod = []
    
    def _addTargetTag(self, tagObject):
        """Adds tagobject, and dictionary of mods,
        as dictionary to self.objects list:
        self.objects = [
            {
            "instance" : tagObject, 
            "mods" : 
                {
                "negation" : negMod, 
                "date" : dateMod,
                etc
                }
            },
            {
            "instance" : tagObject, 
            "mods" : 
                {
                "negation" : negMod, 
                "date" : dateMod,
                etc
                }
            }
        ]
        """
        # """Adds tagObject to end of self.objects list.
        # Also adds modObjects of each type to self.objects_mod
        # """
        # self.objects_tag.append(tagObject)
        # self.objects_mod.append(fact.createModObject())

        # Put everything in 
        self.objects.append({
            "instance" : tagObject, 
            "mods" : fact.createModObject()})

    def _addModifiers(self, mods):
        for mod in mods:
            cat = mod["category"]

            # Translate cat into modifier type:
            found = False
            # Lookup in which modObject subclass this cat belongs
            for key, list in constants.mod_type_dict.items():
                if cat in list:
                    type = key
                    # select last dict from mod object list:
                    self.objects[-1]["mods"][type]._addModifierTag(mod)
                    found = True
                    # Can skip remainder of loop
                    break
        
            # If type for this mod not found:
            if not found:
                raise Exception("categoryString of mod was not recognized")
            
    def __str__(self):
        result = []
        for i in self.objects: 
            result.append(i["instance"])
        return(str(result))

    def isEmpty(self):
        if self.objects: return False
        else: return True

    def __contains__(self, x):
        for i in self.objects:
            if x in i["instance"].values():
                return(True)
            # if x[1] == i["instance"][x[0]]:
            #     return(True)
        return(False)

    def __iter__(self):
        """Iterates over self.objects list and returns:
        (var, varObject)
        """
        for i in self.objects:
            yield (i["instance"], i["mods"])



    # def __next__(self):
    #     if self._n <= len(self.objects):
    #         result = self.objects[1]
    #         self.n += 1
    #         return result
    #     else:
    #         raise StopIteration        

    def __len__(self):
        """Returns the number of instances
        """
        return(len(self.objects))
    
    def _getType(self):
        return(str(type(self).__name__))

    def getDataframe(self):
        """Returns dataframe of varObject"""
        # If no findings, return empty dataframe
        if len(self) == 0:
            return(pd.DataFrame())

        ls = []
        for index, i in enumerate(self.objects):
            # Per instance, gather var information
            data = i["instance"]
            # var_index = str(self._getType()+str(index))
            var_index = str(i["instance"]["var"]+str(index))
            data.update({"index" : var_index})
            serie = pd.Series(data)
            df_var = pd.DataFrame([serie])
            df_var = df_var.add_prefix("var_")

            # Determine number of mod combinations, so number of rows
            n_mod_comb = sum([len(mod) for mod in i["mods"].values()])
            
            # If there are no mods, return current df
            if n_mod_comb == 0:
                ls.append(df_var)

            # Paste mod info to dataframe as new columns
            else:
                # Gather all modifier information 
                df_mods = []
                for mod in i["mods"].values():
                    if not mod.isEmpty():
                        df_mods.append(mod.getDataframe())
                df_mods = pd.concat(df_mods, axis=0, ignore_index=True)
                
                # Combine dataframes:
                # Only if mods are present

                if len(df_mods) == 0:
                    raise Exception(
                        "df_mod contains no rows")
                # Multiply rows of vars to match number of mods
                df_var = pd.concat([df_var]*n_mod_comb, ignore_index=True)
                # Combine var columns with mod columns
                df_comb = pd.concat([df_mods, df_var], axis=1)
                # Add var df to list
                ls.append(df_comb)

        # concatenate rows of dataframes into 1 dataframe
        df = pd.concat(ls, axis=0, ignore_index=True, sort=False)#.reset_index()
        # Set dict keys as column names instead of row indeces.
        # df = df.transpose()

        return(df)

    def process(self):
        # Activate processing of mod objects:
        for i in self.objects:
            for mod in i["mods"].values():
                mod.process()

        # Process information in var level:
        self._addInfo()

    @abstractmethod
    def _addInfo(self):
        pass

    def getSummary(self):
        """Combines summary of mods with var findings.
        Number of rows is number of instances of var found
        """
        ls = []
        for i in self.objects:
            # Get info of varObject
            var_dict = i["instance"]

            # Get summary info of mods
            mods_sum_dict = self._getSummaryMods(i["mods"])

            dict_comb = {**var_dict , **mods_sum_dict}
            ls.append(dict_comb)

        df = pd.DataFrame(ls)
        return(df)

    def _getSummaryMods(self, mod_dict):
        """Returns a 1 row df with summary information of one finding's mods
        """
        summaries_dict = {}
        for type, mod_obj in mod_dict.items():
            summaries_dict.update(mod_obj._summarize())
        
        return(summaries_dict)
        # df = pd.DataFrame.from_dict([summaries_dict], orient="columns")
        # return(df)


    # @abstractmethod
    # def _summarize(self):
    #     pass

# Binary
class binVar(varObject):
    def __init__(self):
        super().__init__()

    def _summarize(self):
        pass

    def _addInfo(self):
        """Nothing to process, all info is in modifiers
        for binary risk variables
        """
        pass


# Factorial
class factVar(varObject):
    def __init__(self):
        super().__init__()

    def _summarize(self):
        pass

    def _addInfo(self):
        """ Processes subtype into factor and corresponding integer
        """
        for i in self.objects:
            # get factor string
            factor = i["instance"]["subtype"]
            
            # Process factor string into factor integer
            fact_int = self._nyha_to_int(factor)

            # Update dictionary with new variables:
            i["instance"].update({
                "factor" : factor,
                "factInt" : fact_int
            })

    def _nyha_to_int(self, string):
        for j in constants.nyha_factors:
            if string == j[0]:
                integer = j[1]
                return(integer)
        # If no string was recognized after looping through list:
        raise Exception(
                "String not recognized as NYHA factor",
                "factor:", string)
        


# Numeric
class numVar(varObject):
    def __init__(self):
        super().__init__()

    def _summarize(self):
        pass

    def _getVef(self, phrase):
        """Returns list with one value, or two values in case of a range
        """
        # Search for pattern with outer characters digits
        string = re.search(pattern = r"\d(.*)\d", string = phrase)
        if string is None:
            raise Exception(
                "No value found when searching in phrase of numeric variable",
                phrase)
        # If there are no other other characters within string 
        # that are no digits, value is just the string 
        if re.search(pattern=r"\D", string=string.group()) is None:
            return([int(string.group())])

        # Else, it is a range, so split up values
        else:
            values = re.findall(pattern = r"\d+", string=string.group())
            range_list = []
            for value in values: range_list.append(int(value))
            if len(range_list) != 2:
                raise Exception("Phrase recognized as range, but no 2 values",
                phrase, string.group(), values, range_list)
            return(range_list)


    def _getSbp(self, phrase):
        "Returns list with value"
        string = re.search(pattern = r"\d{2,3}(?=/(\d{2,3}))", string = phrase)
        if string is None:
            raise Exception(
                "No value found when searching in phrase of numeric variable",
                self.phrase)
        else:
            return([int(string.group())])

    def _addInfo(self):
        """Processes information and adds it to dictionary of instance;
        self.objects[i]["instance"]
        """
        for i in self.objects:
            data = i["instance"]
            # Get values
            if data["var"] == "vef":
                values = self._getVef(data["phrase"])
            elif data["var"] == "sbp":
                values = self._getSbp(data["phrase"])
            else:
                raise Exception(
                    "Numeric var finding category not recognized",
                    "var:", data["var"],
                    "phrase:", data["phrase"])


            # Check if list
            if len(values) > 1:
                isRange = True
            else: isRange = False

            # update information:
            data.update({
                "values" : values,
                "isRange" : isRange
            })
            i["instance"] = data

    

fact = factory.Factory()