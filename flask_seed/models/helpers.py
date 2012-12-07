import datetime
import models

def recurseValidate(doc_class, key, val, doc_errors):
    '''this will be called by recursiveDoc function and be executed on each doc/embedded doc'''
    doc = doc_class(**val)
    errors = doc.validate()
    if errors:
        error = {'fld':key, '_cls': val['_cls'], 'errors': errors}
        if 'eId' in val and val['eId']:
            error['eId'] = val['eId']
        doc_errors.append(error)


def recurseVOnUpSert(doc_class, key, val, doc_errors):
    '''this will be called by recursiveDoc function and be executed on each doc/embedded doc'''
    if '_cls' in val:
        if hasattr(doc_class, 'vOnUpSert'):
            resp = doc_class.vOnUpSert(val)
            if resp['errors']:
                error = {'fld':key, '_cls': val['_cls'], 'errors': resp['errors']}
                if 'eId' in val and val['eId']:
                    error['eId'] = val['eId']
                doc_errors.append(error)

def recurseDoc(key, val, recurseFn, doc_errors):
    '''Recursively traverse model class fields executing validate on any docs/embedded docs'''
    keyvals = {}
    if type(val) == dict:
        doc_class = getattr(models, val['_cls']) if '_cls' in val else None
        if doc_class:
            # this enables using same recursive funct to execute something on any docs/embedded docs
            recurseFn(doc_class, key, val, doc_errors)
        for key in val.keys():
            # if not type(val[key]) == dict or key in ['_cls', '_types']:
            if key in ['_cls', '_types']:
                keyvals[key] = val[key]
                continue
            keyvals[key] = recurseDoc(key, val[key], recurseFn, doc_errors)
    elif type(val) == list:
        for i in range(len(val)):
            val[i] = recurseDoc(key, val[i], recurseFn, doc_errors)
        return val
    else:
        return val

    return keyvals

def recurseValidateAndVOnUpSert(m):
    '''recursively handle validate and execute any doc.vOnUpSert functions'''

    fields_to_process = m.fieldsToHandle()

    doc_errors = []
    m_data_handled = recurseDoc('doc', fields_to_process, recurseValidate, doc_errors)

    if doc_errors:
        return doc_errors

    doc_errors = []
    m_data_handled = recurseDoc('doc', fields_to_process, recurseVOnUpSert, doc_errors)

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
