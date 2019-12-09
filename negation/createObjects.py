from negation.structure2 import batch, constants, factory, modObject, patientObject, varObject

# Object to instantiate other objects:
fact = factory.Factory()

def parse_batch(context_dict, calculator):
    """Go over all patient context documents and create a 
    patient var object per patient, put in a returned dictionary.
    """
    # Instantiate batch object
    result = fact.createBatchObject()

    # For every context document
    # Make patientObject and put it in batchObject with
    # patient ID as key
    for pat_id, context_doc in context_dict.items():
        init_patient = fact.createPatientObject(calculator)
        pat_obj = parse_object(context_doc["object"], init_patient)
        result._addPatientObject(pat_id, pat_obj)
        
    print(result.len(), "patient objects have been created.")
    return(result)


def parse_object(context_doc, patient_obj):
    """
    Go over all targets in a patient ContextDocument and add
    These findings to the patient_vars object
    """

    section_markups = context_doc.getSectionMarkups()
    for sent_markup in section_markups:
        # print(sent_markup[1])
        targets = sent_markup[1].getMarkedTargets()
        for target in targets:
            mods = get_target_mods(target, sent_markup)
            # add targets and corresponding mod to patientObj
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