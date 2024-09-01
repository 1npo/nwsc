---------
-- ALERTS
---------

CREATE TABLE IF NOT EXISTS alerts
(
    retrieved_at        TEXT, -- ISO8601 timestamp
    alert_id	        TEXT,
    url	                TEXT,
    updated_at	        TEXT, -- ISO8601 timestamp
    title	            TEXT,
    headline	        TEXT,
    description	        TEXT,
    instruction	        TEXT,
    urgency	            TEXT,
    area_description	TEXT,
    sent_by	            TEXT,
    sent_by_name	    TEXT,
    sent_at	            TEXT, -- ISO8601 timestamp
    effective_at	    TEXT, -- ISO8601 timestamp
    ends_at	            TEXT, -- ISO8601 timestamp
    status	            TEXT,
    message_type	    TEXT,
    category	        TEXT,
    certainty	        TEXT,
    event_type	        TEXT,
    onset_at	        TEXT, -- ISO8601 timestamp
    expires_at	        TEXT, -- ISO8601 timestamp
    response_type	    TEXT,
    PRIMARY KEY         (retrieved_at, alert_id)
);

CREATE TABLE IF NOT EXISTS prior_alerts
(
    retrieved_at    TEXT, -- ISO8601 timestamp
    parent_alert_id TEXT,
    prior_alert_id	TEXT,
    url	            TEXT,
    sent_at	        TEXT, -- ISO8601 timestamp
    PRIMARY KEY     (retrieved_at, parent_alert_id, prior_alert_id)
);

CREATE TABLE IF NOT EXISTS alert_affected_zones
(
    retrieved_at        TEXT, -- ISO8601 timestamp
    alert_id            TEXT,
    affected_zone_url   TEXT,
    PRIMARY KEY         (retrieved_at, alert_id, affected_zone_url)
);

CREATE TABLE IF NOT EXISTS alert_areas_ugc
(
    retrieved_at        TEXT, -- ISO8601 timestamp
    alert_id            TEXT,
    cap_ugc_area        TEXT,
    PRIMARY KEY         (retrieved_at, alert_id, cap_ugc_area)
);

CREATE TABLE IF NOT EXISTS alert_areas_same
(
    retrieved_at        TEXT, -- ISO8601 timestamp
    alert_id            TEXT,
    cap_same_area       TEXT,
    PRIMARY KEY         (retrieved_at, alert_id, cap_same_area)
);

CREATE TABLE IF NOT EXISTS alert_cap_awips_ids
(
    retrieved_at        TEXT, -- ISO8601 timestamp
    alert_id            TEXT,
    cap_awips_id        TEXT,
    PRIMARY KEY         (retrieved_at, alert_id, cap_awips_id)
);

CREATE TABLE IF NOT EXISTS alert_cap_wmo_ids
(
    retrieved_at        TEXT, -- ISO8601 timestamp
    alert_id            TEXT,
    cap_wmo_id          TEXT,
    PRIMARY KEY         (retrieved_at, alert_id, cap_wmo_id)
);

CREATE TABLE IF NOT EXISTS alert_cap_headlines
(
    retrieved_at        TEXT, -- ISO8601 timestamp
    alert_id            TEXT,
    cap_headline        TEXT,
    PRIMARY KEY         (retrieved_at, alert_id, cap_headline)
);

CREATE TABLE IF NOT EXISTS alert_cap_blocked_channels
(
    retrieved_at        TEXT, -- ISO8601 timestamp
    alert_id            TEXT,
    cap_blocked_channel TEXT,
    PRIMARY KEY         (retrieved_at, alert_id, cap_blocked_channel)
);

CREATE TABLE IF NOT EXISTS alert_cap_vtecs
(
    retrieved_at        TEXT, -- ISO8601 timestamp
    alert_id            TEXT,
    cap_vtec            TEXT,
    PRIMARY KEY         (retrieved_at, alert_id, cap_vtec)
);

---------------
-- ALERT COUNTS
---------------

CREATE TABLE IF NOT EXISTS alert_counts_total_land_marine
(
    retrieved_at    TEXT PRIMARY KEY, -- ISO8601 timestamp
    total_alerts	INTEGER,
    land_alerts	    INTEGER,
    marine_alerts	INTEGER
);

CREATE TABLE IF NOT EXISTS alert_counts_region
(
    retrieved_at    TEXT, -- ISO8601 timestamp
    region_name	    TEXT,
    region_alerts	INTEGER,
    PRIMARY KEY     (retrieved_at, region_name)
);

CREATE TABLE IF NOT EXISTS alert_counts_area
(
    retrieved_at    TEXT, -- ISO8601 timestamp
    area_name	    TEXT,
    area_alerts	    INTEGER,
    PRIMARY KEY     (retrieved_at, area_name)
);

CREATE TABLE IF NOT EXISTS alert_counts_zone
(
    retrieved_at    TEXT, -- ISO8601 timestamp
    zone_name	    TEXT,
    zone_alerts	    INTEGER,
    PRIMARY KEY     (retrieved_at, zone_name)
);
