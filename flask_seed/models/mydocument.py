from app import app
from mongoengine.base import ValidationError

def validate(doc):
    errors = {}

    # Get a list of tuples of field names and their current values
    fields = [(field, getattr(doc, name))
              for name, field in doc._fields.items()]

    # Ensure that each field is matched to a valid value
    errors = {}
    for field, value in fields:
        if value is not None:
            try:
                field._validate(value)
            except ValidationError, error:
                errors[field.name] = error.errors or error
            except (ValueError, AttributeError, AssertionError), error:
                errors[field.name] = error
        elif field.required:
            errors[field.name] = ValidationError('Field is required',
                                                 field_name=field.name)
    return errors

# inspired by http://stackoverflow.com/questions/6102103/using-mongoengine-document-class-methods-for-custom-validation-and-pre-save-hook
class MyDocument(app.db.Document):
    def validate(self):
        return validate(self)

class MyEmbeddedDocument(app.db.EmbeddedDocument):
    def validate(self):
        return validate(self)

