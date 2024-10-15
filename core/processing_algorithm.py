import pandas as pd
import alg_modes


def calculate(df: pd.DataFrame):
    empirical_modes = alg_modes.EMD(df.cte)
    deviation = alg_modes.compare_modes(empirical_modes)
    result = alg_modes.deviation_interpretaion(deviation)
    return result
