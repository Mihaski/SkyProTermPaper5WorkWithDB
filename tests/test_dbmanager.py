from unittest.mock import MagicMock, patch

import pytest

from src.DBManager import DBManager


@pytest.fixture
def db_manager():
    """Создаёт DBManager с замоканным соединением."""
    with patch("src.DBManager.psycopg2.connect") as mock_connect:
        connection = MagicMock()
        cursor = MagicMock()

        connection.cursor.return_value.__enter__.return_value = cursor
        mock_connect.return_value = connection

        manager = DBManager()

        yield manager, connection, cursor


def test_get_countries_and_aeroplanes_count(db_manager):
    """Проверяет получение стран и количества самолётов."""
    manager, _, cursor = db_manager

    expected = [
        ("France", 10),
        ("United Kingdom", 20),
    ]
    cursor.fetchall.return_value = expected

    result = manager.get_countries_and_aeroplanes_count()

    assert result == expected
    cursor.execute.assert_called_once()
    assert "LEFT JOIN aircraft" in cursor.execute.call_args[0][0]


def test_get_all_aeroplanes(db_manager):
    """Проверяет получение всех воздушных судов."""
    manager, _, cursor = db_manager

    expected = [
        ("407a05", "EZY17DR", "United Kingdom", -3.6, 50.7, 11574.0, 171.0, 7.0, 0.0, False),
    ]
    cursor.fetchall.return_value = expected

    result = manager.get_all_aeroplanes()

    assert result == expected
    cursor.execute.assert_called_once()
    assert "FROM aircraft" in cursor.execute.call_args[0][0]


def test_get_all_aeroplanes_empty(db_manager):
    """Проверяет результат при пустой таблице."""
    manager, _, cursor = db_manager
    cursor.fetchall.return_value = []

    result = manager.get_all_aeroplanes()

    assert result == []


def test_get_avg_speed(db_manager):
    """Проверяет получение средней скорости."""
    manager, _, cursor = db_manager
    cursor.fetchone.return_value = (250.5,)

    result = manager.get_avg_speed()

    assert result == 250.5
    cursor.execute.assert_called_once()
    assert "AVG(velocity)" in cursor.execute.call_args[0][0]


def test_get_avg_speed_without_data(db_manager):
    """Проверяет результат, если нет данных о скорости."""
    manager, _, cursor = db_manager
    cursor.fetchone.return_value = (None,)

    result = manager.get_avg_speed()

    assert result is None


def test_get_aeroplanes_with_higher_speed(db_manager):
    """Проверяет получение самолётов быстрее средней скорости."""
    manager, _, cursor = db_manager

    expected = [
        ("407a05", "EZY17DR", "United Kingdom", -3.6, 50.7, 11574.0, 280.0),
    ]
    cursor.fetchall.return_value = expected

    result = manager.get_aeroplanes_with_higher_speed()

    assert result == expected
    assert "SELECT AVG(velocity)" in cursor.execute.call_args[0][0]


def test_get_aeroplanes_with_keyword(db_manager):
    """Проверяет поиск по позывному."""
    manager, _, cursor = db_manager
    cursor.fetchall.return_value = [("407a05", "EZY17DR")]

    result = manager.get_aeroplanes_with_keyword("EZY")

    assert result == [("407a05", "EZY17DR")]
    cursor.execute.assert_called_once()

    query, params = cursor.execute.call_args[0]
    assert "ILIKE %s" in query
    assert params == ("%EZY%",)


def test_get_aeroplanes_with_keyword_no_results(db_manager):
    """Проверяет поиск, который ничего не нашёл."""
    manager, _, cursor = db_manager
    cursor.fetchall.return_value = []

    result = manager.get_aeroplanes_with_keyword("UNKNOWN")

    assert result == []
    assert cursor.execute.call_args[0][1] == ("%UNKNOWN%",)


def test_add_country(db_manager):
    """Проверяет добавление страны."""
    manager, connection, cursor = db_manager

    country = {
        "name": "France",
        "latitude": 46.6,
        "longitude": 1.8,
        "min_latitude": 41.3,
        "max_latitude": 51.1,
        "min_longitude": -5.1,
        "max_longitude": 9.6,
    }

    manager.add_country(country)

    cursor.execute.assert_called_once()
    params = cursor.execute.call_args[0][1]

    assert params == (
        "France",
        46.6,
        1.8,
        41.3,
        51.1,
        -5.1,
        9.6,
    )
    connection.commit.assert_called_once()


def test_get_country_by_name(db_manager):
    """Проверяет получение страны по названию."""
    manager, _, cursor = db_manager

    cursor.fetchone.return_value = (
        1,
        "France",
        46.6,
        1.8,
        41.3,
        51.1,
        -5.1,
        9.6,
    )

    result = manager.get_country_by_name("France")

    assert result == {
        "id": 1,
        "name": "France",
        "latitude": 46.6,
        "longitude": 1.8,
        "min_latitude": 41.3,
        "max_latitude": 51.1,
        "min_longitude": -5.1,
        "max_longitude": 9.6,
    }

    assert cursor.execute.call_args[0][1] == ("France",)


def test_get_country_by_name_not_found(db_manager):
    """Проверяет поиск несуществующей страны."""
    manager, _, cursor = db_manager
    cursor.fetchone.return_value = None

    result = manager.get_country_by_name("Atlantis")

    assert result is None


def test_add_aircraft(db_manager):
    """Проверяет добавление списка воздушных судов."""
    manager, connection, cursor = db_manager

    aircraft = [
        {
            "icao24": "407a05",
            "callsign": "EZY17DR",
            "origin_country": "United Kingdom",
            "longitude": -3.6,
            "latitude": 50.7,
            "altitude": 11574.0,
            "velocity": 171.0,
            "true_track": 7.0,
            "vertical_rate": 0.0,
            "on_ground": False,
        },
        {
            "icao24": "4bc8d6",
            "callsign": "PGT40PJ",
            "origin_country": "Turkey",
            "longitude": -2.9,
            "latitude": 55.8,
            "altitude": 1684.0,
            "velocity": 125.0,
            "true_track": 340.0,
            "vertical_rate": -6.0,
            "on_ground": False,
        },
    ]

    manager.add_aircraft(aircraft, country_id=1)

    cursor.executemany.assert_called_once()
    query, values = cursor.executemany.call_args[0]

    assert "INSERT INTO aircraft" in query
    assert len(values) == 2
    assert values[0] == (
        "407a05",
        "EZY17DR",
        "United Kingdom",
        -3.6,
        50.7,
        11574.0,
        171.0,
        7.0,
        0.0,
        False,
        1,
    )
    assert values[1][-1] == 1
    connection.commit.assert_called_once()


def test_add_aircraft_empty_list(db_manager):
    """Проверяет добавление пустого списка."""
    manager, connection, cursor = db_manager

    manager.add_aircraft([], country_id=1)

    cursor.executemany.assert_called_once()
    assert cursor.executemany.call_args[0][1] == []
    connection.commit.assert_called_once()


def test_clear_aircraft(db_manager):
    """Проверяет очистку таблицы самолётов."""
    manager, connection, cursor = db_manager

    manager.clear_aircraft()

    query = cursor.execute.call_args[0][0]

    assert "TRUNCATE TABLE aircraft" in query
    assert "RESTART IDENTITY" in query
    connection.commit.assert_called_once()


def test_close(db_manager):
    """Проверяет закрытие соединения."""
    manager, connection, _ = db_manager

    manager.close()

    connection.close.assert_called_once()
