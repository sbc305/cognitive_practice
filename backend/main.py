from fastapi import FastAPI
import pandas as pd
from datetime import date
import algo
from pydantic import BaseModel

class Data(BaseModel):
    start: date
    finish: date
    result: str



data = pd.read_csv("data.csv")
data["time"] = pd.to_datetime(data["ts"], format='mixed')
data.index = data['ts']
app = FastAPI()

data = data.fillna('')
@app.get("/data/{timestamps}")
def find_timestamp(timestamps: str):
    times = pd.Series(timestamps.split(','))
    times = pd.DataFrame(times, columns=["time"])
    times['time'] = pd.to_datetime(times["time"], format='mixed')
    start = times.at[0, "time"]
    finish = times.at[1, "time"]
    piece_of_data = data[(finish >= data["time"]) & (data['time'] >= start)]
    return piece_of_data.to_csv()

@app.post("/")
def getData(data: Data):
    data.result = algo.work()
    return data
