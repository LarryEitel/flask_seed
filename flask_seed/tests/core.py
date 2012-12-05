# -*- coding: utf-8 -*-
try:
    import unittest2 as unittest
except ImportError:
    import unittest  # NOQA

import datetime
import random
import os
import globals



class BaseTestCase(unittest.TestCase):
    def setUp(self):
        if os.environ.get('FLASK_SEED_SETTINGS'):
            os.environ['FLASK_SEED_SETTINGS'] = ''

        import default_settings
        default_settings.TEMPLATE_DEBUG = True
        from app import app
        from util import now

        app.config.from_object('default_settings')
        app.config['MONGODB_DB'] = 'flask_seed_unittest'
        app.config['DEBUG'] = True
        app.config['TESTING'] = True

        self.config = app.config
        self.app = app.test_client()
        self.flask_app = app

        self.used_keys = []
        self.now = now

class BaseMongoTestCase(unittest.TestCase):
    def setUp(self):
        if os.environ.get('FLASK_SEED_SETTINGS'):
            os.environ['FLASK_SEED_SETTINGS'] = ''

        import default_settings
        default_settings.TEMPLATE_DEBUG = True

        self.tests_data_yaml_dir = 'data/yaml/'

        from app import app
        from flask.ext.mongoengine import MongoEngine
        from util import now

        app.config.from_object('default_settings')
        app.config['MONGODB_DB'] = 'flask_seed_unittest'
        app.config['DEBUG'] = True
        app.config['TESTING'] = True
        app.db = MongoEngine(app)

        self._flush_db()

        self.config = app.config
        self.app = app.test_client()
        # self.flask_app = app

        self.g = globals.load()
        self.g['usr']         = {"OID": "50468de92558713d84b03fd7", "at": (-84.163063, 9.980516)}
        self.used_keys = []


    def tearDown(self):
        #self._flush_db()
        pass

    def _flush_db(self):
        from mongoengine.connection import _get_db
        db = _get_db()
        #Truncate/wipe the test database
        names = [name for name in db.collection_names() \
            if 'system.' not in name]
        [db.drop_collection(name) for name in names]

    def _get_target_url(self):
        raise NotImplementedError

    def _get_target_class(self):
        raise NotImplementedError

    def _make_one(self, *args, **kwargs):
        return self._get_target_class()(*args, **kwargs)

    def _get_card_class(self):
        from models import Kard
        return Kard

    def _get_record_class(self):
        from models import DailyRecord
        return DailyRecord

    def _make_unique_key(self):
        key = random.randint(1, 10000)
        if key not in self.used_keys:
            self.used_keys.append(key)
            return key
        return self._make_unique_key()

    def assertEqualDateTimes(self, expected, actual):
        expected = (expected.year, expected.month, expected.day, expected.hour, expected.minute)
        actual = (actual.year, actual.month, actual.day, actual.hour, actual.minute)
        self.assertEqual(expected, actual)
