"""Get any needed data from the NWS API endpoints, clean it, and standardize it
"""

import os
import json
from pathlib import Path
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
from nwsc.api.get_zones import *
from nwsc.api.get_enums import *


def get_raw_nws_data(session: CachedSession, address: str) -> dict:
	"""Get sample weather data for testing
	"""
	
	# weather
	location_data = get_location(session, address)

	# stations
	local_stations_data = get_local_stations(session, location_data)
	nearest_station = local_stations_data[1]['station_id']

	# weather
	observations = get_station_observations(session, nearest_station)
	forecast_extended = get_extended_forecast(session, location_data)
	forecast_hourly = get_hourly_forecast(session, location_data)

	# alerts
	alerts = get_alerts_by_area(session, location_data['state'])
	alert_counts = get_alert_counts(session)

	# radar
	radar_servers = get_radar_servers(session)
	radar_stations = get_radar_stations(session)
	radar_station_alarms = get_radar_station_alarms(session, 'KHPX')

	# products
	product_types = get_product_types(session)
	product_types_by_location = get_product_types_by_location(session, 'BGM')
	product_locations = get_product_locations(session)
	product_locations_by_type = get_product_locations_by_type(session, 'AWO')
	products = get_products(session)
	products_by_type = get_products_by_type(session, 'RR2')
	products_by_type_and_location = get_products_by_type_and_location(session, 'ADA', 'SRH')
	product = get_product(session, '5359e496-498b-40b9-bae6-0f0dcddc87a2')

	# zones
	zone = get_zone(session, 'county', 'AKC013')
	zones = get_zones(session, 'coastal')
	zone_stations = get_zone_stations(session, 'NJC003')
	zone_observations = get_zone_observations(session, 'TNZ061')
	zone_forecast = get_zone_forecast(session, 'TXZ120')

	# enums
	valid_zones = get_valid_zones(session)
	valid_forecast_offices = get_valid_forecast_offices(session)

	weather_data = {
		'location_data':					location_data,
		'local_stations_data':				local_stations_data,
		'nearest_station':					nearest_station,
		'observations':						observations,
		'forecast_extended':				forecast_extended,
		'forecast_hourly':					forecast_hourly,
		'alerts':							alerts,
		'alert_counts':						alert_counts,
		'radar_servers':					radar_servers,
		'radar_stations':					radar_stations,
		'radar_station_alarms':				radar_station_alarms,
		'product_types':					product_types,
		'product_types_by_location':		product_types_by_location,
		'product_locations':				product_locations,
		'product_locations_by_type':		product_locations_by_type,
		'products':							products,
		'products_by_type':					products_by_type,
		'products_by_type_and_location':	products_by_type_and_location,
		'product':							product,
		'zone':								zone,
		'zones':							zones,
		'zone_stations':					zone_stations,
		'zone_observations':				zone_observations,
		'zone_forecast':					zone_forecast,
		'valid_zones':						valid_zones,
		'valid_forecast_offices':			valid_forecast_offices,
	}

	return weather_data


def nws_data_to_json(session: CachedSession, address: str):
	nws_data = get_raw_nws_data(session, address)
	output_path = Path(os.path.expanduser('~')) / 'nws_data'
	Path(output_path).mkdir(parents=True, exist_ok=True)
	for name, data in nws_data.items():
		output_file = output_path / f'nws_raw_{name}.json'
		with open(output_file, 'w') as f:
			f.write(json.dumps(data, default=str, indent=4))
		logger.success(f'Wrote {name} to {output_file}')


def pprint_raw_nws_data(session: CachedSession, address: str):
	nws_data = get_raw_nws_data(session, address)
	console = Console()
	for name, data in nws_data.items():
		if name in ('valid_zones', 'valid_forecast_offices'):
			console.print(f'{name}\n{"=" * len(name)}', style='bold red')
			pprint(data)


