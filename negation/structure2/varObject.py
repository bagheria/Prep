from abc import ABC, abstractmethod
import re
import pandas as pd
from pprint import pprint

from negation.structure2 import batch, constants, factory, modObject, patientObject


# Master Class
class varObject(ABC):
    def __init__(self):
        self.objects_tag = []
        self.objects_mod = []
    
    def _addTargetTag(self, tagObject):
        """Adds tagObject to end of self.objects list.
        Also adds modObjects of each type to self.objects_mod
        """
        self.objects_tag.append(tagObject)
        self.objects_mod.append(fact.createModObject())
    
    def _addModifiers(self, mods):
        for mod in mods:
            cat = mod.categoryString()

            # Translate cat into modifier type:
            found = False
            for key, list in constants.mod_type_dict.items():
                if cat in list:
                    type = key
                    # select last dict from mod object list:
                    self.objects_mod[-1][type]._addModifierTag(mod)
                    found = True
                    # Can skip remainder of loop
                    break
            # If type not found:
            if not found:
                raise Exception("categoryString of mod was not recognized")
            
            

    def isEmpty(self):
        if self.objects: return False
        else: return True


# Binary
class binVar(varObject):
    def __init__(self):
        super().__init__()

# Factorial
class factVar(varObject):
    def __init__(self):
        super().__init__()

# Numeric
class numVar(varObject):
    def __init__(self):
        super().__init__()


fact = factory.Factory()