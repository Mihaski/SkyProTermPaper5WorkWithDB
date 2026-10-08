import requests


class OpenStreetMapApi:
    """Класс для работы с Nominatim OpenStreetMap API."""

    URL = "https://nominatim.openstreetmap.org/search"

    def get_country(self, country_name: str) -> dict:
        """Получает информацию о стране."""

        params = {
            "q": country_name,
            "format": "json",
            "limit": 1,
            "addressdetails": 1,
        }

        headers = {
            "User-Agent": "SkyProTermPaper5WorkWithDB/1.0"
        }

        response = requests.get(
            self.URL,
            params=params,
            headers=headers,
            timeout=10,
        )

        response.raise_for_status()

        data = response.json()

        if not data:
            raise ValueError(f"Страна не найдена: {country_name}")

        country = data[0]

        boundingbox = country["boundingbox"]

        return {
            "name": country["name"],
            "latitude": float(country["lat"]),
            "longitude": float(country["lon"]),
            "min_latitude": float(boundingbox[0]),
            "max_latitude": float(boundingbox[1]),
            "min_longitude": float(boundingbox[2]),
            "max_longitude": float(boundingbox[3]),
        }