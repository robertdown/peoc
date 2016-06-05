import hashlib
from pymongo import MongoClient
from pymongo.errors import BulkWriteError
from pymongo.errors import InvalidOperation

class BasePEOC():

    def __init__(self):
        self.conn = MongoClient()
        self.db = self.conn.peoc
        self.coll = self.db.active

    def put(self, data):
        current = self.coll.find().sort('dispatch_time', -1).limit(30)
        bulk = self.coll.initialize_unordered_bulk_op()
        keys = self.parseActiveKeys(self.get())
        for call in data:
            if call['callno'] not in keys:
                bulk.insert(call)
        try:
            bulk.execute()
        except BulkWriteError as e:
            print(e)
            pass
        except InvalidOperation as e:
            print('No new calls  %s' % e)
            pass


    def generateCallNo(self, dispatch_time, address, units):
        unit_str = ""
        for unit in units:
            unit_str = unit + str(unit)
        callno = str(dispatch_time) + address + unit_str
        m = hashlib.sha1()
        m.update(callno.encode('UTF-8'))
        return m.hexdigest()


    def get(self):
        try:
            active = self.coll.find().sort('dispatch_time', -1).limit(30)
            return active
        except Exception as e:
            print(e)


    def parseActiveKeys(self, incidents):
        keys = []
        try:
            for i in incidents:
                keys.append(i['callno'])
            return keys
        except Exception as e:
            print(e)
