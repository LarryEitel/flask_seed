from flask import Flask, request, session

import json
import sys, os

sys.path.insert(0, "..")

from views import generic
from bson.json_util import dumps
from extensions import RegexConverter
from settings import Config

from flask.ext.pymongo import PyMongo
import models

app = Flask(__name__)

# Wanna make sure test db is used if /test/ in url
try:
    if '/test/' in request.url:
        Config.TESTING = True
        # escfg = Config.ES_TEST
except:
    pass

app.config.from_object(Config)

mongo     = PyMongo()
app.mongo = mongo
mongo.init_app(app)

# add regex for routing
app.url_map.converters['regex'] = RegexConverter


##################### POST
# This regex was breaking on /Usr!!!!!
# @app.route( '/<regex("[\w]*[Ss]"):class_name>', methods=['POST'])
@app.route( '/test/<class_name>', methods=['POST'])
@app.route( '/<class_name>', methods=['POST'])
# @requires_auth
def post(class_name):
    if not class_name in Config.DOMAIN.keys():
        abort(404)
    response = generic.post(class_name)
    return response

##################### GET
@app.route( '/', methods=['GET'])
@app.route( '/test/', methods=['GET'])
def home():
    return generic.home(Config.DOMAIN.keys())

def main():
    app.host = sys.argv['-h'] if '-h' in sys.argv else '127.0.0.1'
    if '-t' in sys.argv:
        app.config['TESTING'] = True
        print 'Running in test mode.'
    app.debug = '-d' in sys.argv
    app.use_reloader = '-r' in sys.argv
    app.run()

if __name__ == '__main__':
    main()
