# -*- coding: utf-8 -*-
try:
    import unittest2 as unittest
except ImportError:
    import unittest  # NOQA

import os
from flask_seed.tests.base import TestCase
from flask_seed.nextid import NextId
import json
from random import randint
from bson import ObjectId
from bson.json_util import dumps
from bson import json_util

class TestNextId(TestCase):
    print "NextId tests"
    print "=============="

    def test_nextid(self):
        nextId = NextId(self.db)

        response = nextId.nextId()

        args = {}

        assert response['status_code'] == 200
        data = response['response']
if __name__ == "__main__":
    unittest.main()
