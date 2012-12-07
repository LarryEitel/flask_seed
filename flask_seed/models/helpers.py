import datetime
import models

def recurseValidate(doc_class, key, val, attrPath, doc_errors):
    '''this will be called by recursiveDoc function and be executed on each doc/embedded doc'''
    doc = doc_class(**val)
    errors = doc.validate()
    if errors:
        error = {'attrPath': '.'.join(attrPath), 'fld':key, '_cls': val['_cls'], 'errors': errors}
        if 'eId' in val and val['eId']:
            error['eId'] = val['eId']
        doc_errors.append(error)


def recurseVOnUpSert(doc_class, key, val, attrPath, doc_errors):
    '''this will be called by recursiveDoc function and be executed on each doc/embedded doc'''
    if '_cls' in val:
        if hasattr(doc_class, 'vOnUpSert'):
            resp = doc_class.vOnUpSert(val)
            if resp['errors']:
                error = {'attrPath': '.'.join(attrPath), 'fld':key, '_cls': val['_cls'], 'errors': resp['errors']}
                if 'eId' in val and val['eId']:
                    error['eId'] = val['eId']
                doc_errors.append(error)

def recurseDoc(key, val, recurseFn, attrPath, doc_errors):
    '''Recursively traverse model class fields executing validate on any docs/embedded docs'''
    keyvals = {}
    if type(val) == dict:
        doc_class = getattr(models, val['_cls']) if '_cls' in val else None
        if doc_class:
            # this enables using same recursive funct to execute something on any docs/embedded docs
            recurseFn(doc_class, key, val, attrPath, doc_errors)
        for key in val.keys():
            if key in ['_cls', '_types']:
                keyvals[key] = val[key]
                continue
            keyvals[key] = recurseDoc(key, val[key], recurseFn, attrPath + [key], doc_errors)
    elif type(val) == list:
        for i in range(len(val)):
            thisId = str(val[i]['eId'] if 'eId' in val[i] and val[i]['eId'] else i)
            val[i] = recurseDoc(key, val[i], recurseFn, attrPath + [thisId], doc_errors)
        return val
    else:
        return val

    return keyvals

def recurseValidateAndVOnUpSert(m):
    '''recursively handle validate and execute any doc.vOnUpSert functions'''

    fields_to_process = m.fieldsToHandle()

    doc_errors = []
    attrPath = [m._cls, m.id if m.id else 'new']
    m_data_handled = recurseDoc(m._cls, fields_to_process, recurseValidate, attrPath, doc_errors)

    if doc_errors:
        return doc_errors

    doc_errors = []
    attrPath = [m._cls, m.id if m.id else 'new']
    m_data_handled = recurseDoc(m._cls, fields_to_process, recurseVOnUpSert, attrPath, doc_errors)

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
