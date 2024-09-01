------------
-- LOCATIONS
------------

CREATE TABLE IF NOT EXISTS locations
(
    city	                    TEXT,
    state	                    TEXT,
    timezone	                TEXT,
    grid_x	                    INTEGER,
    grid_y	                    INTEGER,
    forecast_office	            TEXT,
    radar_station	            TEXT,
    forecast_office_url	        TEXT,
    forecast_extended_url	    TEXT,
    forecast_hourly_url	        TEXT,
    gridpoints_url	            TEXT,
    observation_stations_url	TEXT,
    PRIMARY KEY                 (forecast_office, grid_x, grid_y)
);