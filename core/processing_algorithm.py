import pandas as pd
import numpy as np
from . import alg_modes
from . import etalon_data


class ProcessingAlgorithm():
    def __init__(self, data: pd.DataFrame, columns=['cte', 'yaw_rate', 'speed']):
        self.data = data
        self.columns = columns
        self.set_etalon_data()
    
    
    def set_etalon_data(self) -> None:
        etalon_data.get_etalon_emd(self.columns)
        etalon_data.get_etalon_extreme_count(self.columns)
        
        
    def compare_modes(self, empirical_modes: pd.Series, column: str) -> np.array:
        data = pd.read_csv("data/etalon" + column + "EMD.csv")
        etalon = alg_modes.calculate_mean_square_sum(data)
        current = alg_modes.calculate_mean_square_sum(empirical_modes)
        mode_count = min(etalon.shape[0], current.shape[0])
        return (current[:mode_count] - etalon[:mode_count]) / etalon[:mode_count]
    
    
    def calculate(self, column: str) -> str:
        empirical_modes = alg_modes.EMD(self.data[column])
        deviation = self.compare_modes(empirical_modes, column)
        result = alg_modes.deviation_interpretaion(deviation)
        return result