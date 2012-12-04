#!/usr/bin/env python

import datetime
import random
import os

import unittest2


class BaseTestCase(unittest2.TestCase):
    def setUp(self):
        if os.environ.get('FLASK_SEED_SETTINGS'):
            os.environ['FLASK_SEED_SETTINGS'] = ''

        from flask_seed import default_settings
        default_settings.TEMPLATE_DEBUG = True
        from flask_seed.app import app
        from flask_seed.util import now

        app.config.from_object('flask_seed.default_settings')
        app.config['DEBUG'] = True
        app.config['TESTING'] = True

        self.config = app.config
        self.app = app.test_client()
        self.flask_app = app

        self.used_keys = []
        self.now = now

        super(BaseTestCase, self).setUp()

class BaseMongoTestCase(BaseTestCase):
    def setUp(self):
        app = self.app
        from flask.ext.mongoengine import MongoEngine
        delattr(app, 'db')
        from mongoengine.connection import connect, disconnect
        disconnect()

        app.config['MONGODB_DB'] = 'flask_seed_unittest'
        connect(app.config['MONGODB_DB'])
        app.db = MongoEngine(app)
        self.app = app

        super(BaseMongoTestCase, self).setUp()

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
        from flask_seed.models import Kard
        return Kard

    def _get_record_class(self):
        from flask_seed.models import DailyRecord
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
