from pymongo import MongoClient
from pymongo.errors import BulkWriteError

class BasePEOC():

    def __init__(self):
        self.conn = MongoClient()
        self.db = self.conn.peoc
        self.coll = self.db.active

    def put(self, data):
        try:
            insert = self.coll.insert_many(data).inserted_ids
        except BulkWriteError as e:
            print(e)
            pass


    def get(self):
        try:
            active = self.coll.find().sort({dispatch_time: -1})
            return active
        except Exception as e:
            print(e)

