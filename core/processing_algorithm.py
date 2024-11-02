import pandas as pd
from . import alg_modes


def calculate(df: pd.DataFrame):
    cte = alg_modes.calculate_value(df, 'cte')
    yaw_rate = alg_modes.calculate_value(df, 'yaw_rate')
    speed = alg_modes.calculate_value(df, 'speed')
    
    return 'cte: ' + cte + ' yaw_rate: ' +  yaw_rate + ' speed: ' + speed
