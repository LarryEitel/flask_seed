import datetime
import models

def myValidate(key, val, doc_errors):
    '''Recursively traverse model class fields executing validate on any docs/embedded docs'''
    keyvals = {}
    if type(val) == dict:
        doc_class = getattr(models, val['_cls']) if '_cls' in val else None
        if doc_class:
            doc = doc_class(**val)
            errors = doc.validate()
            if errors:
                error = {'fld':key, '_cls': val['_cls'], 'errors': errors}
                if 'eId' in val and val['eId']:
                    error['eId'] = val['eId']
                doc_errors.append(error)

        for key in val.keys():
            if key in ['_cls', '_types']:
                keyvals[key] = val[key]
                continue
            keyvals[key] = myValidate(key, val[key], doc_errors)
    elif type(val) == list:
        for i in range(0, len(val)):
            val[i] = myValidate(key, val[i], doc_errors)
        return val
    else:
        return val

    return keyvals

def vOnUpSert(key, val, doc_errors):
    '''Recursively traverse model class fields executing vOnUpSert functions found in doc.fields'''
    keyvals = {}
    if type(val) == dict:
        doc_class = getattr(models, val['_cls']) if '_cls' in val else None
        if doc_class:
            if '_cls' in val:
                if hasattr(doc_class, 'vOnUpSert'):
                    val = doc_class.vOnUpSert(val)
        for key in val.keys():
            if key in ['_cls', '_types']:
                keyvals[key] = val[key]
                continue
            keyvals[key] = vOnUpSert(key, val[key], doc_errors)
    elif type(val) == list:
        for i in range(0, len(val)):
            val[i] = vOnUpSert(key, val[i], doc_errors)
        return val
    else:
        return val

    return keyvals

def handleVirtualModelFunctions(m):
    '''recursively look for fields with vOnUpSert function to handle'''

    m_data = m._data
    fields_to_process = {}
    for k, v in m_data.iteritems():
        if v and k:
            fields_to_process[k] = v

    fields_to_process['_cls'] = m._cls
    fields_to_process['_types'] = [m._cls]

    doc_errors = []
    myValidate('doc', fields_to_process, doc_errors)

    if doc_errors:
        return doc_errors

    doc_errors = []
    m_data_handled = vOnUpSert('doc', fields_to_process, doc_errors)

    if doc_errors:
        return doc_errors

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
