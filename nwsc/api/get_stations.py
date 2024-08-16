from requests_cache import CachedSession
from nwsc.decorators import display_spinner
from nwsc.api.api_request import api_request
from nwsc.api import WMI_UNIT_MAP, API_URL_NWS_STATIONS


def format_station_data(feature: dict) -> dict:
	"""Format the station data returned from /gridpoints or /stations"""
	elevation_unit = WMI_UNIT_MAP.get(feature['properties']['elevation']['unitCode'])
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
		f'station_elevation_{elevation_unit}':  feature.get('properties').get('elevation', {})['value'],
	}


@display_spinner('Getting local stations...')
def get_local_stations_data(session: CachedSession, location: dict) -> list:
	stations_data = api_request(session, location['observation_stations_url'])
	local_stations = []
	for feature in stations_data['features']:
		local_stations.append(format_station_data(feature))
	return local_stations


@display_spinner('Getting station...')
def get_station_data(session: CachedSession, station_id: dict) -> dict:
	"""Get information about the given station ID"""
	station_data = api_request(session, API_URL_NWS_STATIONS + station_id)
	station = format_station_data(station_data)
	return station
