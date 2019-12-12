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
            for key, list in constants.mod_type_dict.items():
                if cat in list:
                    type = key
                    # select last dict from mod object list:
                    self.objects[-1]["mods"][type]._addModifierTag(mod)
                    found = True
                    # Can skip remainder of loop
                    break
            # If type not found:
            if not found:
                raise Exception("categoryString of mod was not recognized")
            
            

    def isEmpty(self):
        if self.objects: return False
        else: return True

    def __contains__(self, x):
        """Checks if value is present in variable: Depends on subtype
        """
        pass

    def __iter__(self):
        """Iterates over self.objects dictionary and returns:
        (var, varObject)
        """
        yield from self.objects

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