from app import app
from mongoengine.base import ValidationError

class MyDocument(app.db.Document):
    # inspired by http://stackoverflow.com/questions/6102103/using-mongoengine-document-class-methods-for-custom-validation-and-pre-save-hook
    def validate(self):
        errors = {}

        # Get a list of tuples of field names and their current values
        fields = [(field, getattr(self, name))
                  for name, field in self._fields.items()]

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


class MyEmbeddedDocument(app.db.EmbeddedDocument):
    def validate(self):
        errors = {}

        # Get a list of tuples of field names and their current values
        fields = [(field, getattr(self, name))
                  for name, field in self._fields.items()]

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

