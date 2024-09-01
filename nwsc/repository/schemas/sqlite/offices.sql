----------
-- OFFICES
----------

CREATE TABLE IF NOT EXISTS offices
(
    office_id	    TEXT PRIMARY KEY,
    name	        TEXT,
    street_address	TEXT,
    city	        TEXT,
    state	        TEXT,
    zip_code	    TEXT,
    phone_number	TEXT,
    fax_number	    TEXT,
    email	        TEXT,
    url	            TEXT,
    parent_url	    TEXT,
    nws_region	    TEXT
);

CREATE TABLE IF NOT EXISTS office_counties
(
    office_id	TEXT PRIMARY KEY,
    county_url  TEXT,
    FOREIGN KEY (office_id) REFERENCES offices (office_id)
);

CREATE TABLE IF NOT EXISTS office_forecast_zones
(
    office_id	        TEXT PRIMARY KEY,
    forecast_zone_url   TEXT,
    FOREIGN KEY         (office_id) REFERENCES offices (office_id)
);

CREATE TABLE IF NOT EXISTS office_fire_zones
(
    office_id       TEXT PRIMARY KEY,
    fire_zones_url  TEXT,
    FOREIGN KEY     (office_id) REFERENCES offices (office_id)
);

CREATE TABLE IF NOT EXISTS office_observation_stations
(
    office_id               TEXT PRIMARY KEY,
    observation_station_url TEXT,
    FOREIGN KEY             (office_id) REFERENCES offices (office_id)
);

CREATE TABLE IF NOT EXISTS office_headlines
(
    retrieved_at        TEXT, -- ISO8601 timestamp
    office_id           TEXT,
    headline_id	        TEXT,
    name	            TEXT,
    title	            TEXT,
    issued_at	        TEXT, -- ISO8601 timestamp
    url	                TEXT,
    content	            TEXT,
    headline_summary	TEXT,
    office_url	        TEXT,
    is_important	    INTEGER, -- boolean
    PRIMARY KEY         (office_id, headline_id),
    FOREIGN KEY         (office_id) REFERENCES offices (office_id)
);
