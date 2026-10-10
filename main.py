from src.DBManager import DBManager
from src.OpenSkyApi import OpenSkyApi
from src.OpenStreetMapApi import OpenStreetMapApi


def main():
    db_manager = DBManager()
    osm_api = OpenStreetMapApi()
    open_sky_api = OpenSkyApi()

    country_names = [
        "United Kingdom",
        "France",
        "Germany",
        "Italy",
    ]

    try:
        # Получаем страны через OpenStreetMap и сохраняем в БД.
        for country_name in country_names:
            country_data = osm_api.get_country(country_name)
            db_manager.add_country(country_data)

            print(f"Страна добавлена или уже существует: {country_data['name']}")

        # Загружаем актуальные данные о самолётах.
        db_manager.clear_aircraft()

        for country_name in country_names:
            country_data = osm_api.get_country(country_name)
            country = db_manager.get_country_by_name(country_data["name"])

            if country is None:
                print(f"Страна не найдена в БД: {country_data['name']}")
                continue

            print(f"Обрабатываем: {country['name']}")

            aircraft = open_sky_api.get_aircraft(country)

            print(f"Получено самолётов: {len(aircraft)}")

            if aircraft:
                db_manager.add_aircraft(
                    aircraft,
                    country["id"],
                )

            print(f"Самолёты для {country['name']} добавлены в БД.")

        print("Загрузка данных завершена.")

    finally:
        db_manager.close()


if __name__ == "__main__":
    main()
