from src.DBManager import DBManager
from src.OpenSkyApi import OpenSkyApi


def main():
    countries = [
        "United Kingdom",
        "France",
        "Deutschland",
        "Italia",
    ]

    db_manager = DBManager()
    open_sky_api = OpenSkyApi()

    db_manager.clear_aircraft()
    try:
        for country_name in countries:
            country = db_manager.get_country_by_name(country_name)

            if country is None:
                print(f"Страна не найдена в БД: {country_name}")
                continue

            print(f"Обрабатываем: {country['name']}")

            aircraft = open_sky_api.get_aircraft(country)

            print(
                f"Получено самолётов: {len(aircraft)}"
            )

            if aircraft:
                db_manager.add_aircraft(
                    aircraft,
                    country["id"],
                )

            print(
                f"Самолёты для {country['name']} "
                f"добавлены в БД."
            )

    finally:
        db_manager.close()


if __name__ == "__main__":
    main()
