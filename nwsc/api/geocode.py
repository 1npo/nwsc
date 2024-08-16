from typing import Tuple
from requests_cache import CachedSession
from loguru import logger
from nwsc.api.api_request import api_request
from nwsc.api import API_URL_USCB_GEOCODE


# See: https://geocoding.geo.census.gov/geocoder/Geocoding_Services_API.html
def uscb_geocode(session: CachedSession, address: str) -> Tuple[float, float] | None:
	"""Get the lat and lon for a street address using the US Census Bureau's free geocoding API"""
	coord_data = api_request(session, API_URL_USCB_GEOCODE + address.replace(' ', '+'))
	try:
		coords = coord_data['result']['addressMatches'][0]['coordinates']
		lat = round(coords['y'], 2)
		lon = round(coords['x'], 2)
		logger.debug(f'Geocoded address {address} to {lat}, {lon}')
		return (lat, lon)
	except KeyError:
		return None
