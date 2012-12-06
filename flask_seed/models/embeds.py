import datetime

from app import app
import models
from models import MyEmbeddedDocument

class Email(MyEmbeddedDocument):
    typ     = app.db.StringField(required= True)
    address = app.db.StringField()
    prim    = app.db.BooleanField()
    dNam    = app.db.StringField()
    #eId    = app.db.SequenceField(primary_key=True, required= True)
    eId     = app.db.IntField()
    w       = app.db.FloatField()

    def __str__(self):
        s = ('[' + str(self.eId) + '] ') if self.eId else ''
        s += (self.typ + ': ') if self.typ else ''
        s += self.address if self.address else ''
        return s

    @staticmethod
    def vOnUpSert(rec):
        dNam = (rec['typ'] + ': ') if 'typ' in rec and rec['typ'] else ''
        dNam += rec['address'] if 'address' in rec and rec['address'] else ''
        rec['dNam'] = dNam
        return rec

class Mixin(object):
    cloned_id       = app.db.ObjectIdField()
    emails = app.db.ListField(
        app.db.EmbeddedDocumentField(Email),
    )
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