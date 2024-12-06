import pandas as pd
import numpy as np
from scipy.signal import correlate
from . import alg_modes


class ProcessingAlgorithm():
    def __init__(self, data: pd.DataFrame, etalon_data: pd.DataFrame,
                 modes=[], columns=['cte', 'yaw_rate']):
        self.data = data
        self.etalon_data = etalon_data
        self.columns = columns
        self.etalon_modes = dict()
        self.current_modes = dict()
        self.modes = modes
        self.extremes = dict()
        self.etalon_extremes = dict()
        self.set_EMD()
        self.set_exteme_count()
        
        
    def compare_mode_with_etalon(self, column: str) -> np.array: 
        # averaging correlation maxima across all modes
        energy_etalon = np.sum(np.abs(self.etalon_modes[column]), axis=0)
        energy_current = np.sum(np.abs(self.current_modes[column]), axis=0)
        correlation = correlate(self.etalon_modes[column] / energy_etalon, 
                                self.current_modes[column] / energy_current)
        return np.mean(np.max(np.abs(correlation), axis=0))
    
    
    def calculate(self, limit: float=0.004) -> str:
        similarity = 0
        for column in self.columns:
            similarity += self.compare_mode_with_etalon(column)
        result = alg_modes.similarity_interpretaion(similarity / len(self.columns), limit)        
        if result:
            return 'Значительные виляния'
        return 'Не выявлено значительных виляний'
    
    def set_EMD(self) -> None:
        for column in self.columns:
            EMDs = alg_modes.EMD(self.data[column])
            etalon_EMDs = alg_modes.EMD(self.etalon_data[column])
            if len(self.modes) == 0:
                self.current_modes[column] = EMDs
                self.etalon_modes[column] = etalon_EMDs
            else:
                self.current_modes[column] = EMDs[:, self.modes]
                self.etalon_modes[column] = etalon_EMDs[:, self.modes]
                
                
    def set_exteme_count(self) -> None:
        for column in self.columns:
            self.extremes[column] = alg_modes.count_extremes(self.data[column].to_numpy())
            self.etalon_extremes[column] = alg_modes.count_extremes(self.etalon_data[column].to_numpy())
