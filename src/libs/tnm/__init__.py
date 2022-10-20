import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from src.libs import Calender
from src.models import HumanModel


class TNMAnalyzer:
    def __init__(self, month):
        human_model = HumanModel()

        self.emp_names = [_['name'] for _ in human_model.find_all()]

        self.prev_month = month - 1
        self.month = month
        self.calenders = [Calender(self.month, emp_name)
                          for emp_name in self.emp_names]

    def get_tnm_model(self, weights=[1, 1, 1]):
        TNMModel = pd.DataFrame(
            columns=['employee_name', 'Time', 'Number', 'Magnitude', 'TNM Value'])

        for cal in self.calenders:
            emp_name = cal.emp_name
            day_group_datas = cal.get_day_group()
            if day_group_datas is None:
                TNMModel = TNMModel.append({
                    "employee_name": emp_name,
                    "Time": 0,
                    "Number": 0,
                    "Magnitude": 0,
                    "TNM Value": 0
                }, ignore_index=True)

                continue

            time = day_group_datas['day'].max()
            number = len(day_group_datas)
            magnitude = day_group_datas['score'].sum()

            time_weight, number_weight, magnitude_weight = weights

            TNM_value = (time * time_weight) + (number * number_weight) + \
                (magnitude * magnitude_weight)

            TNMModel = TNMModel.append({
                "employee_name": emp_name,
                "Time": time * time_weight,
                "Number": number * number_weight,
                "Magnitude": magnitude * magnitude_weight,
                "TNM Value": TNM_value
            }, ignore_index=True)

        return TNMModel

    def get_score_table(self, TNMModel=None):
        score_table = pd.DataFrame()
        target_col = ['Time', 'Number', 'Magnitude']

        if TNMModel is None:
            TNMModel = self.get_tnm_model()

        for col in target_col:
            col_datas = TNMModel[col].tolist()
            min_data = min(col_datas)
            max_data = max(col_datas)

            score_col = np.linspace(min_data, max_data, 4)
            # 소숫점 첫 째 자리까지만 살려두기
            score_col = np.round(score_col * 10) / 10
            score_table[col] = score_col

        # 작거나 같으면에 점수를 부여하면 되기 때문에 최댓값은 필요없다.
        score_table = score_table.iloc[:-1]
        score_table.index = ['1점(우수)', '2점(미달)', '3점(매우미달)']
        score_table['score'] = [1, 2, 3]

        return score_table

    def get_norm_tnm_model(self, TNMModel=None):
        norm_TNMModel = pd.DataFrame(
            columns=['employee_name', 'Time', 'Number', 'Magnitude', 'TNM Value'])
        if TNMModel is None:
            TNMModel = self.get_tnm_model()
        score_table = self.get_score_table(TNMModel)

        for idx, row in TNMModel.iterrows():
            emp_name = row[0]
            time = score_table['score'][score_table['Time'] <= row['Time']][-1]
            number = score_table['score'][score_table['Number']
                                          <= row['Number']][-1]
            magnitude = score_table['score'][score_table['Magnitude']
                                             <= row['Magnitude']][-1]

            norm_tnm_value = time + number + magnitude
            norm_TNMModel = norm_TNMModel.append({
                "employee_name": emp_name,
                "Time": time,
                "Number": number,
                "Magnitude": magnitude,
                "TNM Value": norm_tnm_value
            }, ignore_index=True)

        return norm_TNMModel

    def draw(self, norm_TNMModel=None):
        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot(projection='3d')

        if norm_TNMModel is None:
            norm_TNMModel = self.get_norm_tnm_model()
        for idx, row in norm_TNMModel.iterrows():
            emp_name, t, n, m = row[:-1]
            ax.scatter(t, n, m, s=400, label=emp_name)

        ax.invert_xaxis()
        ax.set_xlabel('Time')
        ax.set_xticks(range(0, 3))
        ax.set_ylabel('Number')
        ax.set_yticks(range(0, 3))
        ax.set_zlabel('Magnitude')
        ax.set_zticks(range(0, 3))

        plt.legend(fontsize=18)
        plt.show()

    def get_merge_tnm_model(self):
        prev_tnm = TNMAnalyzer(self.prev_month)
        prev_tnm = prev_tnm.get_tnm_model()
        prev_tnm.set_index("employee_name", inplace=True)

        now_tnm = self.get_tnm_model()
        now_tnm.set_index("employee_name", inplace=True)

        prev_tnm.index = ["{}_{}월".format(
            _, self.prev_month) for _ in prev_tnm.index]
        now_tnm.index = ["{}_{}월".format(_, self.month)
                         for _ in now_tnm.index]

        return pd.concat([prev_tnm, now_tnm])

    def get_merge_norm_tnm_model(self):
        TNMModel = self.get_merge_tnm_model()
        TNMModel.reset_index(inplace=True)

        return self.get_norm_tnm_model(TNMModel)

    def draw_merge(self):
        self.draw(self.get_merge_norm_tnm_model())

    def get_result(self):
        TNMModel = self.get_tnm_model()
        _TNMModel = self.get_merge_tnm_model()
        better_scores = list()

        for emp_name in self.emp_names:
            row_prev = _TNMModel.loc["{}_{}월".format(
                emp_name, self.prev_month)]
            row_now = _TNMModel.loc["{}_{}월".format(emp_name, self.month)]

            better_score = np.sqrt(((row_prev[:-1] - row_now[:-1]) ** 2).sum())
            # 첫 째 자리 까지만 살려두기
            better_score = round(better_score * 10) / 10

            better_scores.append(better_score)

        TNMModel['개선점수'] = better_scores
        return TNMModel
