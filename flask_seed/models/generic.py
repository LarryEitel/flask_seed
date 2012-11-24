from schematics.models import Model as _Model
from schematics.types import StringType, DateTimeType, EmailType, FloatType

from schematics.types.mongo import ObjectIdType

class AppId(_Model):
	appName  = StringType()
	appKey   = StringType()
	appId    = StringType()
	appUrl   = StringType()
	siteUrl  = StringType()
	callBack = StringType()

	meta   = {
        'collection': 'apps',
        '_c': 'AppId',
        }
# class Share(_Model):
#     _c    = StringType(required=True, description='Class')
#     _public_fields = ['_c']

#     # The reason for this parent field given the fact that Wid'gets can contain an array of other widgets is that OTHER Widgets may LINK to this widget AND add their Share properties. It is necessary
#     parent   = ObjectIdType(minimized_field_name='Parent Widget ID', description='Primary Parent owner of this widget.')

#     usr_id   = ObjectIdType(minimized_field_name='Usr ID', description='Usr id for this Share.')

#     permission   = StringType(minimized_field_name='Permission', choices=['aa','ab','b'], description='aa=At and Above, ab=At and below, b=Below.')
