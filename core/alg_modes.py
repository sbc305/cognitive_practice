import pandas as pd
import emd
import numpy as np


def EMD(column: pd.Series):
    imf = emd.sift.sift(column.to_numpy())
    return imf


def calculate_mean_square_sum(x: np.array):
    return sum([i * i for i in x]) / len(x)


def count_extremes(x):
    count = 0
    for i in range(1, len(x) - 1):
        if abs(x[i - 1]) <= abs(x[i]) and abs(x[i + 1]) < abs(x[i]):
            count += 1
    return count


def deviation_interpretaion(deviation: np.array, limit: float=40):
    if np.mean(abs(deviation)) > limit:
        return "значительные виляния"
    return "не выявлено значительных виляний" 