# Model Human
from pymongo import MongoClient as mc


class HumanModel:
    def __init__(self):
        mongo_uri = "mongodb://localhost:27017"
        self.conn = mc(mongo_uri)['rfm-for-hr']
        self.col = self.conn.human

    def save(self, name):
        self.col.insert_one({
            "name": name
        })

    def find_all(self):
        return self.col.find({})

    def find(self, name):
        return self.col.find_one({
            "name": name
        })

    def find_by_id(self, _id):
        return self.col.find_one({
            "_id": _id
        })
