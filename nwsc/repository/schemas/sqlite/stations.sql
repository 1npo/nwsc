-----------
-- STATIONS
-----------

CREATE TABLE IF NOT EXISTS stations
(
    station_id	            TEXT PRIMARY KEY,
    name	                TEXT,
    timezone	            TEXT,
    lat	                    REAL,
    lon	                    REAL,
    elevation_m	            REAL,
    elevation_mi	        REAL,
    forecast_url	        TEXT,
    county_url	            TEXT,
    fire_weather_zone_url	TEXT
);
