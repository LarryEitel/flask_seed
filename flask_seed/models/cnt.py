import datetime

from app import app
import models
from models import Mixin, Email, MyDocument
import helpers

class Cnt(MyDocument, Mixin):
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

        errors = helpers.handleVirtualModelFunctions(self)

        if type(errors) == list:
            self._data['myErrors'] = errors
        else:
            super(Cnt, self).save(*args, **kwargs)


class Cmp(Cnt):
    symbol = app.db.StringField()

class Prs(Cnt):
    # namePrefix
    prefix    = app.db.StringField()

    # givenName
    fNam      = app.db.StringField(required= True)

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
    def vOnUpSert(rec):
        rec['dNam'] = rec['fNam'] + ' ' + rec['lNam']
        if not 'dNamS' in rec or not rec['dNamS']:
            rec['dNamS'] = rec['dNam'].lower().replace(' ', '_')
        if not 'slug' in rec or not rec['slug']:
            rec['slug'] = rec['dNamS']
        return rec

    def save(self, *args, **kwargs):
        super(Prs, self).save(*args, **kwargs)
