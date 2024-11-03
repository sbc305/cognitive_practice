from fastapi import FastAPI
import pandas as pd
from pydantic import BaseModel
from core.processing_algorithm import calculate
from fastapi.middleware.cors import CORSMiddleware
class TimeStampData(BaseModel): # модель для обработки запроса по предоставлению данных по таймстемпам
    start: str # начальный таймстемп
    finish: str # конечный таймстемп

class IDData(BaseModel): # модель для предоставления данных по id
    id: int # непосредственно ID файла, который нужно предоставить

app = FastAPI() 
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
data = pd.read_csv("data/data.csv")
data = data.fillna('')

id_to_ts = {0: ["2024-08-21 09:26:38", "2024-08-21 09:27:48"], \
            1: ["2024-08-21 09:41:00", '2024-08-21 09:42:10'], \
            2: ['2024-08-21 09:55:25', '2024-08-21 09:56:55'], \
            3: ['2024-08-21 10:06:17', '2024-08-21 10:07:47'], \
            4: ['2024-08-21 10:25:00', '2024-08-21 10:26:20'], \
            5: ['2024-08-21 10:35:25', '2024-08-21 10:36:45'], \
            6: ['2024-08-21 10:40:13', '2024-08-21 10:41:33'], \
            7: ['2024-08-21 10:45:52', '2024-08-21 10:47:22'], \
            8: ['2024-08-21 10:49:37', '2024-08-21 10:51:07'], \
            9: ["2024-08-21 12:17:03", "2024-08-21 12:27:53"], \
            10: ['2024-08-21 12:44:41', '2024-08-21 12:49:51'], \
            11: ['2024-08-21 12:56:45', '2024-08-21 13:04:15'] }                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
    


def find_data(start, finish):
    return data[(data["ts"] >= start) & (data["ts"] <= finish)]    

@app.post("/data_by_timestamps/")
async def find_by_timestamp(pass_data: TimeStampData):
    return find_data(pass_data.start, pass_data.finish).to_dict(orient = "records")

@app.post("/data_by_id/")
async def find_by_id(pass_data: IDData):
    id = pass_data.id
    if (id < 0 or id > 11):
        return "No such time period"
    return find_data(id_to_ts[id][0], id_to_ts[id][1]).to_dict(orient = "records")

@app.post("/algo/")
async def algo(pass_data: IDData):
    id = pass_data.id
    start, finish = id_to_ts[id]
    return calculate(find_data(start, finish))
