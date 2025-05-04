from datetime import datetime, UTC

import pandas as pd

from internal.platform.csv.csvRepo import CSVRepo


class JourneysRepository:
    def __init__(self, filename: str = None):
        self.filename = "../data/journeys.csv"
        if filename is not None:
            self.filename = filename
        self.schema = [
            "job_run_at",
            "station_id_from",
            "station_id_to",
            "duration_in_seconds"
        ]
        self.repo = CSVRepo(self.filename, self.schema)

    def Update(self, new_rows, subset: list[str]):
        """
        TODO: assuming journeys return the same duration whenever it is queried
        :param subset:
        :param new_rows:
        :return:
        """
        new_rows["job_run_at"] = datetime.now(UTC).isoformat()
        new_rows["job_run_at"] = pd.to_datetime(new_rows["job_run_at"])
        self.repo.Update(new_rows, subset)
