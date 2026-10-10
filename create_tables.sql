CREATE TABLE IF NOT EXISTS countries (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
    min_latitude DOUBLE PRECISION NOT NULL,
    max_latitude DOUBLE PRECISION NOT NULL,
    min_longitude DOUBLE PRECISION NOT NULL,
    max_longitude DOUBLE PRECISION NOT NULL
);


CREATE TABLE IF NOT EXISTS aircraft (
    id SERIAL PRIMARY KEY,
    icao24 VARCHAR(20) NOT NULL,
    callsign VARCHAR(20),
    origin_country VARCHAR(100),
    longitude DOUBLE PRECISION,
    latitude DOUBLE PRECISION,
    altitude DOUBLE PRECISION,
    velocity DOUBLE PRECISION,
    true_track DOUBLE PRECISION,
    vertical_rate DOUBLE PRECISION,
    on_ground BOOLEAN,
    country_id INTEGER REFERENCES countries(id)
);