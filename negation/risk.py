# %%
numeric_vars = ["age", "vef", "sbp", "bmi", "creatinine"]
factorial_vars = ["nyha"]
binary_vars = ["gender", "current smoker", "diabetes", "copd", 
    "heart failure", "beta blocker", "acei"]

class RiskVar:
    def __init__(self, object):
        self.object = object
        self.mod = []
        self.cat = object.getCategory()

    def addMod(self, mod):
        self.mod.append(mod)

    def processInfo(self):
        self.phrase = self.object.getPhrase()

class NumVar(RiskVar):
    def __init_subclass__(cls):
        return super().__init_subclass__()

    def processRange(self):
        string = self.phrase
        
    
# class NumVar(RiskVar):

# %%
# class PatientVars:
#     def __init__(self):
#         self.vef = []
#         self.sbp = []
#         self.nyha = []
#         self.current_smoker = []
#         self.diabetes = []
#         self.copd = []

#     def setVef(self, vef):
#         self.vef.append(vef)

# %%
# i = 0
# risk_vars = ["vef", "sbp", "nyha", "current_smoker", "diabetes", "copd"]
# for var in risk_vars:
#     risk_vars[i] = "['" + risk_vars[i] + "']"
#     i += 1


class PatientVars:
    risk_vars = ["vef", "sbp", "nyha", "current smoker", "diabetes", "copd"]
    # i = 0
    # for var in risk_vars:
    #     risk_vars[i] = "['" + risk_vars[i] + "']"
    #     i += 1

    def __init__(self):
        self.vef = []
        self.sbp = []
        self.nyha = []
        self.current_smoker = []
        self.diabetes = []
        self.copd = []
        dict = {}
        for key in self.risk_vars: 
            dict[key] = []
        self.dict = dict

    def addFinding(self, object):
        for cat in object.cat:
            self.dict[cat].append(object)

    def getMissingAtrs(self):
        for key in self.dict:
            if len(self.dict[key]) == 0:
                print(key)

    def getConflictAtrs(self):
        for key in self.dict:
            if len(self.dict[key]) > 1:
                print(key)



# %%
def parse_batch(context_dict):
    result = {}
    for pat_id in context_dict:
        patient_vars = parse_object(context_dict[pat_id]["object"])
        result.update({pat_id : patient_vars})
    return(result)


def parse_object(context_doc):
    patient_vars = PatientVars()
    section_markups = context_doc.getSectionMarkups()
    for sent_markup in section_markups:
        # print(sent_markup[1])
        targets = sent_markup[1].getMarkedTargets()
        for target in targets:
            finding = parse_findings(target, sent_markup)
            patient_vars.addFinding(finding)
    return(patient_vars)
    

def parse_findings(target, sent_markup):
    risk_var = RiskVar(target)
    print("\n")
    print("Target:", target.getCategory(), target.getPhrase(), target.getLiteral())
    mods = sent_markup[1].predecessors(target)
    for mod in mods:
        print("mod:", mod.getCategory(), mod.getPhrase())
        risk_var.addMod(mod)
    return(risk_var)
            

# %%
context_doc = context_obj[11]["object"]
pat3 = parse_object(context_doc)

# %%
result1 = parse_batch(context_obj)