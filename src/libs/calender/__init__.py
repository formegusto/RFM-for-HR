import pandas as pd
from src.models import SensingModel


class Calender:
    def __init__(self, month, emp_name=None):
        sensing_model = SensingModel()
        self.emp_name = emp_name
        self.datas = pd.DataFrame(sensing_model.get_one_month(month, emp_name))

    def get_day_group(self):
        datas = self.datas.copy()

        if len(datas) == 0:
            return None
        datas['day'] = datas['start_time'].dt.day

        day_group_datas = datas.groupby('day').sum()
        day_group_datas.reset_index(inplace=True)
        return day_group_datas
