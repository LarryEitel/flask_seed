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
import models

class UseCasesTests(BaseMongoTestCase):

    def test_run(self):
        ucs = self.usecase
        ucs.load('usecases')
        cmds = ucs.run_all('test')
        assert len(cmds) == 2
        cmds = ucs.run(['add', 'Prs', 'noemail'])
        assert len(cmds) == 1


if __name__ == "__main__":
    unittest.main()