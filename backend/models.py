from pydantic import BaseModel, model_validator, Field
from typing import Dict, Any, Optional, List
from datetime import datetime

class BaseConfigModel(BaseModel):
    class Config:
        strict = True # проверка типов для всех моделей
        arbitrary_types_allowed = False  # запрет на произвольные типы

class IDData(BaseConfigModel): # модель для предоставления данных по id
    id: int # непосредственно ID файла, который нужно предоставить


class DataSourceModel(BaseConfigModel): # модель для способа поиска данных: по таймстемпам или по ID
    file_id: Optional[int] = Field(default = None, validate_default = True) # ID файла
    start_time: Optional[str] = Field(default = None, validate_default = True) # начальный таймстемп
    finish_time: Optional[str] = Field(default = None, validate_default = True) # конечный таймстемп

    @model_validator(mode = 'before')
    def check_correct_input(data):
        if (('file_id' in data) and (('start_time' in data) or ('finish_time' in data))):
            raise ValueError('ID and sequence of timestamps must be used separately')
        if (('start_time' in data) or ('finish_time' in data)) and (data['start_time'] > data['finish_time']):
            raise ValueError('Wrong order of start time and finish time')
        if ('file_id' not in data) and ('start_time' not in data) and ('finish_time' not in data):
            raise ValueError('Empty source info')
        if ('file_id' in data) and (not isinstance(data['file_id'], int)):
            raise ValueError('Wrong ID type')
        if ('file_id' in data) and ((data['file_id'] < 0) or (data['file_id'] > 11)):
            raise ValueError('File ID out of bounds')
        return data

class AlgoSetup(BaseConfigModel): # модель для запуска алгоритма
    source_info: DataSourceModel # передаются таймстемпы или файл
    device_id: str # ID ТС
    algo_id: int # ID алгоритма, которым хотим считать
    valued_by: List[str] # параметры, по которым идёт оценка
    limit: float # лимит в алгоритме


class AlgoAnswer(BaseConfigModel):
    answer: str # ответ алгоритма
    artefacts: Dict[str, Any] # артефакты работы алгоритма

class Record(BaseConfigModel):
    algo_info: AlgoSetup # информация об алгоритме, которым производился обсчёт
    arrival_time: str # время прихода задачи на обработку
    proc_time: str # длительность работы алгоритма 
    answer_time: str # время получения ответа
    result: AlgoAnswer # результат работы алгоритма
