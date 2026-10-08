import psycopg2


class DBManager:
    """Класс для работы с базой данных PostgreSQL."""

    def __init__(
        self,
        database: str,
        user: str,
        password: str,
        host: str = "localhost",
        port: int = 5432,
    ):
        """Подключение к базе данных."""

        self.connection = psycopg2.connect(
            database=database,
            user=user,
            password=password,
            host=host,
            port=port,
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
