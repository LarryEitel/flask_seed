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
import usecase
import models

class UseCasesTests(BaseMongoTestCase):

    def test_run(self):
    	cmds = usecase.run(self.tests_data_yaml_dir, 'usecases', 'test')
	assert len(cmds) == 2


if __name__ == "__main__":
    unittest.main()
