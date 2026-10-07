class Airplane:
    """Класс для работы с информацией о самолете."""

    def __init__(
        self,
        icao24: str,
        callsign: str,
        country: str,
        speed: float,
        altitude: float,
    ) -> None:
        if not isinstance(icao24, str) or not icao24.strip():
            raise ValueError("ICAO24 должен быть непустой строкой.")

        if not isinstance(callsign, str):
            raise ValueError("Позывной должен быть строкой.")

        if not isinstance(country, str) or not country.strip():
            raise ValueError("Страна должна быть непустой строкой.")

        if not isinstance(speed, (int, float)) or speed < 0:
            raise ValueError("Скорость должна быть неотрицательным числом.")

        if not isinstance(altitude, (int, float)):
            raise ValueError("Высота должна быть числом.")

        self.icao24 = icao24
        self.callsign = callsign.strip()
        self.country = country
        self.speed = speed
        self.altitude = altitude

    def compare_speed(self, other) -> int:
        """Сравнивает два самолета по скорости."""
        if not isinstance(other, Airplane):
            raise TypeError("Можно сравнивать только объекты Airplane.")

        if self.speed < other.speed:
            return -1
        if self.speed > other.speed:
            return 1
        return 0

    def compare_altitude(self, other) -> int:
        """Сравнивает два самолета по высоте."""
        if not isinstance(other, Airplane):
            raise TypeError("Можно сравнивать только объекты Airplane.")

        if self.altitude < other.altitude:
            return -1
        if self.altitude > other.altitude:
            return 1
        return 0