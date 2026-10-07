from requests import get

from src.BaseAPI import BaseAPI


class APIAdapter(BaseAPI):

    def __init__(self) -> None:
        self.openstreetmap_url = "https://nominatim.openstreetmap.org/search"
        self.opensky_url = "https://opensky-network.org/api/states/all?"
        self.aeroplanes = None

    def get_data(self, country: str) -> None:
        """Получает информацию о самолетах в воздушном пространстве страны."""

        headers_nominatim = {
            "User-Agent": "test-app/1.0",
        }

        params_nominatim = {
            "country": country,
            "format": "json",
            "limit": 1,
        }

        response = get(
            url=self.openstreetmap_url,
            params=params_nominatim,
            headers=headers_nominatim,
        )

        data = response.json()

        geo_coordinates = data[0].get("boundingbox")

        params = {
            "lamin": geo_coordinates[0],
            "lamax": geo_coordinates[1],
            "lomin": geo_coordinates[2],
            "lomax": geo_coordinates[3],
        }

        response = get(
            url=self.opensky_url,
            params=params,
        )

        self.aeroplanes = response.json()
