# -*- coding: utf-8 -*-
try:
    import unittest2 as unittest
except ImportError:
    import unittest  # NOQA

import datetime
from core import BaseMongoTestCase
from bson import ObjectId
from utils import myyaml
import models
import controllers

class ControllersGenericPostTests(BaseMongoTestCase):

    def test_post_new(self):
        ucs = self.usecase
        ucs.load('usecases')
        samp_prss = ucs.uc_dat['prs']
        larry_stooge = samp_prss['larry_stooge']

        fn = controllers.generic_post.GenericPost(self.g)

        # try one doc
        resp = fn.post(**{'docs': [larry_stooge]})
        assert resp['status'] == 200
        assert len(resp['response']['docs']) == 1

        # try several docs
        multiple_docs = samp_prss.values()
        resp = fn.post(**{'docs': multiple_docs})
        assert resp['status'] == 200
        assert len(resp['response']['docs']) == len(multiple_docs)

        # test validation including embedded docs!

if __name__ == "__main__":
    unittest.main()