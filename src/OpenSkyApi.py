import requests


class OpenSkyApi:
    """Класс для работы с OpenSky Network API."""

    URL = "https://opensky-network.org/api/states/all"

    def get_aircraft(self, country: dict) -> list[dict]:
        """Получает самолёты, находящиеся в воздушном пространстве страны."""

        params = {
            "lamin": country["min_latitude"],
            "lamax": country["max_latitude"],
            "lomin": country["min_longitude"],
            "lomax": country["max_longitude"],
        }

        response = requests.get(
            self.URL,
            params=params,
            timeout=30,
        )

        response.raise_for_status()

        data = response.json()

        states = data.get("states", [])

        aircraft = []

        for state in states:
            aircraft.append(
                {
                    "icao24": state[0],
                    "callsign": state[1].strip() if state[1] else None,
                    "origin_country": state[2],
                    "longitude": state[5],
                    "latitude": state[6],
                    "altitude": state[7],
                    "velocity": state[9],
                    "true_track": state[10],
                    "vertical_rate": state[11],
                    "on_ground": state[8],
                }
            )

        return aircraft
