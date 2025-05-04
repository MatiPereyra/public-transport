import pandas as pd
from pandas.errors import EmptyDataError


class CSVRepo:
    def __init__(self, table, schema):
        self.filename = table
        self.schema = schema
        return

    def Append(self, new_rows: pd.DataFrame):
        new_rows = new_rows[self.schema]
        try:
            df = pd.read_csv(self.filename)
        except (FileNotFoundError, EmptyDataError):
            df = pd.DataFrame(columns=self.schema)
        df = pd.concat([df, new_rows], ignore_index=True)
        df.to_csv(self.filename, index=False)

    def Update(self, new_rows: pd.DataFrame, subset: list[str]):
        new_rows = new_rows[self.schema]
        try:
            df = pd.read_csv(self.filename)
        except (FileNotFoundError, EmptyDataError):
            df = pd.DataFrame(columns=self.schema)

        df = pd.concat([df, new_rows], ignore_index=True)
        if subset is not None and len(subset) > 0:
            df = new_rows.drop_duplicates(subset=subset, keep="last")
        df.to_csv(self.filename, index=False)

    def Read(self):
        return pd.read_csv(self.filename)
