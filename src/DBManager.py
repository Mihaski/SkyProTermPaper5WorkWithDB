import os

import psycopg2
from dotenv import load_dotenv

# нужно при первом запуске, возможно как то оптимизировать
load_dotenv()


class DBManager:
    """Класс для работы с базой данных PostgreSQL."""

    def __init__(self):
        """Подключение к базе данных."""

        self.connection = psycopg2.connect(
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
        )

    def get_countries_and_aeroplanes_count(self):
        """Возвращает список стран и количество самолётов
        в их воздушном пространстве.
        """

        query = """
            SELECT
                c.name,
                COUNT(a.id) AS aeroplanes_count
            FROM countries AS c
            LEFT JOIN aircraft AS a
                ON c.id = a.country_id
            GROUP BY c.id, c.name
            ORDER BY c.name;
        """

        with self.connection.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()

    def get_all_aeroplanes(self):
        """Возвращает список всех воздушных судов."""

        query = """
            SELECT
                icao24,
                callsign,
                origin_country,
                longitude,
                latitude,
                altitude,
                velocity,
                true_track,
                vertical_rate,
                on_ground
            FROM aircraft
            ORDER BY id;
        """

        with self.connection.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()

    def get_avg_speed(self):
        """Возвращает среднюю скорость всех самолётов."""

        query = """
            SELECT AVG(velocity)
            FROM aircraft
            WHERE velocity IS NOT NULL;
        """

        with self.connection.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchone()[0]

    def get_aeroplanes_with_higher_speed(self):
        """Возвращает самолёты, скорость которых выше средней."""

        query = """
            SELECT
                icao24,
                callsign,
                origin_country,
                longitude,
                latitude,
                altitude,
                velocity
            FROM aircraft
            WHERE velocity > (
                SELECT AVG(velocity)
                FROM aircraft
                WHERE velocity IS NOT NULL
            )
            ORDER BY velocity DESC;
        """

        with self.connection.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()

    def get_aeroplanes_with_keyword(self, keyword: str):
        """Возвращает самолёты, в позывном которых
        содержатся переданные символы.
        """

        query = """
            SELECT
                icao24,
                callsign,
                origin_country,
                longitude,
                latitude,
                altitude,
                velocity
            FROM aircraft
            WHERE callsign ILIKE %s
            ORDER BY callsign;
        """

        with self.connection.cursor() as cursor:
            cursor.execute(query, (f"%{keyword}%",))
            return cursor.fetchall()

    def close(self):
        """Закрывает соединение с базой данных."""

        self.connection.close()

    def add_country(self, country: dict):
        """Добавляет страну в базу данных."""

        query = """
            INSERT INTO countries (
                name,
                latitude,
                longitude,
                min_latitude,
                max_latitude,
                min_longitude,
                max_longitude
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (name) DO NOTHING;
        """

        with self.connection.cursor() as cursor:
            cursor.execute(
                query,
                (
                    country["name"],
                    country["latitude"],
                    country["longitude"],
                    country["min_latitude"],
                    country["max_latitude"],
                    country["min_longitude"],
                    country["max_longitude"],
                ),
            )

        self.connection.commit()

    def get_country_by_name(self, name: str):
        """Возвращает страну по названию."""

        query = """
            SELECT
                id,
                name,
                latitude,
                longitude,
                min_latitude,
                max_latitude,
                min_longitude,
                max_longitude
            FROM countries
            WHERE name = %s;
        """

        with self.connection.cursor() as cursor:
            cursor.execute(query, (name,))
            row = cursor.fetchone()

        if row is None:
            return None

        return {
            "id": row[0],
            "name": row[1],
            "latitude": row[2],
            "longitude": row[3],
            "min_latitude": row[4],
            "max_latitude": row[5],
            "min_longitude": row[6],
            "max_longitude": row[7],
        }

    def add_aircraft(self, aircraft: list[dict], country_id: int):
        """Добавляет список воздушных судов в базу данных."""

        query = """
            INSERT INTO aircraft (
                icao24,
                callsign,
                origin_country,
                longitude,
                latitude,
                altitude,
                velocity,
                true_track,
                vertical_rate,
                on_ground,
                country_id
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """

        values = [
            (
                airplane["icao24"],
                airplane["callsign"],
                airplane["origin_country"],
                airplane["longitude"],
                airplane["latitude"],
                airplane["altitude"],
                airplane["velocity"],
                airplane["true_track"],
                airplane["vertical_rate"],
                airplane["on_ground"],
                country_id,
            )
            for airplane in aircraft
        ]

        with self.connection.cursor() as cursor:
            cursor.executemany(query, values)

        self.connection.commit()

    def clear_aircraft(self):
        """Очищает таблицу воздушных судов."""

        query = """
            TRUNCATE TABLE aircraft RESTART IDENTITY;
        """

        with self.connection.cursor() as cursor:
            cursor.execute(query)

        self.connection.commit()
