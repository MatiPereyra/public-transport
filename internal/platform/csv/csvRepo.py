import pandas as pd
from pandas.errors import EmptyDataError


class CSVRepo():
    def __init__(self, table, schema):
        self.filename = table
        self.schema = schema
        return

    def Append(self, new_rows: pd.DataFrame):
        if set(new_rows.columns) != set(self.schema):
            raise Exception("Schema mismatch: {} != {}".format(set(self.schema), set(new_rows.columns)))
        try:
            df = pd.read_csv(self.filename)
        except (FileNotFoundError, EmptyDataError):
            df = pd.DataFrame(columns=self.schema)
        df = pd.concat([df, new_rows], ignore_index=True)
        df.to_csv(self.filename, index=False)