from pydantic import BaseModel, model_validator, Field
from typing import Dict, Any, Optional
from datetime import datetime

class IDData(BaseModel): # модель для предоставления данных по id
    id: int # непосредственно ID файла, который нужно предоставить


class DataSourceModel(BaseModel): # модель для способа поиска данных: по таймстемпам или по ID
    file_id: Optional[int] = Field(default = None, validate_default = True) # ID файла
    start_time: Optional[str] = Field(default = None, validate_default = True) # начальный таймстемп
    finish_time: Optional[str] = Field(default = None, validate_default = True) # конечный таймстемп

    @model_validator(mode = 'before')
    def check_correct_input(data):
        if (('file_id' in data) and (('start_time' in data) or ('finish_time' in data))):
            raise ValueError('Задать можно либо ID, либо два таймстемпа')    
        if ('file_id' not in data) and ('start_time' not in data) and ('finish_time' not in data):
            raise ValueError('Нужно задать хотя бы что-то')
        return data

class AlgoSetup(BaseModel): # модель для запуска алгоритма
    source_info: DataSourceModel # передаются таймстемпы или файл
    device_id: str # ID ТС
    algo_id: int # ID алгоритма, которым хотим считать
    params: Dict[str, Any] # параметры алгоритма


class AlgoAnswer(BaseModel):
    answer: str # ответ алгоритма
    artefacts: Dict[str, Any] # артефакты работы алгоритма

class Record(BaseModel):
    algo_info: AlgoSetup # информация об алгоритме, которым производился обсчёт
    arrival_time: str # время прихода задачи на обработку
    proc_time: str # длительность работы алгоритма 
    answer_time: str # время получения ответа
    result: AlgoAnswer # результат работы алгоритма

