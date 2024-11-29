import pandas as pd
import emd
import numpy as np


def EMD(column: pd.Series):
    imf = emd.sift.sift(column.to_numpy())
    return imf


def count_extremes(x: np.ndarray) -> int:
    count = len(emd.sift.get_padded_extrema(x)[0])
    return count


def similarity_interpretaion(similarity: float, limit: float):
    # TODO: write more difficult interpretation
    if similarity > limit:
        return True
    return False