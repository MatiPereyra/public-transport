import pandas as pd

from internal.domain.locations import Location
from internal.gateway.openrouteservice.client import OpenRouteServiceClient


class OpenRouteServiceDataFrameAdapter:
    def __init__(self, client: OpenRouteServiceClient):
        self.client = client

    def GetDurationMatrixFromDataFrame(self, profile: str, df: pd.DataFrame) -> pd.DataFrame:
        required_cols = {"station_id", "lon", "lat"}
        if not required_cols.issubset(df.columns):
            raise ValueError(f"DataFrame must contain columns: {required_cols} but has {df.columns}")

        locations = [Location(name=row["station_id"], longitude=row["lon"], latitude=row["lat"]) for _, row in df.iterrows()]
        matrix = self.client.GetDurationMatrix(profile, locations)
        station_ids = df["station_id"].unique()
        matrix_df = pd.DataFrame(index=station_ids, columns=station_ids)
        for i, from_location in enumerate(locations):
            for j, to_location in enumerate(locations):
                matrix_df.loc[from_location.name, to_location.name] = matrix.durations[i][j]
        stacked = matrix_df.stack().reset_index()
        stacked.columns = ["station_id_from", "station_id_to", "duration_in_seconds"]
        return stacked
