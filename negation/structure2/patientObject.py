from abc import ABC, abstractmethod
import re
import pandas as pd
from pprint import pprint

from negation.structure2 import batch, constants, factory, modObject, varObject


class patientObj(ABC):
    """Stores all set variables of a particular patient in 
    attribute: self.objects which is a dictionary with
    key = patient ID, value = list of varObjects
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

    def _addFindings(self, target, mods):
        """Adds the target and corresponding mod to the 
        var object corresponding to the target's risk variable
        """
        var = target.categoryString()
        self.objects[var]._addTargetTag(target)
        self.objects[var]._addModifiers(mods)


fact = factory.Factory()