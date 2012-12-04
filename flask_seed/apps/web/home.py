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

import datetime
from flask_seed import controllers
from flask_seed.util import (
    slugify,
    make_start_date,
    make_end_date,
    month_ranges,
    log_exception,
    standard_deviation,
)


def index():
    # name = "Larry"
    # person = Person.objects.get(name=name)
    person = controllers.person.getPerson()
    date = datetime.datetime.now()
    date = make_end_date(date=date)

    title = app.config.get('SITE_NAME')

    context = {
        'person': person.name,
        'title': 'title: ' + person.name,
        'date': date,
        'updated_at': datetime.datetime.now(),
        'version': '0.001',
    }
    return render_template('home.html', **context)

app.add_url_rule('/', 'home', index)