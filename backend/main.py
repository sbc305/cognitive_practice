from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
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

@app.post("/data/")
async def find(source_info: models.DataSourceModel):
    pass_data = source_info.model_dump(exclude_none = True)
    dm = ''
    if (pass_data["device_id"] == "tractordroid-23080159" or pass_data["device_id"] == "test"):
        dm = DataManager("data/data.csv")
    else:
        if not os.path.exists(f"data/input_samples/{pass_data['device_id']}.csv"):
            raise HTTPException(status_code=404, detail="File not found")
        dm = DataManager(f"data/input_samples/{pass_data['device_id']}.csv")
    if ('file_id' in pass_data):
        id = pass_data['file_id']
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
    proc_alg = {""}
    dm_example = DataManager("data/data.csv")
    if (info_data["device_id"] == "tractordroid-23080159" or info_data["device_id"] == "test"):
        if 'file_id' in info_data:
            proc_alg = ProcessingAlgorithm(data = dm_example.find_data_by_id(info_data["file_id"]), etalon_data = dm_example.data)
        else:
            proc_alg = ProcessingAlgorithm(data = dm_example.find_data(info_data['start_time'], info_data['finish_time']), etalon_data = dm_example.find_data_by_id(id = 1), columns = pass_data.valued_by)
    else:
        if not os.path.exists(f"data/input_samples/{info_data['device_id']}.csv"):
            raise HTTPException(status_code=404, detail="File not found")
        dm = DataManager(f"data/input_samples/{info_data['device_id']}.csv")
        proc_alg = proc_alg = ProcessingAlgorithm(data = dm.find_data(info_data['start_time'], info_data['finish_time']), etalon_data = dm_example.find_data_by_id(id = 1), columns = pass_data.valued_by)
    start_time = timeit.default_timer()
    etalon_modes_conv = {key: value.tolist() for key, value in proc_alg.etalon_modes.items()}
    current_modes_conv = {key: value.tolist() for key, value in proc_alg.current_modes.items()}
    wagging_modes_conv = proc_alg.modes_wagging
    wagging_conv = proc_alg.wagging
    for mode, _ in wagging_modes_conv.items():
        for i in range(len(wagging_modes_conv[mode])):
            wagging_modes_conv[mode][i] = wagging_modes_conv[mode][i].tolist()
    for mode, _ in wagging_conv.items():
        wagging_conv[mode] = wagging_conv[mode].to_dict(orient = 'records') 
    algo_answer = models.AlgoAnswer(answer = proc_alg.calculate(), columns = proc_alg.columns, etalon_modes = etalon_modes_conv, current_modes = current_modes_conv, extremes = proc_alg.extremes, etalon_extremes = proc_alg.etalon_extremes, modes = proc_alg.modes, modes_wagging = proc_alg.modes_wagging, wagging = wagging_conv)
    print(type(wagging_conv[mode]))
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
        raise HTTPException(status_code=404, detail="No logs for now!")

@app.post("/files_info")
async def return_info():
    folder_name = "data/input_samples"
    os.chdir(folder_name)
    files = os.listdir()
    names = [os.path.splitext(f)[0] for f in files if os.path.isfile(f)]
    return names


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={
            "detail": [
                {
                    "type": "validation_error",
                    "loc": exc.errors()[0]['loc'],
                    "msg": exc.errors()[0]['msg'],
                    "input": exc.errors()[0]['input']
                }
            ]
        }
    )
