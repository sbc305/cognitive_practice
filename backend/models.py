from pydantic import BaseModel
from typing import Dict, Any
from datetime import datetime

class TimeStampData(BaseModel): # модель для обработки запроса по предоставлению данных по таймстемпам
    start: str # начальный таймстемп
    finish: str # конечный таймстемп

class IDData(BaseModel): # модель для предоставления данных по id
    id: int # непосредственно ID файла, который нужно предоставить


class AlgoSetup(BaseModel): # модель для запуска алгоритма
    # ts: TimeStampData # таймстемпы для взятия среза из общего файла
    id: int # ID файла
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


# class AlgoResult(BaseModel): # модель для предоставления результатов работы алгоритма
#     cte: str # результат для cte
#     yaw_rate: str # результат для yaw_rate
#     speed: str # результат для speed