from app import app
from mongoengine.fields import StringField, EmailField
from mongoengine.base import ValidationError


# this is all about having to recursively gather all errors in doc and return them
# we temporarily set a myError class attribute, append to doc_errors, then delete it
def myError(field, message="", errors=None, field_name=None):
    field_name = field_name if field_name else field.name
    field.myError = ValidationError(message, errors=errors, field_name=field_name)


class MyStringField(StringField):
    def error(self, message="", errors=None, field_name=None):
        myError(self, message, errors, field_name)

class MyEmailField(EmailField):
    def error(self, message="", errors=None, field_name=None):
        myError(self, message, errors, field_name)