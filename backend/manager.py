import pandas as pd 

class DataManager():
    def __init__(self, source: str):
        self.data = pd.read_csv("data/data.csv")
        self.data = self.data.fillna('')

    def find_data(self, start, finish):
        return self.data[(self.data["ts"] >= start) & (self.data["ts"] <= finish)]
    
    def find_data_by_id(self, id):
        ans = pd.read_csv(f"data/output{id}.csv")
        ans = ans.fillna('')
        return ans