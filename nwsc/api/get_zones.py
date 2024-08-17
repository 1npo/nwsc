from requests_cache import CachedSession
from loguru import logger
from nwsc.render.decorators import display_spinner
from nwsc.api.api_request import api_request, parse_timestamp
from nwsc.api.get_stations import process_station_data
from nwsc.api.get_weather import process_observations_data
from nwsc.api import (
    API_URL_NWS_ZONES,
    API_URL_NWS_ZONE_FORECASTS,
    VALID_NWS_ZONES,
)


"""
- [ ] get_all_zones
- [ ] get_zones_by_type
- [ ] get_zone
- [x] get_zone_forecast
- [x] get_zone_observations
- [x] get_zone_stations
"""


@display_spinner('Getting zones by type...')
def get_zones_by_type(session: CachedSession, zone_type: str) -> dict:
    pass


@display_spinner('Getting stations servicing zone...')
def get_zone_stations(session: CachedSession, zone_id: str) -> dict:
    """ """
    zone_stations_data = api_request(session, API_URL_NWS_ZONE_FORECASTS + f'/{zone_id}/stations')
    zone_stations = []
    for feature in zone_stations_data.get('features', {}):
        zone_stations.append(process_station_data(feature))
    return zone_stations


@display_spinner('Getting observations for zone...')
def get_zone_observations(session: CachedSession, zone_id: str) -> dict:
    """ """
    zone_observations_data = api_request(session, API_URL_NWS_ZONE_FORECASTS + f'/{zone_id}/observations')
    return process_observations_data(zone_observations_data)


@display_spinner('Getting forecast for zone...')
def get_zone_forecast(session: CachedSession, zone_id: str) -> dict:
    """ """
    zone_forecast_data = api_request(session, API_URL_NWS_ZONE_FORECASTS + f'/{zone_id}/forecast')
    forecast = {'forecasted_at': parse_timestamp(zone_forecast_data.get('properties', {}).get('updated'))}
    period_forecasts = []
    for period in zone_forecast_data.get('properties', {}).get('periods', {}):
        if period and isinstance(period, dict):
            period_forecasts.append({
                'period_num':               period.get('number'),
                'period_name':              period.get('name'),
                'period_forecast_detailed': period.get('detailedForecast'),
            })
    forecast['period_forecasts'] = period_forecasts
    return forecast
