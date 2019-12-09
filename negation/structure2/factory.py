from negation.structure2 import constants


class Factory:
    
    def __init__(self):
        pass


    def createBatchObject(self):
        from negation.structure2 import batch
        return(batch.Batch())


    def createPatientObject(self, calculators):
        """Calculators can be a name of single calculator (str),
        or list of multiple calculators (str)
        """
        from negation.structure2 import patientObject
        return(patientObject.patientObj(calculators))


    def createVarObject(self, var_given):
        from negation.structure2 import varObject
        # print("type:", type)

        # Determine subclass of varObject for this 
        for type, var_list in constants.var_type_dict.items():
            if var_given in var_list:
                make_type = type
                if type == "binary":
                    return(varObject.binVar())
                if type == "factorial":
                    return(varObject.factVar())
                if type == "numeric":
                    return(varObject.numVar())
        else:
            raise Exception(
                "Variable type not recognized:",
                "var given:", type)

   
    def createModObject(self):
        """Returns a dictionary with keys the types of modObject
        and values the corresponding modObject type"""
        from negation.structure2 import modObject

        dictionary = {
            "negation" : modObject.negMod(),
            "date" : modObject.dateMod(),
            "examination" : modObject.examMod(),
            "temporality" : modObject.tempMod()
        }
        return(dictionary)

        # if type in constants.examination_mods:
        #     return(modObject.ExamMod(object))
        # elif type in constants.negation_mods:
        #     return(modObject.NegMod(object))
        # elif type in constants.date_mods:
        #     return(modObject.DateMod(object))
        # elif type in constants.temporality_mods:
        #     return(modObject.TempMod(object))
        # else:
        #     raise Exception("Modifier type not recognized:",
        #     type, object)
