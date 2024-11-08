from . import alg_modes
import pandas as pd


def get_etalon_emd(columns):
    data = pd.read_csv("data/data.csv")
    data["time"] = pd.to_datetime(data["ts"], format='mixed').dt.time
    timestamps = pd.Series(["2024-08-21 09:26:38", "2024-08-21 09:27:48"])

    timestamps = pd.DataFrame(timestamps, columns=["timestamps"])
    timestamps['time'] = pd.to_datetime(timestamps["timestamps"], format='mixed').dt.time

    start = timestamps.at[0, "time"]
    end = timestamps.at[1, "time"]
    piece_of_data = data[(end >= data["time"]) & (data['time'] >= start)]

    for column in columns:
        EMDs = pd.DataFrame()
        modes = alg_modes.EMD(piece_of_data[column])
        for i in range(modes.shape[1]):
            EMDs[str(i)] = modes[:, i]
        
        EMDs.to_csv("data/etalon_" + column + "_EMD.csv")

def get_etalon_extreme_count(columns):
    data = pd.read_csv("data/data.csv")
    data["time"] = pd.to_datetime(data["ts"], format='mixed').dt.time
    timestamps = pd.Series(["2024-08-21 09:26:48", "2024-08-21 09:27:48"])

    timestamps = pd.DataFrame(timestamps, columns=["timestamps"])
    timestamps['time'] = pd.to_datetime(timestamps["timestamps"], format='mixed').dt.time

    start = timestamps.at[0, "time"]
    end = timestamps.at[1, "time"]
    piece_of_data = data[(end >= data["time"]) & (data['time'] >= start)]

    extremes = pd.DataFrame()
    for column in columns:
        extremes_column = alg_modes.count_extremes(piece_of_data[column].values)
        extremes[column] = pd.Series(extremes_column)
        
    extremes.to_csv("data/etalon_extremes.csv")
    
    
if __name__ == "__main__":
    get_etalon_emd(['cte', 'yaw_rate', 'speed'])
    get_etalon_extreme_count(['cte', 'yaw_rate', 'speed'])
