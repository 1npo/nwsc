-- nwsc schema: sqlite


/****************
    ALERTS
*****************/


-- related to prior_alerts
CREATE TABLE IF NOT EXISTS alerts
(
    alert_id: str
    url: str
    updated_at: datetime
    title: str
    headline: str
    description: str
    instruction: str
    urgency: str
    area_description: str
    affected_zones_urls: list
    areas_ugc: list
    areas_same: list
    sent_by: str
    sent_by_name: str
    sent_at: datetime
    effective_at: datetime
    ends_at: datetime
    status: str
    message_type: str
    category: str
    certainty: str
    event_type: str
    onset_at: datetime
    expires_at: datetime
    response_type: str
    cap_awips_id: list
    cap_wmo_id: list
    cap_headline: list
    cap_blocked_channels: list
    cap_vtec: list
);

-- related to alerts
CREATE TABLE IF NOT EXISTS prior_alerts
(
    prior_alert_id: str
    url: str
    sent_at: datetime
);

CREATE TABLE IF NOT EXISTS alert_counts
(
    total: int
    land: int
    marine: int
    region_name: str
    region_count: int
    area_name: str
    area_count: int
    zone_name: str
    zone_count: int
);


/****************
    AVIATION
*****************/


CREATE TABLE IF NOT EXISTS sigmets
(
    url: str
    issued_at: datetime
    effective_at: datetime
    expires_at: datetime
    fir: str
    atsu: str
    sequence: str
    phenomenon: str
    -- add area_polygon
);

CREATE TABLE IF NOT EXISTS center_weather_advisories
(
    url: str
    text: str
    cwsu: str
    sequence: str
    issued_at: datetime
    effective_at: datetime
    expires_at: datetime
    observed_property_url: str
    -- add area_polygon
);

CREATE TABLE IF NOT EXISTS central_weather_service_units
(
    cwsu_id: str
    name: str
    street: str
    city: str
    state: str
    zip_code: str
    email: str
    fax: str
    phone: str
    url: str
    nws_region: str
);


/****************
    LOCATIONS
*****************/


CREATE TABLE IF NOT EXISTS locations
(
    city: str
    state: str
    timezone: str
    grid_x: int
    grid_y: int
    county_warning_area: str
    radar_station: str
    forecast_office_url: str
    forecast_extended_url: str
    forecast_hourly_url: str
    gridpoints_url: str
    observation_stations_url: str
);


/****************
    OFFICES
*****************/


-- related to office_urls
CREATE TABLE IF NOT EXISTS offices
(
    office_id: str
    name: str
    street_address: str
    city: str
    state: str
    zip_code: str
    phone_number: str
    fax_number: str
    email: str
    url: str
    parent_url: str
    nws_region: str
);

-- related to offices
CREATE TABLE IF NOT EXISTS office_urls
(
    office_id: str
    url_type: str
    url: str
);

CREATE TABLE IF NOT EXISTS office_headlines
(
    headline_id: str
    name: str
    title: str
    issued_at: datetime
    url: str
    content: str
    headline_summary: str
    office_url: str
    is_important: bool
);


/****************
    PRODUCTS
*****************/


CREATE TABLE IF NOT EXISTS products
(
    product_id: str
    wmo_id: str
    name: str
    code: str
    text: str
    issuing_office: str
    issued_at: datetime
);

CREATE TABLE IF NOT EXISTS product_locations
(
    code: str
    name: str
);

CREATE TABLE IF NOT EXISTS product_types
(
    code: str
    name: str
);


/****************
    PRODUCTS
*****************/


-- related to radar_data_acquisition, radar_performance, radar_adaptation
CREATE TABLE IF NOT EXISTS radar_stations
(
    radar_station_id: str
    name: str
    station_type: str
    timezone: str
    lat: float
    lon: float
    server_host: str
    reporting_host: str
    elevation_m: float
    elevation_mi: float 
    latency_current_s: float
    latency_average_s: float
    latency_max_s: float
    latency_nexrad_l2_last_received_at: datetime
    max_latency_at: datetime
);

