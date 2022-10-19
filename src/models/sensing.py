# Model Human
from pymongo import MongoClient as mc
from datetime import datetime as dt
from src.models.human import HumanModel
from src.models.schedule import ScheduleModel
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

    def get_one_month(self, month):
        human_model = HumanModel()
        schedule_model = ScheduleModel()

        target_start_date = dt.strptime(
            "2022{}01T00:00".format(str(month).zfill(2)), "%Y%m%dT%H:%M")
        target_end_date = dt.strptime("2022{}01T00:00".format(
            str(month + 1).zfill(2)), "%Y%m%dT%H:%M")

        cursor = self.col.find({
            "$and": [
                {
                    "start_time": {
                        "$gte": target_start_date
                    }
                },
                {
                    "start_time": {
                        "$lte": target_end_date
                    }
                },
            ]
        })

        datas = list()
        for c in cursor:
            user_id = c['user_id']
            human = human_model.find_by_id(user_id)

            schedule_id = c['schedule_id']
            schedule = schedule_model.find_by_id(schedule_id)

            datas.append({
                "employee_name": human['name'],
                "event": "지각" if schedule['title'] == '출근 확인' else "자리 이탈",
                "start_time": c['start_time'],
                "end_time": c['end_time'],
                "score": c['score']
            })

        return datas
