# -*- coding: utf-8 -*-
try:
    import unittest2 as unittest
except ImportError:
    import unittest  # NOQA

import datetime
from copy import deepcopy
from core import BaseTestCase, BaseMongoTestCase
from bson import ObjectId
from utils import myyaml

class GenericModelsTests(BaseMongoTestCase):
    def setUp(self):
        super(GenericModelsTests, self).setUp()

    def test_prs(self):
        uc = self.usecase
        from models import Email, Prs

        uc.load('usecases')
        cmds = uc.run_all('one')
        assert len(cmds) == 2


if __name__ == "__main__":
    unittest.main()