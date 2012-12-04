import datetime
from copy import deepcopy
from models import Person
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
        name = "Larry"
        person = Person.objects.get(name=name)
        assert person.name == name


