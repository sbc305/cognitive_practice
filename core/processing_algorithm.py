import pandas as pd
import numpy as np
import emd
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
        self.wagging = dict()
        self.modes_wagging = dict()
        self.set_EMD()
        self.set_extemes()
        self.find_wagging()
        
        
    def compare_mode_with_etalon(self, column: str) -> np.array: 
        # averaging correlation maxima across all modes
        energy_etalon = np.sum(self.etalon_modes[column] ** 2, axis=1)
        energy_current = np.sum(self.current_modes[column] ** 2, axis=1)
        correlation = correlate(self.etalon_modes[column].T / energy_etalon, 
                                self.current_modes[column].T / energy_current)
        return np.mean(np.max(np.abs(correlation), axis=0))
    
    
    def calculate(self, limit: float=21) -> str:
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
                self.current_modes[column] = EMDs.T
                self.etalon_modes[column] = etalon_EMDs.T
            else:
                self.current_modes[column] = (EMDs[:, self.modes]).T
                self.etalon_modes[column] = (etalon_EMDs[:, self.modes]).T
                
                
    def set_extemes(self) -> None:
        for column in self.columns:
            self.extremes[column] = alg_modes.count_extremes(self.data[column].to_numpy())
            self.etalon_extremes[column] = alg_modes.count_extremes(self.etalon_data[column].to_numpy())
            
            
    def find_wagging(self) -> None:
        for column in self.columns:
            extremes = []
            for mode in self.current_modes[column]:
                temp = np.array(emd.sift.get_padded_extrema(mode))
                if len(temp.shape) != 2:
                    break
                extremes.append(temp.T[np.argmax(temp[1, :], axis=0)])
            extremes = np.array(extremes)
            for i in range(extremes.shape[0]):
                if extremes[i][0] < 0 and len(self.current_modes[column]) > 0:
                    extremes[i][0] += self.current_modes[column][0].shape[0]
            index = int(extremes[np.argmax(extremes.T[1, :], axis=0)][0])
            self.wagging[column] = self.data.iloc[max(index-10, 0):min(index+10, self.data.shape[0])]
            self.modes_wagging[column] = [self.current_modes
                                          [column]
                                          [i]
                                          [max(int(index)-10, 0):min(int(index)+10, self.current_modes[column][i].shape[0])]
                                          for i, index in 
                                          zip(range(self.current_modes[column].shape[0]), extremes[:, 0])]

                