EXAPI
##############

REST-API being built using python, flask, mongodb and pymongo.

Key Services and Tools
============

    mongodb
    python
    flask
    pymongo
    schematics

Make it run!
============

To make it run, you just have to do something like::

    cd into a python projects directory 
    git clone git@github.com:LarryEitel/flask_seed.git
    cd gsapi
    virtualenv venv

Create a local_settings to override for your environment

    cp settings.py local_settings.py

This is a windows hack to set some paths, etc. You may need to adjust for your Windows environment.

    activate.cmd

Non-Windows users:

    source venv/bin/activate
    cd flask_seed

    pip install -r requirements.txt

Run tests:

    nosetests
    Or:
        nosetests -v
        nosetests -v -s
        nosetests -v -s --nocapture

Run the application:

    python run.py

Developer Notes
===============

If you use WingWare IDE (Highly recommended), here are some useful settings for debugging:

Project/Project Settings

    Environment
        Python Path (Added):
            c:\Users\Larry\__prjs\flask_seed\venv\Lib\site-packages
            c:\Users\Larry\__prjs\flask_seed
    Debug
        Main Debug File:
            c:\Users\Larry\__prjs\flask_seed\flask_seed\run.py
        Initial Directory:
            c:\Users\Larry\__prjs\flask_seed\flask_seed
        Python Options (set testing ON, see flask_seed.run.main)
            -t
    Testing
        Default Test Framework
            Nose

