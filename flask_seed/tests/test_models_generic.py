import datetime
from copy import deepcopy
from core import BaseTestCase, BaseMongoTestCase
from bson import ObjectId
from utils import myyaml

def docCleanData(m_data):
    ks = {}
    for k, v in m_data.iteritems():
        if v and k:
            ks[k] = v

    return ks

def docCloneToTmp(m, tmpClass):
    m_dict = m._data
    ks = {}
    for k, v in m_dict.iteritems():
        if v and k:
            ks[k] = v

    ks['cloned_id'] = m.id
    del ks['sId']
    return tmpClass(**ks)

def docClone(m):
    m_dict = m._data
    ks = {}
    for k, v in m_dict.iteritems():
        if v and k:
            ks[k] = v

    ks['cloned_id'] = m.id
    del ks['sId']
    return m.__class__(**ks)

class GenericTests(BaseTestCase):
    def setUp(self):
        #super(GenericTests, self).setUp()
        pass

    def test_one(self):
        assert True

class GenericMongoTests(BaseMongoTestCase):
    def setUp(self):
        super(GenericMongoTests, self).setUp()

    def test_prs(self):
        from models import Email, Prs

        cnts = myyaml.pyObj(self.tests_data_yaml_dir + 'cnts.yaml')

        for doc_dict in cnts.itervalues():
            doc = Prs(**doc_dict)
            doc.save()
            assert doc.id

        assert prs.dNam == 'Larry King'

        prs.fNam = 'Wayne'
        prs.save()
        assert prs.dNam == 'Wayne King'

        resp = Prs.objects.get(pk=prs.id)
        assert resp.fNam == prs.fNam

        pass


    #def test_vNam(self):
        #doc_dict = \
        #{
          #"_id" : ObjectId("50be37ed936aa21380e1a982"),
          #"_types" : ["Cnt", "Cnt.Prs"],
          ##"updated_at" : ISODate("2012-12-04T11:50:37.89Z"),
          #"lNam" : "King",
          #"_cls" : "Cnt.Prs",
          #"fNam" : "Larry",
          #"sId" : 2,
          #"emails" : [{
              #"_types" : ["Email"],
              #"_cls" : "Email",
              #"address" : "steve@apple.com"
            #}, {
              #"_types" : ["Email"],
              #"_cls" : "Email",
              #"address" : "bill@ms.com"
            #}]
        #}
        #print doc_dict
