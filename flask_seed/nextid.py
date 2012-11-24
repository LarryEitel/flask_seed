class NextId():

    def __init__(self, db):
        self.db = db

    def nextId(self):
        db = self.db
        doc = {'id':1234}
        collection = db['ids']
        ret = collection.insert(doc, safe = True)       

        return 1234