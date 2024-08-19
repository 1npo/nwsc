from requests_cache import CachedSession
from rich.pretty import pprint
from loguru import logger
from nwsc.render.decorators import display_spinner
from nwsc.api.conversions import convert_measures
from nwsc.api.api_request import api_request
from nwsc.api import (
    WMI_UNIT_MAP,
    API_URL_NWS_STATIONS,
	API_URL_NWS_GRIDPOINTS,
)


def process_station_data(feature: dict) -> dict:
	"""Format the station data returned from /gridpoints or /stations"""
	elevation_unit = WMI_UNIT_MAP.get(feature.get('properties', {}).get('elevation', {}).get('unitCode', {}))
	station_coords = feature.get('geometry').get('coordinates')
	if station_coords and isinstance(station_coords, list):
		station_lat = station_coords[0]
		station_lon = station_coords[1]
	else:
		station_lat = None
		station_lon = None
	return {
		'station_lat':                          station_lat,
		'station_lon':                          station_lon,
		'station_id':                           feature.get('properties').get('stationIdentifier', {}),
		'station_name':                         feature.get('properties').get('name', {}),
		'station_timezone':                     feature.get('properties').get('timeZone', {}),
		f'station_elevation_{elevation_unit}':  feature.get('properties').get('elevation', {}).get('value'),
	}


def get_stations(session: CachedSession, url: str) -> list:
	stations_data = api_request(session, url)
	stations = []
	for feature in stations_data.get('features', {}):
		station = process_station_data(feature)
		station = convert_measures(station)
		stations.append(station)
	return stations


@display_spinner('Getting stations usable in grid area...')
def get_stations_by_grid(session: CachedSession, forecast_office: str, gridpoints: dict) -> list:
	return get_stations(session, API_URL_NWS_GRIDPOINTS + f'/{forecast_office}/{gridpoints}/stations')


@display_spinner('Getting local stations...')
def get_stations_near_location(session: CachedSession, location: dict) -> list:
	return get_stations(session, location['observation_stations_url'])


@display_spinner('Getting station...')
def get_station(session: CachedSession, station_id: dict) -> dict:
	station_data = api_request(session, API_URL_NWS_STATIONS + station_id)
	station = process_station_data(station_data)
	station = convert_measures(station)
	return station
