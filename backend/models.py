from pydantic import BaseModel

class TimeStampData(BaseModel): # модель для обработки запроса по предоставлению данных по таймстемпам
    start: str # начальный таймстемп
    finish: str # конечный таймстемп

class IDData(BaseModel): # модель для предоставления данных по id
    id: int # непосредственно ID файла, который нужно предоставить

# подключу этот функционал позже

# class AlgoSetup(BaseModel): # модель для запуска алгоритма
#     id: int # ID файла для обсчёта
#     algo_id: int # ID алгоритма, которым хотим считать
#     params: str # частный случай для нашего алгоритма: по каким параметрам хотим производить оценку

# class AlgoResult(BaseModel): # модель для предоставления результатов работы алгоритма
#     cte: str # результат для cte
#     yaw_rate: str # результат для yaw_rate
#     speed: str # результат для speed