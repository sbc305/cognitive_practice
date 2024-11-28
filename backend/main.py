from fastapi import FastAPI
import pandas as pd
from pydantic import BaseModel
from core.processing_algorithm import ProcessingAlgorithm
from fastapi.middleware.cors import CORSMiddleware
import timeit
from datetime import datetime
import os
import json
from .manager import DataManager
from . import models

app = FastAPI() 
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
dm = DataManager("data/data.csv")

@app.post("/data/")
async def find(source_info: models.DataSourceModel):
    pass_data = source_info.model_dump(exclude_none = True)
    if ('file_id' in pass_data):
        id = pass_data['file_id']
        if (id < 0 or id > 11):
            return "No such time period"
        return dm.find_data_by_id(id).to_dict(orient = "records")
    else:
        start_ts = pass_data['start_time']
        finish_ts = pass_data['finish_time']
        return dm.find_data(start_ts, finish_ts).to_dict(orient = "records")


@app.post("/algo/", response_model = models.AlgoAnswer)
async def algo(pass_data: models.AlgoSetup) -> models.AlgoAnswer:
    request_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    start = "not provided"
    finish = "not provided"
    info_data = pass_data.source_info.model_dump(exclude_none = True)
    result = ""
    if 'file_id' in info_data:
        result = ProcessingAlgorithm(dm.find_data_by_id(info_data["file_id"]), pass_data.valued_by).calculate()
    else:
        result = ProcessingAlgorithm(dm.find_data(info_data['start_time'], info_data['finish_time']), pass_data.valued_by).calculate()
    start_time = timeit.default_timer()
    algo_answer = models.AlgoAnswer(answer = result, artefacts = {})
    finish_time = timeit.default_timer()
    result_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    count_time = f"{(finish_time - start_time) * 1000:.2} ms"
    record = models.Record(algo_info = pass_data, arrival_time = request_time, proc_time = count_time, answer_time = result_time, result = algo_answer)
    data = []
    if os.path.exists('data/log.json'):
        with open('data/log.json', 'r') as f:
            file_content = f.read()
            data = json.loads(file_content)
    string = json.loads(record.model_dump_json())
    data.append(string)
    with open('data/log.json', 'w', encoding = 'utf-8') as f:
        json.dump(data, f, ensure_ascii=False)
    return algo_answer

@app.post("/logs")
async def logs():
    if os.path.exists('data/log.json'):
        with open('data/log.json', 'r') as f:
            file_content = f.read()
            data = json.loads(file_content)
            return data   
    else:
        return "No logs for now!"

