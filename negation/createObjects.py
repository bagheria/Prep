import negation.structure2 as classObjects


def parse_batch(context_dict):
    """Go over all patient context documents and create a 
    patient var object per patient, put in a returned dictionary.
    """
    result = {}
    for pat_id in context_dict:
        patient_vars = parse_object(context_dict[pat_id]["object"])
        # patient_vars.process()
        result.update({pat_id : patient_vars})
    print(len(result), "patient objects have been created.")
    return(result)




def parse_object(context_doc):
    """
    Go over all targets in a patient ContextDocument and add
    These findings to the patient_vars object
    """
    patient_obj = factory.factory.createPatientObject()
    section_markups = context_doc.getSectionMarkups()
    for sent_markup in section_markups:
        # print(sent_markup[1])
        targets = sent_markup[1].getMarkedTargets()
        for target in targets:
            mods = get_target_mods(target, sent_markup)
            patient_obj._addFindings(target, mods)
    return(patient_obj)
    

def get_target_mods(target, sent_markup):
    """
    Create risk variable object for every finding found,
    add modifiers to these objects, process the information in the object,
    and return it to be added to patient object
    """
    # print(target.categoryString())
    # var_object = factory.createVar(target.categoryString(), target)
    # print("\n")
    # print("Target:", target.getCategory(), target.getPhrase(), target.getLiteral())
    mods_list = []
    mods = sent_markup[1].predecessors(target)
    for mod in mods:
        # print("mod:", mod.getCategory(), mod.getPhrase())
        # var_object.objecs_mod._addModifier(mod)
        mods_list.append(mod)
    # risk_var.processInfo()
    return(mods_list)