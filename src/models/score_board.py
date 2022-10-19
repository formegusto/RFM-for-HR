from pymongo import MongoClient as mc


class ScoreBoardModel:
    def __init__(self):
        mongo_uri = "mongodb://localhost:27017"
        self.conn = mc(mongo_uri)['rfm-for-hr']
        self.col = self.conn['score-board']

    def save(self, start_time, end_time, score):
        self.col.insert_one({
            "start_time": start_time,
            "end_time": end_time,
            "score": score
        })

    def find(self, minute):
        print("minute", minute)
        return self.col.find_one({
            "$and": [
                {
                    "start_time": {
                        "$lte": minute
                    }
                },
                {
                    "end_time": {
                        "$gte": minute
                    }
                }
            ]
        })
