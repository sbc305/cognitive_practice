from fastapi import FastAPI
import pandas as pd
from datetime import date
import algo
from pydantic import BaseModel

class TimeStampData(BaseModel): # модель для обработки запроса по предоставлению данных по таймстемпам
    start: str # начальный таймстемп
    finish: str # конечный таймстемп


app = FastAPI() 
data = pd.read_csv("data.csv")
numbers = [i for i in range(data.shape[0])]
data["time"] = pd.to_datetime(data["ts"], format='mixed')
data.index = data['ts']
data = data.fillna('')

@app.post("/data_timestamps/")
async def find_timestamp(pass_data: TimeStampData):
    times = pd.Series((pass_data.start, pass_data.finish))
    times = pd.DataFrame(times, columns=["time"])
    times['time'] = pd.to_datetime(times["time"], format='mixed')
    start = times.at[0, "time"]
    finish = times.at[1, "time"]
    condition = (data['time'] >= start) & (data['time'] <= finish)
    indices = data.index[condition].tolist()
    piece_of_data = list()
    for i in indices:
        piece_of_data.append(data.loc[i])
    return piece_of_data    
