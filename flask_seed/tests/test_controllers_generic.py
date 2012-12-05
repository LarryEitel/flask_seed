import datetime
from copy import deepcopy
from core import BaseTestCase, BaseMongoTestCase
from bson import ObjectId
from utils import myyaml

class GenericControllersTests(BaseMongoTestCase):

    def test_prs(self):
        pass
        # from models import Email, Prs

        # cnts = myyaml.pyObj(self.tests_data_yaml_dir + 'cnts.yaml')

        # for doc_dict in cnts.itervalues():
        #     doc = Prs(**doc_dict)
        #     doc.save()
        #     assert doc.id
        #     coll = doc._get_collection()
        #     ret = coll.find_one({'_id': doc.id})
        #     pass
