from flask_seed.models import Person

def getPerson():
    name = "Larry"
    person = Person.objects.get(name=name)
    return person