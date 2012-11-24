# -*- coding: utf-8 -*-
try:
    import unittest2 as unittest
except ImportError:
    import unittest  # NOQA

import sys, os

sys.path.insert(0, "..")
sys.path.insert(0, os.getcwd() + os.sep + 'flask_seed')

import os
import base64
import json

from flask import session

import flask_seed.run as run
from flask_seed import models
from flask_seed.utils import load_data
from pymongo import Connection

class TestCase(unittest.TestCase):

    def setUp(self):
        app                   = run.app
        app.config['TESTING'] = True
        self.host             = app.config['TESTING_HOST']
        app    = app.test_client()
        
        dbhost = app.application.config['MONGO_HOST']
        dbname = app.application.config['MONGO_TEST_DBNAME']
        db     = Connection(dbhost)[dbname]

        # delete existing test db
        db.connection.drop_database(dbname)

        # recreate
        db       = Connection(dbhost)[dbname]
        self.db  = db
        self.app = app

    def tearDown(self):
        pass
        # clean after testing
        #models.db.session.remove()

        # self.es.delete_index_if_exists(self.index_name)

if __name__ == "__main__":
    unittest.main()
