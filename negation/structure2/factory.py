import negation.structure2 as structure
from structure import batch as batch

class Factory:
    def __init__(self):
        pass

    def createPatientObject(self):
        pass

    def createVarObject(self, var_given):
        # print("type:", type)

        # Determine subclass of varObject for this 
        for type, var in constants.var_type_dict:
            if var_given == var:
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

factory = Factory()

