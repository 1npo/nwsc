"""Get any needed data from the NWS API endpoints, clean it, and standardize it
"""

from rich.console import Console
from rich.pretty import pprint
from requests_cache import CachedSession
from loguru import logger
from nwsc.render.decorators import display_spinner
from nwsc.api.get_weather import *
from nwsc.api.get_stations import *
from nwsc.api.get_radar import *
from nwsc.api.get_products import *
from nwsc.api.get_offices import *
from nwsc.api.get_glossary import *
from nwsc.api.get_alerts import *


def pprint_raw_data_weather(weather_data: dict):
	console = Console()
	for name, data in weather_data.items():
		console.print(f'{name}\n{"=" * len(name)}', style='bold red')
		pprint(data)


def get_weather_for_location(session: CachedSession, address: str) -> dict:
	"""Get sample weather data for testing
	"""
	
	# weather
	location_data = get_location_data(session, address)

	# stations
	local_stations_data = get_local_stations_data(session, location_data)
	nearest_station = local_stations_data[1]['station_id']

	# weather
	observations = get_station_observations_data(session, nearest_station)
	forecast_extended = get_extended_forecast_data(session, location_data)
	forecast_hourly = get_hourly_forecast_data(session, location_data)

	# alerts
	alerts = get_alerts_data_by_area(session, location_data['state'])
	alert_counts = get_alert_counts_data(session)

	# radar
	servers = get_radar_server_data(session)
	radar_stations = get_radar_station_data(session)
	radar_station_alarms = get_radar_station_alarm_data(session, 'KHPX')

	# products
	product_types1 = get_product_types(session)
	product_types2 = get_product_types_by_location(session, 'BGM')
	product_locations1 = get_product_locations(session)
	product_locations2 = get_product_locations_by_type(session, 'AWO')
	product_listing1 = get_product_listing(session)
	product_listing2 = get_product_listing_by_type(session, 'RR2')
	product_listing3 = get_product_listing_by_type_and_location(session, 'ADA', 'SRH')
	product_data = get_product(session, '5359e496-498b-40b9-bae6-0f0dcddc87a2')

	'''
	- [x] process_product_listing_data
	- [x] process_product_locations_data
	- [x] process_product_types_data
	- [x] get_product_listing
	- [x] get_product_listing_by_type
	- [x] get_product_listing_by_type_and_location
	- [x] get_product_types
	- [x] get_product_types_by_location
	- [x] get_product_locations
	- [x] get_product_locations_by_type
	- [x] get_product
	'''


	weather_data = {
		'location_data':		location_data,
		'local_stations_data':	local_stations_data,
		'nearest_station':		nearest_station,
		'observations':			observations,
		'forecast_extended':	forecast_extended,
		'forecast_hourly':		forecast_hourly,
		'servers':				servers,
		'alerts':				alerts,
		'alert_counts':			alert_counts,
		'radar_stations':		radar_stations,
		'radar_station_alarms':	radar_station_alarms,
		'product_types1':		product_types1,
		'product_types2':		product_types2,
		'product_locations1':	product_locations1,
		'product_locations2':	product_locations2,
		'product_listing1':		product_listing1,
		'product_listing2':		product_listing2,
		'product_listing3':		product_listing3,
		'product_data':			product_data,
	}

	pprint_raw_data_weather(weather_data)

# get_radar_server_data()
# get_radar_station_data()
# get_glossary_data()
# get_station_observations_data()