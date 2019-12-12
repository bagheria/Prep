from abc import ABC, abstractmethod
import re
import pandas as pd
from pprint import pprint
from collections import abc

# from negation.structure2 import factory, constants, modObject, patientObject, varObject

class Batch(abc.Collection):
    def __init__(self):
        self.objects = {
            # "a" : {"c" : 1, "d" : 2}, 
            # "b" : {"c" : 5, "d" : 8}
            }

    def _addPatientObject(self, id, patObj):
        self.objects.update({id : patObj})

    def isEmpty(self):
        if not self.objects: return(False)
        else: return(True)


    def __contains__(self, x):
        return True if x in self.objects.keys() else False

    def __iter__(self):
        yield from self.objects.items()

    # def __next__(self):
    #     if self._n <= len(self.objects):
    #         result = self.objects[1]
    #         self.n += 1
    #         return result
    #     else:
    #         raise StopIteration        

    def __len__(self):
        return(len(self.objects))

# a = Batch()
# for key, value in a:
#     print("key:", key)
#     for type, object in value.items():
#         print("type", type)
#         print("object", object)