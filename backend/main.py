from fastapi import FastAPI
import pandas as pd
from datetime import date
import algo
from pydantic import BaseModel

class TimeStampData(BaseModel): # модель для обработки запроса по предоставлению данных по таймстемпам
    start: str # начальный таймстемп
    finish: str # конечный таймстемп

class IDData(BaseModel): # модель для предоставления данных по id
    id: int # непосредственно ID файла, который нужно предоставить

app = FastAPI() 
data = pd.read_csv("data.csv")
data = data.fillna('')
data = data.to_dict(orient = "records")

def find(start, finish):
    return_data = list()
    for line in data:
        if ((line['ts'] >= start) and (line['ts'] <= finish)):
            return_data.append(line)    
    return return_data    

@app.post("/data_by_timestamps/")
async def find_by_timestamp(pass_data: TimeStampData):
    return find(pass_data.start, pass_data.finish)

@app.post("/data_by_id/")
async def find_by_id(pass_data: IDData):
    id = pass_data.id
    if (id < 0 or id > 11):
        return "No such time period"
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
    return find(id_to_ts[id][0], id_to_ts[id][1])