-- related to radar_path_loss
CREATE TABLE IF NOT EXISTS radar_adaptation
(
    refreshed_at: datetime
    reporting_host: str
    transmitter_frequency: int
    transmitter_power_data_watts_factor: float
    antenna_gain_incl_radome: float
    coho_power_at_a1j4: float
    stalo_power_at_a1j2: float
    horizontal_receiver_noise_long_pulse: float
    horizontal_receiver_noise_short_pulse: float
    transmitter_spectrum_filter_installed: str # bool? are "F" and "T" the only values?
    pulse_width_transmitter_out_long_pulse: int
    pulse_width_transmitter_out_short_pulse: int
    ame_noise_source_horizontal_excess_noise_ratio: float
    ame_horizontal_test_signal_power: float
);

CREATE TABLE IF NOT EXISTS radar_performance
(
    refreshed_at: datetime
    performance_checked_at: datetime
    reporting_host: str
    ntp_status: int
    command_channel: str
    linearity: float
    power_source: str
    fuel_level_pc: float
    dynamic_range_db: float
    transmitter_peak_power_kw: float
    transmitter_recycle_count: int
    transmitter_imbalance_db: float
    transmitter_leaving_air_temp_c: float
    transmitter_leaving_air_temp_f: float
    shelter_temp_c: float
    shelter_temp_f: float
    radome_air_temp_c: float
    radome_air_temp_f: float
    horizontal_noise_temp_c: float
    horizontal_noise_temp_f: float
    transitional_power_source: str
    elevation_encoder_light: str
    azimuth_encoder_light: str
    horizontal_delta_db: float
    vertical_delta_db: float
    receiver_bias_db: float
    horizontal_short_pulse_noise_db_m: float
    horizontal_short_pulse_noise_db_mi: float
    horizontal_long_pulse_noise_db_m: float
    horizontal_long_pulse_noise_db_mi: float
);

CREATE TABLE IF NOT EXISTS radar_path_loss
(
    wg04_circulator: float
    wg02_harmonic_filter: float
    wg06_spectrum_filter: float
    ifd_rif_anti_alias_filter: float
    ifd_burst_anti_alias_filter: float
    a6_arc_detector: float
    transmitter_coupler_coupling: float
    vertical_f_heliax_to_4at16: float
    horizontal_f_heliax_to_4at17: float
    at4_attenuator: float
    waveguide_klystron_to_switch: float
);

CREATE TABLE IF NOT EXISTS radar_data_acquisition
(
    refreshed_at: str
    reporting_host: str
    mode: str
    status: str
    control_status: str
    operability_status: str
    super_resolution_status: str
    generator_state: str
    alarm_summary: str
    resolution_version: str
    nexrad_l2_path: str
    volume_coverage_pattern: str
    build_number: float
    average_tx_power_w: float
    reflectivity_calibration_correction_db: float
);

-- related to network_interfaces
CREATE TABLE IF NOT EXISTS radar_servers
(
    host: str
    server_type: str
    up_since: datetime
    hardware_refreshed_at: datetime
    network_interfaces_refreshed_at: datetime
    cpu: float
    memory: float
    io_utilization: float
    disk: int
    load_1: float
    load_5: float
    load_15: float
    command_last_executed: str
    command_last_executed_at: datetime
    command_last_nexrad_data_at: datetime
    command_last_received: str
    command_last_received_at: datetime
    command_last_refreshed_at: datetime
    ldm_refreshed_at: datetime
    ldm_latest_product_at: datetime
    ldm_oldest_product_at: datetime
    ldm_storage_size: int
    ldm_count: int
    is_ldm_active: bool
    is_server_active: bool
    is_server_primary: bool
    is_server_aggregate: bool
    is_server_locked: bool
    is_radar_network_up: bool
    collection_time: datetime
    reporting_host: str
    last_ping_at: datetime
);

CREATE TABLE IF NOT EXISTS rader_server_ping_responses
(
    ldm_name: str
    ldm_response: bool
    radar_name: str
    radar_response: bool
    server_name: str
    server_response: bool
    network_name: str
    network_response: bool
)

