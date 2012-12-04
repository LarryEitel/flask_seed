import datetime
from copy import deepcopy

from tests.core import BaseTestCase, BaseMongoTestCase

class GenericTests(BaseTestCase):
    def setUp(self):
        #super(GenericTests, self).setUp()
        pass

    def test_one(self):
        assert True

class GenericMongoTests(BaseMongoTestCase):
    def setUp(self):
        #super(GenericMongoTests, self).setUp()
        pass


    def test_person(self):
        assert True