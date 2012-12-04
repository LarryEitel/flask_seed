import csv
import cStringIO
import datetime
import importlib
import os

from dateutil import relativedelta
from flask import (
    render_template,
    make_response,
    request,
    redirect,
    session,
    url_for,
    flash,
    abort,
    send_from_directory,
)

from flask_seed.app import app
from flask_seed.models import Q, Person
import flask_seed.util
from flask_seed.util import (
    slugify,
    make_start_date,
    make_end_date,
    month_ranges,
    log_exception,
    standard_deviation,
)
def robots():
    response = make_response(render_template('robots.txt'))
    content_type = response.headers['Content-type']
    content_type.replace('text/html', 'text/plain')
    return response

def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')
