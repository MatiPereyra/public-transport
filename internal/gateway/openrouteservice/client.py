import os
import requests
from typing import List

from internal.domain.locations import Location, MatrixResponse


class OpenRouteServiceClient:
    def __init__(self):
        self.api_key = os.getenv("HEIGIT_OPENROUTESERVICE_API_KEY")
        if not self.api_key:
            raise ValueError("HEIGIT_OPENROUTESERVICE_API_KEY environment variable is not set")
        self.base_url = "https://api.openrouteservice.org/v2/matrix/{profile}"
        self.client = requests.Session()
        self.headers = {
            "Content-Type": "application/json; charset=utf-8",
            "Accept": "application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8",
            "Authorization": self.api_key
        }

    def GetDurationMatrix(self, profile: str, locations: List[Location]) -> MatrixResponse:
        """

        :param profile: values driving-car, cycling-regular
        :param locations:
        :return:
        """
        payload = {
            "locations": [loc.to_list() for loc in locations],
            "metrics": ["duration"]  # could also pass distance
        }
        response = self.client.post(self.base_url.format(profile=profile), json=payload, headers=self.headers)
        try:
            response.raise_for_status()
        except:
            error = response.json()
            print(error)
            response.raise_for_status()
        return MatrixResponse.from_dict(response.json())


