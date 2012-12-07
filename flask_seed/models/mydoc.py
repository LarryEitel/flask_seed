from app import app
from mongoengine.base import ValidationError

def fieldsToHandle(m):
    m_data = m._data
    fields = {}
    for k, v in m_data.iteritems():
        if v and k:
            fields[k] = v

    fields['_cls'] = m._cls
    fields['_types'] = [m._cls]
    return fields

def validate(doc):
    # Get a list of tuples of field names and their current values
    fields = [(field, getattr(doc, name))
              for name, field in doc._fields.items()]

    # Ensure that each field is matched to a valid value
    errors = {}
    for field, value in fields:
        if value is not None:
            try:
                field._validate(value)
                # need to capture field-level errors!
                if hasattr(field, 'myError'):
                    errors[field.name] = field.myError
                    # del it not that we have captured the error
                    del field.myError
            except ValidationError, error:
                errors[field.name] = error.errors or error
            except (ValueError, AttributeError, AssertionError), error:
                errors[field.name] = error
        elif field.required:
            errors[field.name] = ValidationError('Field is required',
                                                 field_name=field.name)
    return errors

# inspired by http://stackoverflow.com/questions/6102103/using-mongoengine-document-class-methods-for-custom-validation-and-pre-save-hook
class MyDoc(app.db.Document):

    def fieldsToHandle(self):
        return fieldsToHandle(self)

    def validate(self):
        return validate(self)

class MyEmbedDoc(app.db.EmbeddedDocument):

    def fieldsToHandle(self):
        return fieldsToHandle(self)

    def validate(self):
        return validate(self)

