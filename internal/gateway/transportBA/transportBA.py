import os
import requests
from internal.domain.stations import Stations
from internal.domain.stations_status import StationsStatus


class Client():
    def __init__(self):
        self.get_stations_url = "https://apitransporte.buenosaires.gob.ar/ecobici/gbfs/stationInformation?"
        self.get_stations_status_url = "https://apitransporte.buenosaires.gob.ar/ecobici/gbfs/stationStatus?"
        self.client = requests.Session()
        clientID = os.getenv("TRANSPORT_BA_CLIENT_ID")
        clientSecret = os.getenv("TRANSPORT_BA_SECRET")
        self.query_params = {
            "client_id": clientID,
            "client_secret": clientSecret
        }

    def GetStations(self) -> Stations:
        df = self.__get(self.get_stations_url)
        return Stations(df)

    def GetStationStatus(self) -> StationsStatus:
        df = self.__get(self.get_stations_status_url)
        return StationsStatus(df)

    def __get(self, url):
        response = self.client.get(url, params=self.query_params)
        response.raise_for_status()
        data = response.json()
        return data["data"]["stations"]
