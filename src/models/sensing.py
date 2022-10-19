# Model Human
from pymongo import MongoClient as mc
from datetime import datetime as dt
from src.models.score_board import ScoreBoardModel


class SensingModel:
    def __init__(self):
        mongo_uri = "mongodb://localhost:27017"
        self.conn = mc(mongo_uri)['rfm-for-hr']
        self.col = self.conn.sensing

    # 시간은 YYYYMMDDTHH:MM 형식의 스트링으로 입력된다.
    def save(self, user_id, schedule_id, start_time, end_time):
        # score를 구해야 한다.
        start_time = dt.strptime(start_time, "%Y%m%dT%H:%M")
        end_time = dt.strptime(end_time, "%Y%m%dT%H:%M")
        minute = end_time - start_time
        minute = int(minute.seconds / 60)

        score_board = ScoreBoardModel()
        score = score_board.find(minute)['score']

        self.col.insert_one({
            "user_id": user_id,
            "schedule_id": schedule_id,
            "start_time": start_time,
            "end_time": end_time,
            "score": score
        })
