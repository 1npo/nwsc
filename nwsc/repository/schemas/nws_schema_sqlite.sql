-- nwsc schema - sqlite


------------
-- LOCATIONS
------------

CREATE TABLE IF NOT EXISTS locations
(
    city	                    TEXT
    state	                    TEXT
    timezone	                TEXT
    grid_x	                    INTEGER
    grid_y	                    INTEGER
    county_warning_area	        TEXT
    radar_station	            TEXT
    forecast_office_url	        TEXT
    forecast_extended_url	    TEXT
    forecast_hourly_url	        TEXT
    gridpoints_url	            TEXT
    observation_stations_url	TEXT
);

----------
-- OFFICES
----------

-- related to office_urls
CREATE TABLE IF NOT EXISTS offices
(
    office_id	    TEXT
    name	        TEXT
    street_address	TEXT
    city	        TEXT
    state	        TEXT
    zip_code	    TEXT
    phone_number	TEXT
    fax_number	    TEXT
    email	        TEXT
    url	            TEXT
    parent_url	    TEXT
    nws_region	    TEXT
);

-- related to offices
CREATE TABLE IF NOT EXISTS office_urls
(
    office_id	TEXT
    url_type	TEXT
    url	        TEXT
);

CREATE TABLE IF NOT EXISTS office_headlines
(
    headline_id	        TEXT
    name	            TEXT
    title	            TEXT
    issued_at	        TEXT -- ISO8601 timestamp
    url	                TEXT
    content	            TEXT
    headline_summary	TEXT
    office_url	        TEXT
    is_important	    INTEGER -- boolean
);

-----------
-- PRODUCTS
-----------

CREATE TABLE IF NOT EXISTS products
(
    product_id	    TEXT
    wmo_id	        TEXT
    name	        TEXT
    code	        TEXT
    text	        TEXT
    issuing_office	TEXT
    issued_at	    TEXT -- ISO8601 timestamp
);

CREATE TABLE IF NOT EXISTS product_locations
(
    code	TEXT
    name	TEXT
);

CREATE TABLE IF NOT EXISTS product_types
(
    code	TEXT
    name	TEXT
);

-----------
-- PRODUCTS
-----------

-- related to:
-------------------------
-- radar_data_acquisition
-- radar_performance
-- radar_adaptation
CREATE TABLE IF NOT EXISTS radar_stations
(
    radar_station_id	                TEXT
    name	                            TEXT
    station_type	                    TEXT
    timezone	                        TEXT
    lat	                                REAL
    lon	                                REAL
    server_host	                        TEXT
    reporting_host	                    TEXT
    elevation_m	                        REAL
    elevation_mi	                    REAL 
    latency_current_s	                REAL
    latency_average_s	                REAL
    latency_max_s	                    REAL
    latency_nexrad_l2_last_received_at	TEXT -- ISO8601 timestamp
    max_latency_at	                    TEXT -- ISO8601 timestamp
);

-- related to radar_path_loss
CREATE TABLE IF NOT EXISTS radar_adaptation
(
    refreshed_at	                                TEXT -- ISO8601 timestamp
    reporting_host	                                TEXT
    transmitter_frequency	                        INTEGER
    transmitter_power_data_watts_factor	            REAL
    antenna_gain_incl_radome	                    REAL
    coho_power_at_a1j4	                            REAL
    stalo_power_at_a1j2	                            REAL
    horizontal_receiver_noise_long_pulse	        REAL
    horizontal_receiver_noise_short_pulse	        REAL
    transmitter_spectrum_filter_installed	        TEXT -- bool? are "F" and "T" the only values?
    pulse_width_transmitter_out_long_pulse	        INTEGER
    pulse_width_transmitter_out_short_pulse	        INTEGER
    ame_noise_source_horizontal_excess_noise_ratio	REAL
    ame_horizontal_test_signal_power	            REAL
);

CREATE TABLE IF NOT EXISTS radar_performance
(
    refreshed_at	                    TEXT -- ISO8601 timestamp
    performance_checked_at	            TEXT -- ISO8601 timestamp
    reporting_host	                    TEXT
    ntp_status	                        INTEGER
    command_channel	                    TEXT
    linearity	                        REAL
    power_source	                    TEXT
    fuel_level_pc	                    REAL
    dynamic_range_db	                REAL
    transmitter_peak_power_kw	        REAL
    transmitter_recycle_count	        INTEGER
    transmitter_imbalance_db	        REAL
    transmitter_leaving_air_temp_c	    REAL
    transmitter_leaving_air_temp_f	    REAL
    shelter_temp_c	                    REAL
    shelter_temp_f	                    REAL
    radome_air_temp_c	                REAL
    radome_air_temp_f	                REAL
    horizontal_noise_temp_c	            REAL
    horizontal_noise_temp_f	            REAL
    transitional_power_source	        TEXT
    elevation_encoder_light	            TEXT
    azimuth_encoder_light	            TEXT
    horizontal_delta_db	                REAL
    vertical_delta_db	                REAL
    receiver_bias_db	                REAL
    horizontal_short_pulse_noise_db_m	REAL
    horizontal_short_pulse_noise_db_mi	REAL
    horizontal_long_pulse_noise_db_m	REAL
    horizontal_long_pulse_noise_db_mi	REAL
);

