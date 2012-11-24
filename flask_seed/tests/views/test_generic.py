# -*- coding: utf-8 -*-
try:
    import unittest2 as unittest
except ImportError:
    import unittest  # NOQA

import os
from flask_seed.tests.base import TestCase
import json
import time
import datetime
import dateutil.parser
from flask import request
from random import randint
from bson import ObjectId
from bson.json_util import dumps
import isodate

class TestGeneric(TestCase):
    collection = 'Prs'
    collection_name = 'Prs'
    def test_post_one(self):
        print '''### INSERT NEW PERSON:'''

        host = self.host
        sample = {
            "fNam":"johnathan",
            "lNam":"doe",
            #"lvOn":{"$date": 1347893866298},
            "dOn":"$isodate:2012-09-14T17:41:32.471Z",
            "oBy":{"$oid":"50468de92558713d84b03fd0"},
            "rBy":{"$oid":"50468de92558713d84b03fd7"},
            "gen":'m',
            "emails" : [{
                "email" : "john@doe.com"
            }]
        }
        data = json.dumps(sample)
        route = "/" + self.collection
        addParams = {
            'verb'   : "POST",
            'host'   : host,
            'url'    : 'http://' + host + route,
            'route'  : route,
            'http'   : "HTTP/1.1",
            'headers': "\n".join(['content-type: application/json']),
            'data'   : data,
            'length' : len(data)
        }
        print "\n#### RAW REQUEST:\n%(verb)s %(url)s %(http)s\n%(headers)s\nHost: %(host)s\nContent-Length: %(length)i\n\n%(data)s\n" % addParams
        response = self.app.post('/test' + addParams['route'], data=addParams['data'])

        data = json.loads(response.data)
        if not response.status_code   == 200:
            print "FAILED: ", data
        assert response.status_code   == 200
        print "Success.\n#### RESPONSE:\n%s" % data

        assert data['total_inserted'] == 1

        doc = data['docs'][0]['doc']
        id  = data['docs'][0]['id']
        print "INSERTED OBJECT_ID:", id
        assert doc['fNam']            == sample['fNam']

if __name__ == "__main__":
    unittest.main()
