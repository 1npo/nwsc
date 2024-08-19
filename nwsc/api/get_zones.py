from requests_cache import CachedSession
from rich.pretty import pprint
from loguru import logger
from nwsc.render.decorators import display_spinner
from nwsc.api.conversions import convert_measures
from nwsc.api.api_request import api_request, parse_timestamp
from nwsc.api.get_stations import process_station_data
from nwsc.api.get_weather import process_observations_data
from nwsc.api import (
    NWS_API_ZONES,
    NWS_API_ZONE_FORECASTS,
    VALID_NWS_ZONES,
)


def process_zone_data(zone_data: list) -> dict:
    zone_geometry = zone_data.get('geometry', {})
    if zone_geometry:
        zone_geometry = zone_geometry.get('coordinates')
    return {
        'zone_id':              zone_data.get('properties', {}).get('id'),
        'grid_id':              zone_data.get('properties', {}).get('gridIdentifier'),
        'awips_id':             zone_data.get('properties', {}).get('awipsLocationIdentifier'),
        'zone_type':            zone_data.get('properties', {}).get('type'),
        'zone_name':            zone_data.get('properties', {}).get('name'),
        'zone_url':             zone_data.get('properties', {}).get('@id'),
        'state':                zone_data.get('properties', {}).get('state'),
        'timezones':            zone_data.get('properties', {}).get('timeZone'),
        'county_warning_areas': zone_data.get('properties', {}).get('cwa'),
        'zone_effective_at':    parse_timestamp(zone_data.get('properties', {}).get('effectiveDate')),
        'zone_expires_at':      parse_timestamp(zone_data.get('properties', {}).get('expirationDate')),
        'forecast_offices':     zone_data.get('properties', {}).get('forecastOffices'),
        'observation_stations': zone_data.get('properties', {}).get('observationStations'),
        'multi_polygon':        zone_geometry,
    }


@display_spinner('Getting zone...')
def get_zone(session: CachedSession, zone_type: str, zone_id: str) -> dict:
    if zone_type not in VALID_NWS_ZONES:
        raise ValueError(f'Invalid zone type provided: {zone_type}. Valid zones are: {", ".join(VALID_NWS_ZONES)}')
    zone_data = api_request(session, NWS_API_ZONES + f'/{zone_type}/{zone_id}')
    return process_zone_data(zone_data)


@display_spinner('Getting all zones...')
def get_zones(session: CachedSession, zone_type: str = None) -> dict:
    if zone_type:
        zones_data = api_request(session, NWS_API_ZONES + f'/{zone_type}')
    else:
        zones_data = api_request(session, NWS_API_ZONES)
    zones = []
    for feature in zones_data.get('features', {}):
        zones.append(process_zone_data(feature))
    return zones


@display_spinner('Getting stations servicing zone...')
def get_zone_stations(session: CachedSession, zone_id: str) -> dict:
    zone_stations_data = api_request(session, NWS_API_ZONE_FORECASTS + f'{zone_id}/stations')
    zone_stations = []
    for feature in zone_stations_data.get('features', {}):
        zone_stations.append(process_station_data(feature))
    return zone_stations


@display_spinner('Getting observations for zone...')
def get_zone_observations(session: CachedSession, zone_id: str) -> dict:
    zone_observations_data = api_request(session, NWS_API_ZONE_FORECASTS + f'{zone_id}/observations')
    zone_observations = []
    for feature in zone_observations_data.get('features', {}):
        observation = process_observations_data(feature)
        observation = convert_measures(observation)
        zone_observations.append(observation)
    return zone_observations


@display_spinner('Getting forecast for zone...')
def get_zone_forecast(session: CachedSession, zone_id: str) -> dict:
    zone_forecast_data = api_request(session, NWS_API_ZONE_FORECASTS + f'{zone_id}/forecast')
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
