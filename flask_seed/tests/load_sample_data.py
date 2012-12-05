import datetime
from bson import ObjectId
from utils import myyaml

def go():
    from models import Email, Prs

    cnts = myyaml.pyObj(self.tests_data_yaml_dir + 'cnts.yaml')

    for doc_dict in cnts.itervalues():
        doc = Prs(**doc_dict)
        doc.save()
        assert doc.id
        coll = doc._get_collection()
        ret = coll.find_one({'_id': doc.id})
        pass
