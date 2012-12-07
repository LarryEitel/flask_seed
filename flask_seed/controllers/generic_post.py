# -*- coding: utf-8 -*-
import os
import re
import datetime
from bson import ObjectId
import models
import globals

class GenericPost(object):

    def __init__(self, g):
        #: Doc comment for instance attribute db
        self.usr = g['usr']
        self.db  = g['db']
        #self.es  = g['es']

    def post(self, **kwargs):
        '''Insert a doc
            newDocTmp: Initialize a temp (tmp) doc if no OID and no data.
            cloneDocTmp: Clone to a temp doc if OID and no isTmp flag set.
            upsertDocTmp: Update or Insert temp doc to base collection if OID and isTmp is set.
            insertDoc: Insert a new doc if no OID and there are more attributes than _c.
            '''
        db           = self.db

        response     = {}
        docs         = {}
        status       = 200

        usrOID       = self.usr['OID']
        docs_to_post = kwargs['docs']

        post_errors  = []
        total_errors = 0

        for doc_dict in docs_to_post:
            errors      = {}
            doc_info    = {}

            # required attribute
            _cls          = doc_dict['_cls']

            # shortcut
            doc_keys   = doc_dict.keys()

            modelClass = getattr(models, _cls)
            _id        = doc_dict['_id'] if '_id' in doc_keys else None
            where      = {'_id': ObjectId(_id)} if _id else None
            attrNam    = doc_dict['attrNam'] if 'attrNam' in doc_keys else None
            attr_c     = doc_dict['attr_c'] if attrNam else None
            attrVal    = doc_dict['attrVal'] if attrNam else None

            doc = modelClass(**doc_dict)
            resp = doc.save()
            if 'myErrors' in doc._data:
                error = {'doc_dict': doc_dict, 'errors': doc._data['myErrors']}
                post_errors.append(error)
            else:
                docs[doc.id]   = models.helpers.docCleanData(doc._data)

        response['total_inserted'] = len(docs.keys())

        if post_errors:
            response['total_invalid'] = len(post_errors)
            response['errors']        = post_errors
            status                    = 500
        else:
            response['total_invalid'] = 0

        response['docs'] = docs

        return {'response': response, 'status': status}