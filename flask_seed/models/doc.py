import datetime

from app import app
import models



def vDoc(key, val):
    '''Recursively traverse model class fields executing vOnUpsert functions found in doc.fields'''
    keyvals = {}
    if type(val) == dict:
        if '_cls' in val:
            doc_class = getattr(models, val['_cls'])
            if hasattr(doc_class, 'vOnUpsert'):
                val = doc_class.vOnUpsert(val)
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
    '''recursively look for fields with vOnUpsert function to handle'''
    m_data = m._data
    fields_to_process = {}
    for k, v in m_data.iteritems():
        if v and k:
            fields_to_process[k] = v

    m_data_handled = vDoc('doc', fields_to_process)

    # make sure base doc is handled
    if hasattr(m, 'vOnUpsert'):
        m_data_handled = m.vOnUpsert(m_data_handled)

    for field in m._fields.keys():
        if field in m_data_handled:
            setattr(m, field, m_data_handled[field])



    # return m.__class__(**m_data_handled)
    # return m


def docCleanData(m_data):
    '''Models contains some fields with keys and/or vals == None. Return dict with only value keys that also have value'''
    ks = {}
    for k, v in m_data.iteritems():
        if v and k:
            ks[k] = v

    return ks

class Email(app.db.EmbeddedDocument):
    typ = app.db.StringField(required=True)
    address = app.db.StringField(required=True)
    prim = app.db.BooleanField()
    dNam = app.db.StringField()
    #eId = app.db.SequenceField(primary_key=True, required= True)
    w = app.db.FloatField()

    def __str__(self):
        return self.address

    @staticmethod
    def vOnUpsert(rec):
        rec['dNam'] = rec['address'] + 'test'
        return rec


class Mixin(object):
    cloned_id       = app.db.ObjectIdField()
    emails = app.db.ListField(
        app.db.EmbeddedDocumentField(Email),
    )
    dNam = app.db.StringField()
    dNamS = app.db.StringField()

    sId = app.db.SequenceField()

    oBy       = app.db.ObjectIdField()
    oOn = app.db.DateTimeField(required=True)
    cBy       = app.db.ObjectIdField()
    cOn = app.db.DateTimeField(required=True)
    mBy       = app.db.ObjectIdField()
    mOn = app.db.DateTimeField(required=True)
    dOn = app.db.DateTimeField()
    dBy = app.db.ObjectIdField()


#class Mixin2(object):
    #dNam = app.db.StringField()
    #dNamS = app.db.StringField()
    #sId = app.db.SequenceField()

#class Doc(app.db.Document, Mixin2):
    #dNam = app.db.StringField()
    #meta           = {
        #'collection'               : 'test',
        #}
    #def save(self, *args, **kwargs):
        #now = datetime.datetime.now()

        #self = handleVirtualModelFunctions(self)
        #super(Doc, self).save(*args, **kwargs)


class Cnt(app.db.Document, Mixin):
    code = app.db.StringField()
    meta           = {
        'collection'               : 'cnts',
        'allow_inheritance'        : True,
        }

    def save(self, *args, **kwargs):
        now = datetime.datetime.now()

        if not self.id:
            self.cOn = self.oOn = now

        self.mOn = now


        handleVirtualModelFunctions(self)

        super(Cnt, self).save(*args, **kwargs)


class Cmp(Cnt):
    symbol = app.db.StringField()

class Prs(Cnt):
    # namePrefix
    prefix    = app.db.StringField()

    # givenName
    fNam      = app.db.StringField()

    # additionalName
    fNam2     = app.db.StringField()

    # givenName
    lNam      = app.db.StringField()
    lNam2     = app.db.StringField()

    # nameSuffix
    suffix    = app.db.StringField()
    gen       = app.db.StringField()
    rBy       = app.db.ObjectIdField()


    @staticmethod
    def vOnUpsert(rec):
        rec['dNam'] = rec['fNam'] + ' ' + rec['lNam']
        return rec

    def save(self, *args, **kwargs):
        super(Prs, self).save(*args, **kwargs)