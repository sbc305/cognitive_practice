import pandas as pd
import emd
import numpy as np

import etalon_data


def EMD(cte: pd.Series):
    imf = emd.sift.sift(cte.to_numpy())
    return imf


def calculate_mean_square_sum(x: np.array):
    return sum([i * i for i in x]) / len(x)


def compare_modes(empirical_modes: pd.Series):
    etalon = calculate_mean_square_sum(etalon_data.get_etalon_emd())
    current = calculate_mean_square_sum(empirical_modes)
    mode_count = min(etalon.shape[0], current.shape[0])
    return (current[:mode_count] - etalon[:mode_count]) / etalon[:mode_count]

def deviation_interpretaion(deviation: np.array):
    if max(abs(deviation)) > 40:
        return "значительные виляния"
    return "не выявлено значительных виляний"