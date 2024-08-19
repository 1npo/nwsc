
from typing import Tuple
from requests_cache import CachedSession
from loguru import logger
from nwsc.render.decorators import display_spinner
from nwsc.api.api_request import api_request
from nwsc.api import USCB_API_GEOCODE, NWS_API_POINTS


# See: https://geocoding.geo.census.gov/geocoder/Geocoding_Services_API.html
def uscb_geocode(session: CachedSession, address: str) -> Tuple[float, float] | None:
	"""Get the lat and lon for a street address using the US Census Bureau's free geocoding API"""
	coord_data = api_request(session, USCB_API_GEOCODE + address.replace(' ', '+'))
	try:
		coords = coord_data['result']['addressMatches'][0]['coordinates']
		lat = round(coords['y'], 2)
		lon = round(coords['x'], 2)
		logger.debug(f'Geocoded address {address} to {lat}, {lon}')
		return (lat, lon)
	except KeyError:
		return None


@display_spinner('Getting location data...')
def get_points_for_location(session: CachedSession, address: str) -> dict:
	coords = uscb_geocode(session, address)
	coords_str = f'{coords[0]},{coords[1]}'
	location_data = api_request(session, NWS_API_POINTS + coords_str)
	location = {
		'city':                     location_data.get('properties', {}).get('relativeLocation', {}).get('properties', {}).get('city'),
		'state':                    location_data.get('properties', {}).get('relativeLocation', {}).get('properties', {}).get('state'),
		'timezone':                 location_data.get('properties', {}).get('timeZone'),
		'grid_x':                   location_data.get('properties', {}).get('gridX'),
		'grid_y':                   location_data.get('properties', {}).get('gridY'),
		'county_warning_area':      location_data.get('properties', {}).get('cwa'),
		'forecast_office_url':      location_data.get('properties', {}).get('forecastOffice'),
		'radar_station':            location_data.get('properties', {}).get('radarStation'),
		'forecast_extended_url':    location_data.get('properties', {}).get('forecast'),				# /gridpoints/{wfo}/{x},{y}/forecast
		'forecast_hourly_url':      location_data.get('properties', {}).get('forecastHourly'),			# /gridpoints/{wfo}/{x},{y}/forecast/hourly
		'gridpoints_url':           location_data.get('properties', {}).get('forecastGridData'),		# /gridpoints/{wfo}/{x},{y}
		'observation_stations_url': location_data.get('properties', {}).get('observationStations'),		# /gridpoints/{wfo}/{x},{y}/stations
	}
	return location
