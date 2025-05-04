import pandas as pd

from internal.gateway.openrouteservice.client import OpenRouteServiceClient
from internal.gateway.openrouteservice.dataframe_adapter import OpenRouteServiceDataFrameAdapter
from internal.gateway.transportBA import transportBA
from internal.repository.transportBA.journeys_repository import JourneysRepository
from internal.repository.transportBA.stations_repository import StationsRepository
from internal.webscrapping.utils import preprocessStations, preprocessStationsStatus


class Service:
    def __init__(self, stationsFilename: str = None, journeysFilename: str = None):
        self.transportBAClient = transportBA.Client()
        self.stationsDao = StationsRepository(stationsFilename)
        self.journeysDao = JourneysRepository(journeysFilename)
        self.openRouteServiceDataFrameAdapter = OpenRouteServiceDataFrameAdapter(client=OpenRouteServiceClient())
        pass

    def SampleEcobiciStations(self):
        stations_df = self.transportBAClient.GetStations()
        station_status_df = self.transportBAClient.GetStationStatus()

        stations_df = preprocessStations(stations_df)
        station_status_df = preprocessStationsStatus(station_status_df)
        stations_with_status_df = pd.merge(stations_df, station_status_df, on="station_id")

        self.stationsDao.AppendWithJobRunAt(stations_with_status_df)
        return

    def UpdateEcobiciStationsDurations(self):
        stations_with_coords_df = self.stationsDao.GroupByStationIDWithCoordinates()
        length = len(stations_with_coords_df)
        lower, stations_per_req = 0, 59  # max of 59 elements in request

        journeys_df = pd.DataFrame()
        for i in range(0, int(length / 59)):
            stations_df_short = stations_with_coords_df.iloc[lower * stations_per_req:(lower + 1) * stations_per_req]
            df = self.openRouteServiceDataFrameAdapter.GetDurationMatrixFromDataFrame("cycling-regular", stations_df_short)
            journeys_df = pd.concat([journeys_df, df], ignore_index=True)

        self.journeysDao.Update(journeys_df, subset=["station_id_from", "station_id_to"])
        return
