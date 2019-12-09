from abc import ABC, abstractmethod
import re
import pandas as pd
from pprint import pprint

# Master Class
class varObject(ABC):
    def __init__(self):
        self.objects_tag = []
        self.objects_mod = []
    
    def _addTarget(self, tagObject):
        """Adds tagObject to end of self.objects list.
        Also adds modObjects of each type to self.objects_mod"""
        self.objects_tag.append(tagObject)
        self.objects_mod.append(factory.createModObject())
    
    def _addModifiers(self, mods):
        for mod in mods:
            type = mod.categoryString()
            # select last dict from mod object list:
            self.objects._mod[-1][type]._addModifier(mod)
            

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
