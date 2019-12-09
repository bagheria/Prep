from abc import ABC, abstractmethod
import re
import pandas as pd
from pprint import pprint

from negation.structure2 import batch, constants, factory, patientObject, varObject


# Master Class
class modObject(ABC):
    def __init__(self):
        self.objects = []
    
    def _addModifierTag(self, tagObject):
        """Adds tagObject to end of self.objects list"""
        self.objects.append(tagObject)

    def isEmpty(self):
        if self.objects: return False
        else: return True


# Negation
class negMod(modObject):
    def __init__(self):
        super().__init__()

# Date
class dateMod(modObject):
    def __init__(self):
        super().__init__()

# Temporality
class tempMod(modObject):
    def __init__(self):
        super().__init__()

# Examination
class examMod(modObject):
    def __init__(self):
        super().__init__()