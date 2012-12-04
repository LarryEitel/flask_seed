import sys
from flask_seed.app import app
from flask_seed.apps import web

def run():
    app.host = sys.argv['-h'] if '-h' in sys.argv else '127.0.0.1'
    if '-t' in sys.argv:
        app.config['TESTING'] = True
        print 'Running in test mode.'
    app.debug = '-d' in sys.argv
    app.use_reloader = '-r' in sys.argv
    app.run()

if __name__ == "__main__":
    run()
