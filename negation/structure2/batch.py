from abc import ABC, abstractmethod
import re
import pandas as pd
from pprint import pprint

from negation.structure2 import factory, constants, modObject, patientObject, varObject

class Batch:
    def __init__(self):
        self.objects = {}

    def _addPatientObject(self, id, patObj):
        self.objects.update({id : patObj})

    def isEmpty(self):
        if not self.objects: return(False)
        else: return(True)

    def len(self):
        return(len(self.objects))