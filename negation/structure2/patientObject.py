from abc import ABC, abstractmethod
from negation.structure2 import constants as constants
import re
import pandas as pd
from pprint import pprint

class patientObj(ABC):
    def __init__(self, calcs):

        # If calcs is just a string instead of list
        # Put in a list
        if not isinstance(calc, list):
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
            for var in constants.var_incl[calc]:
                obj_dictionary.update({
                    var : factory.createVarObject(var)})
        self.objects = obj_dictionary

    def _addFindings(self, target, mods):
        var = target.categoryString()
        self.objects[var]._addTarget(target)
        self.objects[var]._addModifiers(mods)