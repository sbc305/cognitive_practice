from . import alg_modes
import pandas as pd


def get_etalon_emd():
    data = pd.read_csv("data/data.csv")
    data["time"] = pd.to_datetime(data["ts"], format='mixed').dt.time
    timestamps = pd.Series(["2024-08-21 09:26:38", "2024-08-21 09:27:48"])

    timestamps = pd.DataFrame(timestamps, columns=["timestamps"])
    timestamps['time'] = pd.to_datetime(timestamps["timestamps"], format='mixed').dt.time

    start = timestamps.at[0, "time"]
    end = timestamps.at[1, "time"]
    piece_of_data = data[(end >= data["time"]) & (data['time'] >= start)]

    return alg_modes.EMD(piece_of_data['cte'])
