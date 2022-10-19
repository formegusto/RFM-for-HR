from pymongo import MongoClient as mc


class ScheduleModel:
    def __init__(self):
        mongo_uri = "mongodb://localhost:27017"
        self.conn = mc(mongo_uri)['rfm-for-hr']
        self.col = self.conn.schedule

    # status type, 1. static 2. real-time 3. stop-observe
    def save(self, title, start_time, end_time, status_type):
        self.col.insert_one({
            "title": title,
            "start_time": start_time,
            "end_time": end_time,
            "status_type": status_type
        })

    def find(self, title):
        return self.col.find_one({
            "title": title
        })

    def find_by_id(self, _id):
        return self.col.find_one({
            "_id": _id
        })
