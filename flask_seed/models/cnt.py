import datetime

from app import app
import models
from models import Mixin, Email, Note, MyDoc
import helpers

class Cnt(MyDoc, Mixin):
    code = app.db.StringField()

    def save(self, *args, **kwargs):
        now = datetime.datetime.now()

        if not self.id:
            self.cOn = self.oOn = now

        self.mOn = now

        errors = helpers.recurseValidateAndVOnUpSert(self)

        self._meta['collection'] = 'cnts'
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
    def vOnUpSert(d):
        errors = []
        d['dNam'] = d['fNam'] + ' ' + d['lNam']
        if not 'dNamS' in d or not d['dNamS']:
            d['dNamS'] = d['dNam'].lower().replace(' ', '_')
        if not 'slug' in d or not d['slug']:
            d['slug'] = d['dNamS']
        return {'doc_dict': d, 'errors': errors}

    def save(self, *args, **kwargs):
        super(Prs, self).save(*args, **kwargs)
