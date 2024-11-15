import pandas as pd
import numpy as np
from . import alg_modes
from . import etalon_data


class ProcessingAlgorithm():
    def __init__(self, data: pd.DataFrame, columns=['cte', 'yaw_rate', 'steer_fb']):
        self.data = data
        self.columns = columns
        self.set_etalon_data()
        self.limits = dict()
    
    
    def set_etalon_data(self) -> None:
        etalon_data.get_etalon_emd(self.columns)
        etalon_data.get_etalon_extreme_count(self.columns)
        
        
    def compare_mode_with_etalon(self, column: str) -> np.array:
        etalon = alg_modes.calculate_mean_square_sum(self.get_EMD(column, True))
        empirical_modes = self.get_EMD(column)
        current = alg_modes.calculate_mean_square_sum(empirical_modes)
        if current.shape[0] > etalon.shape[0]:
            np.append(etalon, np.zeros(etalon.shape[0],))
        mode_count = min(etalon.shape[0], current.shape[0])
        self.limits[column] = np.mean(abs(etalon))
        return (current[:mode_count] - etalon[:mode_count]) / etalon[:mode_count]
    
    
    def calculate(self, column: str, limit: float=40) -> str:
        deviation = self.compare_mode_with_etalon(column)
        result = alg_modes.deviation_interpretaion(deviation, limit)
        return result
    
    def get_EMD(self, column: str, etalon=False):
        if etalon:
            return pd.read_csv("data/etalon_" + column + "_EMD.csv").values
        return alg_modes.EMD(self.data[column])
    
    def get_extremes_count(self, column: str, etalon=False) -> int:
        if etalon:
            return pd.read_csv("data/etalon_extremes.csv").loc[0, column]
        return alg_modes.count_extremes(self.data[column])