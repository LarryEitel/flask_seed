
class Config(object):
	DEBUG               = False

	DEFAULT_MAIL_SENDER = ("mail manager", "mail@manager.com")
	SECRET_KEY          = 'asdfasdfasdfasdfasdfasdfadsfasdf'

	TESTING_HOST        = 'localhost:5000'

	MONGO_HOST          = 'localhost'
	MONGO_DBNAME        = 'flask_seed'
	MONGO_TEST_DBNAME   = 'flask_seed-test'

	MONGO_TEST_DBNAME   = 'ex-test'

	ES_HOST             = 'localhost'
	ES_PORT             = 9200
	ES_NAME       		= 'index'
	ES_TEST_HOST        = 'localhost'
	ES_TEST_PORT        = 9200
	ES_TEST_NAME  		= 'index-test'

	ES 					= {
        'host': 'localhost',
        'port': 9200,
        'name': 'index'
        }

	#WTForms Settings
	CSRF_ENABLED        = True
	CSRF_SESSION_KEY    = '_csrf_token'

	#Flask Mail settings
	MAIL_SERVER         = 'localhost'
	MAIL_PORT           =  25
	MAIL_USE_TLS        = False
	MAIL_USE_SSL        = False
	MAIL_DEBUG          = DEBUG
	MAIL_USERNAME       = None
	MAIL_PASSWORD       = None
	DEFAULT_MAIL_SENDER = None


# try to COMPLETELY override the above Config with a local one
# TODO: Override vs Replace entire Object
try:
    from local_settings import Config as LocalConfig
    class Config(LocalConfig): pass

except ImportError:
    pass
