import typer

from internal import webscrapping
from internal.platform.environment.environment import set_environment

app = typer.Typer()
set_environment("./.env")
service = webscrapping.Service(
    stationsFilename="./data/stations.csv",
    journeysFilename="./data/journeys.csv")


@app.command("sample-ecobici-stations")
def SampleEcobiciStations():
    service.SampleEcobiciStations()


@app.command("update-ecobici-stations-durations")
def UpdateEcobiciStationsDurations():
    service.UpdateEcobiciStationsDurations()


if __name__ == "__main__":
    app()
