import os

import path

from flask import Flask
from flask.ext.mongoengine import MongoEngine
from jinja2 import ModuleLoader
from flask_debugtoolbar import DebugToolbarExtension


from util import (
    slugify,
    timesince,
    timeuntil,
    jsonencode,
    configure_logging,
    newrelic_head,
    newrelic_foot,
    FixGunicorn
)

def get_app():
    app = Flask('flask_seed')
    app.config.from_object('default_settings')
    if os.getenv('FLASK_SEED_SETTINGS', None):
        app.config.from_envvar('FLASK_SEED_SETTINGS')

    app.secret_key = app.config['SECRET_KEY']

    # app.g  = globals.load()
    app.db = MongoEngine(app)

    app.jinja_env.add_extension('util.Markdown2Extension')
    app.jinja_env.filters['slugify'] = slugify
    app.jinja_env.filters['timesince'] = timesince
    app.jinja_env.filters['timeuntil'] = timeuntil
    app.jinja_env.filters['jsonencode'] = jsonencode
    app.jinja_env.globals['newrelic_head'] = newrelic_head
    app.jinja_env.globals['newrelic_foot'] = newrelic_foot

    if not app.config.get('TEMPLATE_DEBUG', True):
        compiled_templates = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'compiled_templates')
        compiled_files = path.path(compiled_templates).files()
        if len(compiled_files) <= 1:
            app.jinja_env.compile_templates(compiled_templates, zip=None, py_compile=True)
        app.jinja_env.loader = ModuleLoader(compiled_templates)

    return app

app = get_app()
toolbar = DebugToolbarExtension(app)
