from dataclasses import dataclass
from typing import Dict, Any, List


@dataclass
class Location:
    name: str
    longitude: float
    latitude: float

    def to_list(self) -> list:
        return [self.longitude, self.latitude]

    def __str__(self):
        return f"({self.latitude}, {self.longitude})"


@dataclass
class LocationPoint:
    location: Location
    snapped_distance: float  # unused, can eventually be null or not be present

    @staticmethod
    def from_dict(data: dict) -> 'LocationPoint':
        loc = Location(longitude=data["location"][0], latitude=data["location"][1], name=data.get("name"))
        return LocationPoint(location=loc, snapped_distance=data.get("snapped_distance"))


@dataclass
class Metadata:
    attribution: str
    service: str
    timestamp: int
    query: Dict[str, Any]
    engine: Dict[str, Any]


@dataclass
class MatrixResponse:
    durations: List[List[float]]
    destinations: List[LocationPoint]
    sources: List[LocationPoint]
    metadata: Metadata

    @staticmethod
    def from_dict(data: dict) -> 'MatrixResponse':
        return MatrixResponse(
            durations=data["durations"],
            destinations=[LocationPoint.from_dict(d) for d in data["destinations"]],
            sources=[LocationPoint.from_dict(s) for s in data["sources"]],
            metadata=Metadata(**data["metadata"])
        )
