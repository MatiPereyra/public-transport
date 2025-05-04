import pandas as pd


def preprocessStations(stations_df: pd.DataFrame) -> pd.DataFrame:
    return stations_df.explode("groups")


def preprocessStationsStatus(stations_status_df: pd.DataFrame) -> pd.DataFrame:
    stations_status_df["status_last_reported_utc"] = pd.to_datetime(stations_status_df["last_reported"], unit="s", utc=True)
    return stations_status_df
