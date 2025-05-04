import pandas as pd


class Stations(pd.DataFrame):
    def __init__(self, data):
        if isinstance(data, pd.DataFrame):
            df = data
        else:
            df = pd.DataFrame.from_dict(data)
        super().__init__(df)

    def GetLocationsByGroup(self):
        """

        :return: pd.DataFrame with columns ["groups", "lat", "lon"]
        """
        df = (self[["groups", "lat", "lon", "job_run_at"]].
              sort_values(on="job_run_at", ascending=False).
              drop_duplicates(keep="first"))
        df.groupby("groups")
        return df[["groups", "lat", "lon"]]
