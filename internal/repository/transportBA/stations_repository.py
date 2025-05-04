from datetime import datetime, UTC

import pandas as pd

from internal.platform.csv.csvRepo import CSVRepo


class StationsRepository:
    def __init__(self, filename: str = None):
        self.filename = "../data/stations.csv"
        if filename is not None:
            self.filename = filename
        self.schema = [
            "job_run_at",
            "station_id",
            "groups",
            "num_bikes_available",
            "num_bikes_disabled",
            "num_docks_available",
            "num_docks_disabled",
            "status_last_reported_utc",
            "lat",
            "lon"
        ]
        self.repo = CSVRepo(self.filename, self.schema)

    def AppendWithJobRunAt(self, new_rows):
        new_rows["job_run_at"] = datetime.now(UTC).isoformat()
        new_rows["job_run_at"] = pd.to_datetime(new_rows["job_run_at"])
        self.repo.Append(new_rows)

    def GroupByStationIDWithCoordinates(self):
        df = self.repo.Read()
        return df[["station_id", "lat", "lon"]].groupby("station_id").max().reset_index()
