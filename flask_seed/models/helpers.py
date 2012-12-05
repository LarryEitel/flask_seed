import datetime
import models

doc_errors = []
def vDoc(key, val):
    '''Recursively traverse model class fields executing vOnUpSert functions found in doc.fields'''
    global doc_errors
    keyvals = {}
    if type(val) == dict:
        doc_class = getattr(models, val['_cls']) if '_cls' in val else None
        if doc_class:
            if hasattr(doc_class, 'myValidate'):
                errors = doc_class.myValidate(val)
                if errors:
                    error = {'fld':key, '_cls': val['_cls'], 'errors': errors}
                    if 'eId' in val and val['eId']:
                        error['eId'] = val['eId']
                    doc_errors.append(error)
            if '_cls' in val:
                if hasattr(doc_class, 'vOnUpSert'):
                    val = doc_class.vOnUpSert(val)
        for key in val.keys():
            if key in ['_cls', '_types']:
                return val
            keyvals[key] = vDoc(key, val[key])
    elif type(val) == list:
        for i in range(0, len(val)):
            val[i] = vDoc(key, val[i])
        return val
    else:
        return val

    return keyvals

def handleVirtualModelFunctions(m):
    '''recursively look for fields with vOnUpSert function to handle'''
    global doc_errors
    doc_errors = []
    m_data = m._data
    fields_to_process = {}
    for k, v in m_data.iteritems():
        if v and k:
            fields_to_process[k] = v

    m_data_handled = vDoc('doc', fields_to_process)

    if hasattr(m.__class__, 'myValidate'):
        errors = m.myValidate(m_data_handled)
        if errors:
            error = {'_cls':m._cls, 'errors': errors}
            doc_errors.append(error)

    if doc_errors:
        return doc_errors

    # make sure base doc is handled
    if hasattr(m, 'vOnUpSert'):
        m_data_handled = m.vOnUpSert(m_data_handled)

    for field in m._fields.keys():
        if field in m_data_handled:
            setattr(m, field, m_data_handled[field])

    return m





def docCleanData(m_data):
    '''Models contains some fields with keys and/or vals == None. Return dict with only value keys that also have value'''
    ks = {}
    for k, v in m_data.iteritems():
        if v and k:
            ks[k] = v

    return ks

#def docCleanData(m_data):
    #ks = {}
    #for k, v in m_data.iteritems():
        #if v and k:
            #ks[k] = v

    #return ks

#def docCloneToTmp(m, tmpClass):
    #m_dict = m._data
    #ks = {}
    #for k, v in m_dict.iteritems():
        #if v and k:
            #ks[k] = v

    #ks['cloned_id'] = m.id
    #del ks['sId']
    #return tmpClass(**ks)

#def docClone(m):
    #m_dict = m._data
    #ks = {}
    #for k, v in m_dict.iteritems():
        #if v and k:
            #ks[k] = v

    #ks['cloned_id'] = m.id
    #del ks['sId']
    #return m.__class__(**ks)
