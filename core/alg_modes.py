import pandas as pd
import emd
import numpy as np


def EMD(column: pd.Series):
    imf = emd.sift.sift(column.to_numpy())
    return imf


def calculate_mean_square_sum(x: np.array) -> np.array:
    result = []
    for i in range(x.shape[1]):
        result.append((x[:, i] ** 2).mean())
    return np.array(result)



def count_extremes(x: np.ndarray) -> int:
    count = len(emd.sift.get_padded_extrema(x)[0])
    return count


def deviation_interpretaion(deviation: np.array, limit: float):
    if np.mean(abs(deviation)) > limit:
        return True
    return False