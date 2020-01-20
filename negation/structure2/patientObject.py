from abc import ABC, abstractmethod
import re
import pandas as pd
from pprint import pprint
from collections import abc

from negation.structure2 import batch, constants, factory, modObject, varObject


class patientObj(abc.Collection):
    """Stores all set variables of a particular patient in 
    attribute: self.objects which is a dictionary with
    key = patient ID, value = list of varObjects
    self.objects = {
        "copd" : varObject,
        "vef" : varObject,
        "nyha" : varobject,
        etc
    }
    """ 
    def __init__(self, calcs):

        # If calcs is just a string instead of list
        # Put in a list
        if not isinstance(calcs, list):
            calcs = [calcs]

        # check if calcs are in calculators list from constants
        if not set(calcs).issubset(constants.calculators):
            raise Exception(
        "Unknown calculator is given in calcs argument",
        "calcs given:", calcs)

        obj_dictionary = {}
        # For every calculator
        for calc in calcs:
            # Put the variable names in the dictionary
            # and add a varObject
            for var in constants.vars_incl[calc]:
                obj_dictionary.update({
                    # key as var, and var determiens type 
                    # of varObject
                    var : fact.createVarObject(var)})
        
        # initialize objects with dictionary with items:
        # key = var, value = varObject
        self.objects = obj_dictionary

    def getVarNames(self):
        """Returns all variable names
        """
        return(self.objects.keys())


    def _addFindings(self, target, mods):
        """Adds the target and corresponding mod to the 
        var object corresponding to the target's risk variable
        """
        var = target['var']
        self.objects[var]._addTargetTag(target)
        self.objects[var]._addModifiers(mods)

    def __contains__(self, x):
        """Checks if patient self has at least one target finding
        in variable x
        """
        return(not self.objects[x].isEmpty())

    def __iter__(self):
        """Iterates over self.objects dictionary and returns:
        (var, varObject)
        """
        yield from self.objects.items()

    # def __next__(self):
    #     if self._n <= len(self.objects):
    #         result = self.objects[1]
    #         self.n += 1
    #         return result
    #     else:
    #         raise StopIteration        

    def __len__(self):
        """Returns the number of vars for patient with at least
        1 finding:
        """
        n = 0
        for varObject in self.objects.values():
            if not varObject.isEmpty():
                n = n + 1
        return(n)

    def getDataframe(self):
        ls = []
        for i in self.objects.values():
            df = i.getDataframe()
            # df = df.insert(
            #     loc = 0, column="colname", value=id, allow_duplicates = False)
            ls.append(df)
        df = pd.concat(ls, axis=0, ignore_index=True, sort=False).reset_index()

        return(df)


    def process(self):
        for var, varObj in self:
            varObj.process()

    def getSummary(self):
        """Combines all variable finding dataframes
        into one larger dataframe
        Appends var
        """
        df_list = []
        for var, var_obj in self.objects.items():
            var_df = var_obj.getSummary()
            # Index to varIndex
            var_df['varIndex'] = var_df.index

            # Insert column with var = key
            var_df['var'] = var

            # add df to list
            df_list.append(var_df)

        # Append all dataframes 
        df = pd.concat(df_list, axis=0, sort=False, ignore_index=True)
        df.reset_index()
        return(df)


fact = factory.Factory()