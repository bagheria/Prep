from abc import ABC, abstractmethod
import re
import pandas as pd
from pprint import pprint
from collections import abc

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

    def __contains__(self, x):
        """Checks of value x is in instances
        Should be specified per subtype
        """
        pass

    def __iter__(self):
        yield from self.objects

    # def __next__(self):
    #     if self._n <= len(self.objects):
    #         result = self.objects[1]
    #         self.n += 1
    #         return result
    #     else:
    #         raise StopIteration        

    def __len__(self):
        return(len(self.objects))


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