CREATE TABLE IF NOT EXISTS radar_path_loss
(
    wg04_circulator	                REAL
    wg02_harmonic_filter	        REAL
    wg06_spectrum_filter	        REAL
    ifd_rif_anti_alias_filter	    REAL
    ifd_burst_anti_alias_filter	    REAL
    a6_arc_detector	                REAL
    transmitter_coupler_coupling	REAL
    vertical_f_heliax_to_4at16	    REAL
    horizontal_f_heliax_to_4at17	REAL
    at4_attenuator	                REAL
    waveguide_klystron_to_switch	REAL
);

CREATE TABLE IF NOT EXISTS radar_data_acquisition
(
    refreshed_at	                        TEXT
    reporting_host	                        TEXT
    mode	                                TEXT
    status	                                TEXT
    control_status	                        TEXT
    operability_status	                    TEXT
    super_resolution_status	                TEXT
    generator_state	                        TEXT
    alarm_summary	                        TEXT
    resolution_version	                    TEXT
    nexrad_l2_path	                        TEXT
    volume_coverage_pattern	                TEXT
    build_number	                        REAL
    average_tx_power_w	                    REAL
    reflectivity_calibration_correction_db	REAL
);

-- related to network_interfaces
CREATE TABLE IF NOT EXISTS radar_servers
(
    host	                        TEXT
    server_type	                    TEXT
    up_since	                    TEXT -- ISO8601 timestamp
    hardware_refreshed_at	        TEXT -- ISO8601 timestamp
    network_interfaces_refreshed_at	TEXT -- ISO8601 timestamp
    cpu	                            REAL
    memory	                        REAL
    io_utilization	                REAL
    disk	                        INTEGER
    load_1	                        REAL
    load_5	                        REAL
    load_15	                        REAL
    command_last_executed	        TEXT
    command_last_executed_at	    TEXT -- ISO8601 timestamp
    command_last_nexrad_data_at	    TEXT -- ISO8601 timestamp
    command_last_received	        TEXT
    command_last_received_at	    TEXT -- ISO8601 timestamp
    command_last_refreshed_at	    TEXT -- ISO8601 timestamp
    ldm_refreshed_at	            TEXT -- ISO8601 timestamp
    ldm_latest_product_at	        TEXT -- ISO8601 timestamp
    ldm_oldest_product_at	        TEXT -- ISO8601 timestamp
    ldm_storage_size	            INTEGER
    ldm_count	                    INTEGER
    is_ldm_active	                INTEGER -- boolean
    is_server_active	            INTEGER -- boolean
    is_server_primary	            INTEGER -- boolean
    is_server_aggregate	            INTEGER -- boolean
    is_server_locked	            INTEGER -- boolean
    is_radar_network_up	            INTEGER -- boolean
    collection_time	                TEXT -- ISO8601 timestamp
    reporting_host	                TEXT
    last_ping_at	                TEXT -- ISO8601 timestamp
);

CREATE TABLE IF NOT EXISTS rader_server_ping_responses
(
    ldm_name	        TEXT
    ldm_response	    INTEGER -- boolean
    radar_name	        TEXT
    radar_response	    INTEGER -- boolean
    server_name	        TEXT
    server_response	    INTEGER -- boolean
    network_name	    TEXT
    network_response	INTEGER -- boolean
)

-- related to radar_servers
CREATE TABLE IF NOT EXISTS network_interfaces
(
    interface_name	    TEXT
    is_interface_active	INTEGER -- boolean
    packets_out_ok	    INTEGER
    packets_out_error	INTEGER
    packets_out_dropped	INTEGER
    packets_out_overrun	INTEGER
    packets_in_ok	    INTEGER
    packets_in_error	INTEGER
    packets_in_dropped	INTEGER
    packets_in_overrun	INTEGER
);

CREATE TABLE IF NOT EXISTS radar_queues
(
    host	            TEXT
    arrived_at	        TEXT -- ISO8601 timestamp
    created_at	        TEXT -- ISO8601 timestamp
    station_id	        TEXT
    queue_item_type	    TEXT
    feed	            TEXT
    resolution_version	INTEGER
    sequence_number	    TEXT
    size	            INTEGER    
);

