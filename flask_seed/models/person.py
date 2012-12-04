import datetime

from app import app

class Person(app.db.Document):
    name = app.db.StringField(required=True, unique=True)
    """A unique string that identifies the person"""

    updated_at = app.db.DateTimeField(required=True)

    def save(self, *args, **kwargs):
        self.updated_at = datetime.datetime.now()
        super(Person, self).save(*args, **kwargs)