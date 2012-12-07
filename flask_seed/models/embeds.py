import datetime

from app import app
import models
from models import MyEmbedDoc
from models.myfields import MyStringField, MyEmailField

class EmbedMixin(object):
    typ     = MyStringField(required= True)
    dNam    = app.db.StringField()
    dNamS   = app.db.StringField()
    #eId    = app.db.SequenceField(primary_key=True, required= True)
    eId     = app.db.IntField()
    w       = app.db.FloatField()
    prim    = app.db.BooleanField()

class Tel(MyEmbedDoc, EmbedMixin):
    text = MyStringField(required= True)

class Note(MyEmbedDoc, EmbedMixin):
    #address = app.db.EmailField(required= True)
    title = MyStringField(required= True)
    body    = app.db.StringField()
    tels = app.db.ListField(app.db.EmbeddedDocumentField(Tel))

    def __str__(self):
        s = ('[' + str(self.eId) + '] ') if self.eId else ''
        s += (self.typ + ': ') if self.typ else ''
        s += self.title if self.title else ''
        return s

    @staticmethod
    def vOnUpSert(d):
        errors = []
        dNam = (d['typ'] + ': ') if 'typ' in d and d['typ'] else ''
        dNam += d['title'].lower() if 'title' in d and d['title'] else ''
        d['dNam'] = dNam
        d['dNamS'] = d['title'].lower().replace(' ', '_')
        return {'doc_dict': d, 'errors': errors}

class Email(MyEmbedDoc, EmbedMixin):
    address = MyEmailField(required= True)
    notes = app.db.ListField(app.db.EmbeddedDocumentField(Note))

    def __str__(self):
        s = ('[' + str(self.eId) + '] ') if self.eId else ''
        s += (self.typ + ': ') if self.typ else ''
        s += self.address if self.address else ''
        return s

    @staticmethod
    def vOnUpSert(d):
        errors = []
        dNam = (d['typ'] + ': ') if 'typ' in d and d['typ'] else ''
        dNam += d['address'].lower() if 'address' in d and d['address'] else ''
        d['dNam'] = dNam
        d['dNamS'] = d['address'].lower()
        return {'doc_dict': d, 'errors': errors}

class Mixin(object):
    emails = app.db.ListField(app.db.EmbeddedDocumentField(Email))
    notes = app.db.ListField(app.db.EmbeddedDocumentField(Note))
    dNam = app.db.StringField()
    dNamS = app.db.StringField()
    slug = app.db.StringField()

    sId = app.db.SequenceField()

    oBy = app.db.ObjectIdField()
    oOn = app.db.DateTimeField()
    cBy = app.db.ObjectIdField()
    cOn = app.db.DateTimeField()
    mBy = app.db.ObjectIdField()
    mOn = app.db.DateTimeField()
    dOn = app.db.DateTimeField()
    dBy = app.db.ObjectIdField()