-- related to radar_servers
CREATE TABLE IF NOT EXISTS network_interfaces
(
    interface_name: str
    is_interface_active: bool
    packets_out_ok: int
    packets_out_error: int
    packets_out_dropped: int
    packets_out_overrun: int
    packets_in_ok: int
    packets_in_error: int
    packets_in_dropped: int
    packets_in_overrun: int
);

CREATE TABLE IF NOT EXISTS radar_queues
(
    host: str
    arrived_at: datetime
    created_at: datetime
    station_id: str
    queue_item_type: str
    feed: str
    resolution_version: int
    sequence_number: str
    size: int    
);

CREATE TABLE IF NOT EXISTS radar_station_alarms
(
    status: str
    message: str
    active_channel: int
    event_at: datetime
);


/****************
    STATIONS
*****************/


CREATE TABLE IF NOT EXISTS stations
(
    station_id: str
    name: str
    timezone: str
    lat: float
    lon: float
    elevation_m: float
    elevation_mi: float
    forecast_url: str
    county_url: str
    fire_weather_zone_url: str
);


/****************
    WEATHER
*****************/


-- related to observations_cloud_layers
CREATE TABLE IF NOT EXISTS observations
(
    observed_at: datetime
    icon_url: str
    text_description: str
    raw_message: str
    station_elevation_m: int
    station_elevation_mi: float
    temperature_c: float
    temperature_f: float
    dew_point_c: float
    dew_point_f: float
    wind_direction_deg_ang: int
    wind_direction_compass: str
    wind_speed_kmh: float
    wind_speed_mph: float
    wind_gust_kmh: float
    wind_gust_mph: float
    barometric_pressure_pa: int
    barometric_pressure_inhg: float
    sea_level_pressure_pa: int
    sea_level_pressure_inhg: float
    visibility_m: int
    visibility_mi: float
    max_temp_last_24h_c: float
    max_temp_last_24h_f: float
    min_temp_last_24h_c: float
    min_temp_last_24h_f: float
    precip_last_1h_mm: float
    precip_last_3h_mm: float
    precip_last_6h_mm: float
    relative_humidity_pc: float
    wind_chill_c: float
    wind_chill_f: float
    heat_index_c: float
    heat_index_f: float
);

-- related to observations
CREATE TABLE IF NOT EXISTS observations_cloud_layers
(
    cloud_layer_height: str
    cloud_layer_description: str
);

CREATE TABLE IF NOT EXISTS forecasts
(
    generated_at: datetime
    updated_at: datetime
    num: int
    name: str
    start_at: datetime
    end_at: datetime
    name: str
    forecast_short: str
    forecast_detailed: str
    forecast_icon_url: str
    is_daytime: bool
    wind_speed: str
    wind_direction: str
    temperature_trend: str
    temperature_c: float
    temperature_f: float
    dew_point_c: float
    dew_point_f: float
    relative_humidity_pc: float
    precipitation_probability_pc: float
);


/****************
    WEATHER
*****************/


-- related to:
-- - zone_county_warning_areas
-- - zone_observation_stations
-- - zone_forecast_offices
-- - zone_timezones
CREATE TABLE IF NOT EXISTS zones
(
    zone_id: str
    grid_id: str
    awips_id: str
    name: str
    zone_type: str
    state: str
    url: str
    effective_at: datetime
    expires_at: datetime
    -- add multi_polygon
);

-- related to zones
CREATE TABLE IF NOT EXISTS zone_county_warning_areas
(
    zone_id: str
    county_warning_area: str
);

-- related to zones
CREATE TABLE IF NOT EXISTS zone_observation_stations
(
    zone_id: str
    observation_station: str
);

-- related to zones
CREATE TABLE IF NOT EXISTS zone_forecast_offices
(
    zone_id: str
    forecast_office: str
);

-- related to zones
CREATE TABLE IF NOT EXISTS zone_timezones
(
    zone_id: str
    timezone: str
);

CREATE TABLE IF NOT EXISTS zone_forecast:
(
    forecasted_at: datetime
    num: int
    name: str
    forecast_detailed: str
);