CREATE TABLE IF NOT EXISTS radar_station_alarms
(
    status	        TEXT
    message	        TEXT
    active_channel	INTEGER
    event_at	    TEXT -- ISO8601 timestamp
);

-----------
-- STATIONS
-----------

CREATE TABLE IF NOT EXISTS stations
(
    station_id	            TEXT
    name	                TEXT
    timezone	            TEXT
    lat	                    REAL
    lon	                    REAL
    elevation_m	            REAL
    elevation_mi	        REAL
    forecast_url	        TEXT
    county_url	            TEXT
    fire_weather_zone_url	TEXT
);

----------
-- WEATHER
----------

-- related to observations_cloud_layers
CREATE TABLE IF NOT EXISTS observations
(
    observed_at	                TEXT -- ISO8601 timestamp
    icon_url	                TEXT
    text_description	        TEXT
    raw_message	                TEXT
    station_elevation_m	        INTEGER
    station_elevation_mi	    REAL
    temperature_c	            REAL
    temperature_f	            REAL
    dew_point_c	                REAL
    dew_point_f	                REAL
    wind_direction_deg_ang	    INTEGER
    wind_direction_compass	    TEXT
    wind_speed_kmh	            REAL
    wind_speed_mph	            REAL
    wind_gust_kmh	            REAL
    wind_gust_mph	            REAL
    barometric_pressure_pa	    INTEGER
    barometric_pressure_inhg	REAL
    sea_level_pressure_pa	    INTEGER
    sea_level_pressure_inhg	    REAL
    visibility_m	            INTEGER
    visibility_mi	            REAL
    max_temp_last_24h_c	        REAL
    max_temp_last_24h_f	        REAL
    min_temp_last_24h_c	        REAL
    min_temp_last_24h_f	        REAL
    precip_last_1h_mm	        REAL
    precip_last_3h_mm	        REAL
    precip_last_6h_mm	        REAL
    relative_humidity_pc	    REAL
    wind_chill_c	            REAL
    wind_chill_f	            REAL
    heat_index_c	            REAL
    heat_index_f	            REAL
);

-- related to observations
CREATE TABLE IF NOT EXISTS observations_cloud_layers
(
    cloud_layer_height	    TEXT
    cloud_layer_description	TEXT
);

CREATE TABLE IF NOT EXISTS forecasts
(
    generated_at	                TEXT -- ISO8601 timestamp
    updated_at	                    TEXT -- ISO8601 timestamp
    num	                            INTEGER
    name	                        TEXT
    start_at	                    TEXT -- ISO8601 timestamp
    end_at	                        TEXT -- ISO8601 timestamp
    name	                        TEXT
    forecast_short	                TEXT
    forecast_detailed	            TEXT
    forecast_icon_url	            TEXT
    is_daytime	                    INTEGER -- boolean
    wind_speed	                    TEXT
    wind_direction	                TEXT
    temperature_trend	            TEXT
    temperature_c	                REAL
    temperature_f	                REAL
    dew_point_c	                    REAL
    dew_point_f	                    REAL
    relative_humidity_pc	        REAL
    precipitation_probability_pc	REAL
);

----------
-- WEATHER
----------

-- related to:
-- - zone_county_warning_areas
-- - zone_observation_stations
-- - zone_forecast_offices
-- - zone_timezones
CREATE TABLE IF NOT EXISTS zones
(
    zone_id	        TEXT
    grid_id	        TEXT
    awips_id	    TEXT
    name	        TEXT
    zone_type	    TEXT
    state	        TEXT
    url	            TEXT
    effective_at	TEXT -- ISO8601 timestamp
    expires_at	    TEXT -- ISO8601 timestamp
    -- add multi_polygon
);

-- related to zones
CREATE TABLE IF NOT EXISTS zone_county_warning_areas
(
    zone_id	            TEXT
    county_warning_area	TEXT
);

-- related to zones
CREATE TABLE IF NOT EXISTS zone_observation_stations
(
    zone_id	            TEXT
    observation_station	TEXT
);

-- related to zones
CREATE TABLE IF NOT EXISTS zone_forecast_offices
(
    zone_id	        TEXT
    forecast_office	TEXT
);

-- related to zones
CREATE TABLE IF NOT EXISTS zone_timezones
(
    zone_id	    TEXT
    timezone	TEXT
);

CREATE TABLE IF NOT EXISTS zone_forecast:
(
    forecasted_at	    TEXT -- ISO8601 timestamp
    num	                INTEGER
    name	            TEXT
    forecast_detailed	TEXT
);