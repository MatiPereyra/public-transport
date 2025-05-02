import pandas as pd


class Stations(pd.DataFrame):
    def __init__(self, data):
        if isinstance(data, pd.DataFrame):
            df = data
        else:
            df = pd.DataFrame.from_dict(data)
        super().__init__(df)
