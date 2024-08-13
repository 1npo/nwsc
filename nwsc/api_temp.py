"""Get any needed data from the NWS API endpoints, clean it, and standardize it
"""

import pytz
from rich.console import Console
from rich.pretty import pprint
from typing import Tuple
from datetime import datetime
from requests_cache import CachedSession
from loguru import logger
from nwsc.decorators import display_spinner


# See:
# - https://github.com/weather-gov/api/discussions/478
# - https://weather-gov.github.io/api/general-faqs, especially these sections:
#   - "How do I get a forecast for a location from the API?"
#   - "How do I know I'm getting the latest data? Do I need to use “cache busting” methods?"
API_URL_USCB_GEOCODE = 'https://geocoding.geo.census.gov/geocoder/locations/onelineaddress?benchmark=Public_AR_Current&format=json&address='
API_URL_NWS_POINTS = 'https://api.weather.gov/points/'
API_URL_NWS_STATIONS = 'https://api.weather.gov/stations/'
API_URL_NWS_ALERTS = 'http://api.weather.gov/alerts/'
API_URL_NWS_ALERTS_AREA = 'http://api.weather.gov/alerts/active/area/'
API_URL_NWS_ALERTS_REGION = 'http://api.weather.gov/alerts/active/region/'
API_URL_NWS_ALERTS_ZONE = 'http://api.weather.gov/alerts/active/zone/'
API_URL_NWS_ALERT_TYPES = 'http://api.weather.gov/alerts/types'
API_URL_NWS_ALERT_COUNTS = 'http://api.weather.gov/alerts/active/count'
API_URL_NWS_GLOSSARY = 'https://api.weather.gov/glossary'
API_URL_NWS_SERVERS = 'http://api.weather.gov/radar/servers'
API_URL_NWS_RADAR_STATIONS = 'http://api.weather.gov/radar/stations'

# See: https://codes.wmo.int/common/unit
WMI_UNIT_MAP = {                            
	'wmoUnit:Pa':               'pa',       # pressure in pascals
	'wmoUnit:km_h-1':           'kmph',     # kilometers per hour
	'wmoUnit:m':                'm',        # meters
	'wmoUnit:percent':          'pc',       # percent
	'wmoUnit:mm':               'mm',       # milimeters
	'wmoUnit:degree_(angle)':   'deg_ang',  # degrees (angle)
	'wmoUnit:degC':             'c',        # degrees celsius
	'wmoUnit:W':				'w',		# watts
	'wmoUnit:dB':				'db',		# decibels
	'F':                        'f',        # degrees fahrenheit
	'nwsUnit:s':				's',		# seconds

}

# See:
# - https://www.atmos.albany.edu/facstaff/ralazear/ATM209/Home_files/METAR_Code.pdf
# - https://en.wikipedia.org/wiki/Okta
METAR_CLOUD_COVER_MAP = {
	'SKC':  'Clear Sky',
	'CLR':  'Clear Sky',
	'FEW':  'Few Clouds',           # 1-2 oktas (1/8 - 2/8 of sky covered)
	'SCT':  'Scattered Clouds',     # 3-4 oktas (3/8 - 4/8 of sky covered)
	'BKN':  'Broken Sky',           # 4-7 oktas (5/8 - 7/8 of sky covered)
	'OVC':  'Overcast',             # 8 oktas (sky completely covered)
}


def convert_temperatures(data: dict) -> dict:
	"""Ensure that temperatures are represented in both metric and imperial"""
	new_data = {}
	for field, value in data.items():
		new_data[field] = value
		if field[-2:] == '_c':
			field_f = f'{field[:-2]}_f'
			if field_f not in data:
				new_data[field_f] = None
				if value:
					new_data[field_f] = (value * 9/5) + 32
		if field[-2:] == '_f':
			field_c = f'{field[:-2]}_c'
			if field_c not in data:
				new_data[field_c] = None
				if value:
					new_data[field_c] = (value - 32) * 5/9
	return new_data


def convert_speeds(data: dict) -> dict:
	"""Ensure that speeds are represented in both metric and imperial"""
	new_data = {}
	for field, value in data.items():
		new_data[field] = value
		if field[-5:] == '_kmph':
			field_mph = f'{field[:-5]}_mph'
			if field_mph not in data:
				new_data[field_mph] = None
				if value:
					new_data[field_mph] = value / 1.609344
		if field[-4:] == '_mph':
			field_kmph = f'{field[:-4]}_kmph'
			if field_kmph not in data:
				new_data[field_kmph] = None
				if value:
					new_data[field_kmph] = value * 1.609344
	return new_data


def convert_distances(data: dict) -> dict:
	"""Ensure that distances are represented in both metric and imperial"""
	new_data = {}
	for field, value in data.items():
		new_data[field] = value
		if field[-2:] == '_m':
			field_miles = f'{field[:-2]}_mi'
			if field_miles not in data:
				new_data[field_miles] = None
				if value:
					new_data[field_miles] = value / 1609.344
		if field[-3:] == '_mi':
			field_meters = f'{field[:-3]}_m'
			if field_meters not in data:
				new_data[field_miles] = None
				if value:
					new_data[field_meters] = value * 1609.344
	return new_data


def convert_pressures(data: dict) -> dict:
	"""Ensure that pressures are represented in both metric and imperial"""
	new_data = {}
	for field, value in data.items():
		new_data[field] = value
		if field[-3:] == '_pa':
			field_inhg = f'{field[:-3]}_inhg'
			if field_inhg not in data:
				new_data[field_inhg] = None
				if value:
					new_data[field_inhg] = value / 3386.39
		if field[-5:] == '_inhg':
			field_pa = f'{field[:-5]}_pa'
			if field_pa not in data:
				if value:
					new_data[field_pa] = value * 3386.39
	return new_data


# See: http://tamivox.org/dave/compass/
def convert_directions(data: dict) -> dict:
	"""Add wind direction string on a 16-point compass"""
	if data.get('wind_direction_deg_ang'):
		if (0 <= data['wind_direction_deg_ang'] <= 22.4) or data['wind_direction_deg_ang'] == 360:
			data['wind_direction_compass'] = 'N'
		elif 22.5 <= data['wind_direction_deg_ang'] <= 44.9:
			data['wind_direction_compass'] = 'NNE'
		elif 45 <= data['wind_direction_deg_ang'] <= 67.4:
			data['wind_direction_compass'] = 'NE'
		elif 67.5 <= data['wind_direction_deg_ang'] <= 89.9:
			data['wind_direction_compass'] = 'ENE'
		elif 90 <= data['wind_direction_deg_ang'] <= 112.4:
			data['wind_direction_compass'] = 'E'
		elif 112.5 <= data['wind_direction_deg_ang'] <= 134.9:
			data['wind_direction_compass'] = 'ESE'
		elif 135 <= data['wind_direction_deg_ang'] <= 157.4:
			data['wind_direction_compass'] = 'SE'
		elif 157.5 <= data['wind_direction_deg_ang'] <= 179.9:
			data['wind_direction_compass'] = 'SSE'
		elif 180 <= data['wind_direction_deg_ang'] <= 202.4:
			data['wind_direction_compass'] = 'S'
		elif 202.5 <= data['wind_direction_deg_ang'] <= 224.9:
			data['wind_direction_compass'] = 'SSW'
		elif 225 <= data['wind_direction_deg_ang'] <= 247.4:
			data['wind_direction_compass'] = 'SW'
		elif 247.5 <= data['wind_direction_deg_ang'] <= 269.9:
			data['wind_direction_compass'] = 'WSW'
		elif 270 <= data['wind_direction_deg_ang'] <= 292.4:
			data['wind_direction_compass'] = 'W'
		elif 292.5 <= data['wind_direction_deg_ang'] <= 314.9:
			data['wind_direction_compass'] = 'WNW'
		elif 315 <= data['wind_direction_deg_ang'] <= 337.4:
			data['wind_direction_compass'] = 'NW'
		elif 337.5 <= data['wind_direction_deg_ang'] <= 359.9:
			data['wind_direction_compass'] = 'NNW'
	return data


def round_floats(data: dict) -> dict:
	for k, v in data.items():
		if isinstance(v, float):
			data[k] = round(v, 2)
	return data


def convert_measures(data: dict) -> dict:
	data = convert_temperatures(data)
	data = convert_speeds(data)
	data = convert_distances(data)
	data = convert_pressures(data)
	data = convert_directions(data)
	data = round_floats(data)
	return data


def api_request(session: CachedSession, url: str) -> dict:
	return session.get(url).json()


def parse_timestamp(timestamp: str) -> datetime | None:
	if timestamp:
		return datetime.fromisoformat(timestamp).astimezone(pytz.timezone('US/Eastern')).replace(tzinfo=None)


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


@display_spinner('Getting location data...')
def get_location_data(session: CachedSession, address: str) -> dict:
	"""Get weather station data for the given address"""
	coords = uscb_geocode(session, address)
	coords_str = f'{coords[0]},{coords[1]}'
	location_data = api_request(session, API_URL_NWS_POINTS + coords_str)
	location = {
		'city':                     location_data.get('properties', {}).get('relativeLocation', {}).get('properties', {}).get('city'),
		'state':                    location_data.get('properties', {}).get('relativeLocation', {}).get('properties', {}).get('state'),
		'timezone':                 location_data.get('properties', {}).get('timeZone'),
		'grid_x':                   location_data.get('properties', {}).get('gridX'),
		'grid_y':                   location_data.get('properties', {}).get('gridY'),
		'forecast_office':          location_data.get('properties', {}).get('cwa'),
		'forecast_office_url':      location_data.get('properties', {}).get('forecastOffice'),
		'radar_station':            location_data.get('properties', {}).get('radarStation'),
		'forecast_extended_url':    location_data.get('properties', {}).get('forecast'),
		'forecast_hourly_url':      location_data.get('properties', {}).get('forecastHourly'),
		'gridpoints_url':           location_data.get('properties', {}).get('forecastGridData'),
		'observation_stations_url': location_data.get('properties', {}).get('observationStations'),
	}
	return location


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


@display_spinner('Getting station observations...')
def get_station_observations_data(session: CachedSession, station_id: str) -> dict:
	"""Get the current observations for the given station"""
	observations_data = api_request(session, API_URL_NWS_STATIONS + station_id + '/observations/latest')
	observation_type_names = {
		'elevation':                    'station_elevation',
		'temperature':                  'temperature',
		'dewpoint':                     'dew_point',
		'windDirection':                'wind_direction',    
		'windSpeed':                    'wind_speed',
		'windGust':                     'wind_gust',
		'barometricPressure':           'barometric_pressure',
		'seaLevelPressure':             'sea_level_pressure',
		'visibility':                   'visibility',
		'maxTemperatureLast24Hours':    'max_temp_last_24h',
		'minTemperatureLast24Hours':    'min_temp_last_24h',
		'precipitationLastHour':        'precip_last_1h',
		'precipitationLast3Hours':      'precip_last_3h',
		'precipitationLast6Hours':      'precip_last_6h',
		'relativeHumidity':             'relative_humidity',
		'windChill':                    'wind_chill',
		'heatIndex':                    'heat_index',
		'cloudLayers':                  'cloud_layers',
	}
	observations = {
		'observed_at':      parse_timestamp(observations_data['properties']['timestamp']),
		'icon_url':         observations_data['properties']['icon'],
		'text_description': observations_data['properties']['textDescription'],
	}
	for api_name, new_name in observation_type_names.items():
		if api_name == 'cloudLayers':
			cloud_layers = {}
			for layer in observations_data['properties'][api_name]:
				layer_amount = METAR_CLOUD_COVER_MAP.get(layer['amount'])
				layer_unit = WMI_UNIT_MAP[layer['base']['unitCode']]
				layer_height = layer['base']['value']
				if layer_height:
					layer_name = f'{layer_height}{layer_unit}'
				else:
					layer_name = 'None'
				cloud_layers.update({layer_name: layer_amount})
			observations[new_name] = cloud_layers
		else:
			observation_unit = WMI_UNIT_MAP[observations_data['properties'][api_name]['unitCode']]
			observations[f'{new_name}_{observation_unit}'] = observations_data['properties'][api_name]['value']
	observations = convert_measures(observations)
	return observations


def get_forecast_data(session: CachedSession, forecast_url: str) -> dict:
	"""Get the forecast for the given location"""
	forecast_data = api_request(session, forecast_url)
	len_periods = len(forecast_data['properties']['periods'])
	forecast = {}
	for i in range(0, len_periods):
		period = forecast_data['properties']['periods'][i]
		if not period:
			continue
		temp_unit = WMI_UNIT_MAP.get(period.get('temperatureUnit'))
		humidity_unit = WMI_UNIT_MAP.get(period.get('relativeHumidity', {}).get('unitCode'))
		precip_unit = WMI_UNIT_MAP.get(period.get('probabilityOfPrecipitation', {}).get('unitCode'))
		dew_point_unit = WMI_UNIT_MAP.get(period.get('dewpoint', {}).get('unitCode'))
		period_forecast = {
			'forecast_generated_at':        parse_timestamp(forecast_data.get('properties', {}).get('generatedAt')),
			'forecast_updated_at':          parse_timestamp(forecast_data.get('properties', {}).get('updateTime')),
			'period_start_at':              parse_timestamp(period.get('startTime')),
			'period_end_at':                parse_timestamp(period.get('endTime')),
			'period_name':                  period.get('name'),
			'period_forecast_short':        period.get('shortForecast'),
			'period_forecast_detailed':     period.get('detailedForecast'),
			'period_forecast_icon_url':     period.get('icon'),
			'is_daytime':                   period.get('isDaytime'),
			'wind_speed':                   period.get('windSpeed'),
			'wind_direction':               period.get('windDirection'),
			'temperature_trend':            period.get('temperatureTrend'),
			f'temperature_{temp_unit}':		period.get('temperature'),
			f'dew_point_{dew_point_unit}':	period.get('dewpoint', {}).get('value'),
			f'humidity_{humidity_unit}':	period.get('relativeHumidity', {}).get('value'),
			f'precipitation_{precip_unit}':	period.get('probabilityOfPrecipitation', {}).get('value'),
		}
		period_forecast = convert_measures(period_forecast)
		forecast.update({period['number']: period_forecast})
	return forecast


@display_spinner('Getting extended forecast...')
def get_extended_forecast_data(session: CachedSession, location: dict) -> dict:
	return get_forecast_data(session, location['forecast_extended_url'])


@display_spinner('Getting hourly forecast...')
def get_hourly_forecast_data(session: CachedSession, location: dict) -> dict:
	return get_forecast_data(session, location['forecast_hourly_url'])


# See:
# - https://vlab.noaa.gov/web/nws-common-alerting-protocol
# - https://www.weather.gov/media/alert/CAP_v12_guide_05-16-2017.pdf
# - https://www.weather.gov/vtec/
def process_alert_data(alert_data: dict) -> list:
	"""Get all current alerts for the given area, zone, or region"""
	alerts = []
	for feature in alert_data['features']:
		alert = {
			'alert_title':                  alert_data.get('title'),
			'alert_updated_at':             parse_timestamp(alert_data.get('updated')),
			'alert_url':                    feature.get('id'),
			'alert_id':                     feature.get('properties', {}).get('id'),
			'alert_area_desc':              feature.get('properties', {}).get('areaDesc'),
			'alert_area_urls':              feature.get('properties', {}).get('affectedZones'),
			'alert_areas_ugc':              feature.get('properties', {}).get('geocode', {}).get('UGC'),
			'alert_areas_same':             feature.get('properties', {}).get('geocode', {}).get('SAME'),
			'alert_sent_by':                feature.get('properties', {}).get('sender'),
			'alert_sent_by_name':           feature.get('properties', {}).get('senderName'),
			'alert_sent_at':                parse_timestamp(feature.get('properties', {}).get('sent')),
			'alert_effective_at':           parse_timestamp(feature.get('properties', {}).get('effective')),
			'alert_ends_at':                parse_timestamp(feature.get('properties', {}).get('ends')),
			'alert_status':                 feature.get('properties', {}).get('status'),
			'alert_message_type':           feature.get('properties', {}).get('messageType'),
			'alert_category':               feature.get('properties', {}).get('category'),
			'alert_certainty':              feature.get('properties', {}).get('certainty'),
			'alert_urgency':                feature.get('properties', {}).get('urgency'),
			'alert_event_type':             feature.get('properties', {}).get('event'),
			'alert_onset_at':               parse_timestamp(feature.get('properties', {}).get('onset')),
			'alert_expires_at':             parse_timestamp(feature.get('properties', {}).get('expires')),
			'alert_headline':               feature.get('properties', {}).get('headline'),
			'alert_description':            feature.get('properties', {}).get('description'),
			'alert_instruction':            feature.get('properties', {}).get('instruction'),
			'alert_response_type':          feature.get('properties', {}).get('response'),
			'alert_cap_awips_id':           feature.get('properties', {}).get('parameters', {}).get('AWIPSidentifier'),
			'alert_cap_wmo_id':             feature.get('properties', {}).get('parameters', {}).get('WMOidentifier'),
			'alert_cap_headline':           feature.get('properties', {}).get('parameters', {}).get('NWSheadline'),
			'alert_cap_blocked_channels':   feature.get('properties', {}).get('parameters', {}).get('BLOCKCHANNEL'),
			'alert_cap_vtec':               feature.get('properties', {}).get('parameters', {}).get('VTEC'),
			'prior_alerts':                 [],
		}
		for reference in feature.get('properties', {}).get('references'):
			prior_alert = {
				'prior_alert_url':          reference.get('@id'),
				'prior_alert_id':           reference.get('identifier'),
				'prior_alert_sent_at':      parse_timestamp(reference.get('sent')),
			}
			alert['prior_alerts'].append(prior_alert)
		alerts.append(alert)
	return alerts


@display_spinner('Getting alerts for the local area...')
def get_alerts_data_by_area(session: CachedSession, area: str) -> dict:
	alert_data = api_request(session, API_URL_NWS_ALERTS_AREA + area)
	return process_alert_data(alert_data)


@display_spinner('Getting alerts for zone...')
def get_alerts_data_by_zone(session: CachedSession, zone: str) -> dict:
	alert_data = api_request(session, API_URL_NWS_ALERTS_ZONE + zone)
	return process_alert_data(alert_data)


@display_spinner('Getting alerts for marine region...')
def get_alerts_data_by_region(session: CachedSession, region: str) -> dict:
	alert_data = api_request(session, API_URL_NWS_ALERTS_REGION + region)
	return process_alert_data(alert_data)


@display_spinner('Getting alerts for marine region...')
def get_alerts_data_by_id(session: CachedSession, alert_id: str) -> dict:
	alert_data = api_request(session, API_URL_NWS_ALERTS + alert_id)
	return process_alert_data({'features': [alert_data]})


@display_spinner('Getting alert types...')
def get_alert_types_data(session: CachedSession) -> list:
	alert_types_data = api_request(session, API_URL_NWS_ALERT_TYPES)
	return alert_types_data.get('eventTypes')


@display_spinner('Getting alert counts...')
def get_alert_counts_data(session: CachedSession) -> list:
	return api_request(session, API_URL_NWS_ALERT_COUNTS)


@display_spinner('Getting glossary...')
def get_glossary_data(session: CachedSession) -> dict:
	"""Get the glossary of weather terms"""
	glossary_data = api_request(session, API_URL_NWS_GLOSSARY)
	glossary = {}
	for entry in glossary_data['glossary']:
		term = entry.get('term')
		definition = entry.get('definition')
		if term and definition:
			glossary.update({term: definition})
	return glossary


# See:
# - https://www.ncdc.noaa.gov/wct/data.php
# -
#
# LDM = Local Data Manager
# RDS = Remote Data Server
# TDS = THREDDs Data Server
#
# NOTE: The official API documentation doesn't include a schema for the radar
# servers and stations endpoints. Some field meanings are inferred from the data.
@display_spinner('Getting radar server metadata...')
def get_radar_server_data(session: CachedSession) -> dict:
	""" """
	radar_server_data = api_request(session, API_URL_NWS_SERVERS)
	servers = []
	for feature in radar_server_data['@graph']:
		server = {
			'server_host':                  feature.get('id'),
			'server_type':                  feature.get('type'),
			'server_up_since':              parse_timestamp(feature.get('hardware', {}).get('uptime')),
			'server_hardware_refresh_at':   parse_timestamp(feature.get('hardware', {}).get('timestamp')),
			'server_cpu':                   feature.get('hardware', {}).get('cpuIdle'),
			'server_memory':                feature.get('hardware', {}).get('memory'),
			'server_io_utilization':        feature.get('hardware', {}).get('ioUtilization'),
			'server_disk':                  feature.get('hardware', {}).get('disk'),
			'server_load_1':                feature.get('hardware', {}).get('load1'),
			'server_load_5':                feature.get('hardware', {}).get('load5'),
			'server_load_15':               feature.get('hardware', {}).get('load15'),
			'command_last_executed':        feature.get('command', {}).get('lastExecuted'),
			'command_last_executed_at':     parse_timestamp(feature.get('command', {}).get('lastExecutedTime')),
			'command_last_nexrad_data_at':  parse_timestamp(feature.get('command', {}).get('lastNexradDataTime')),
			'command_last_received':        feature.get('command', {}).get('lastReceived'),
			'command_last_received_at':     parse_timestamp(feature.get('command', {}).get('lastReceivedTime')),
			'command_last_refresh_at':      parse_timestamp(feature.get('command', {}).get('timestamp')),
			'ldm_refresh_at':               parse_timestamp(feature.get('ldm', {}).get('timestamp')),
			'ldm_latest_product_at':        parse_timestamp(feature.get('ldm', {}).get('latestProduct')),
			'ldm_oldest_product_at':        parse_timestamp(feature.get('ldm', {}).get('oldestProduct')),
			'ldm_storage_size':             feature.get('ldm', {}).get('storageSize'),
			'ldm_count':                    feature.get('ldm', {}).get('count'),
			'is_ldm_active':                feature.get('ldm', {}).get('active'),
			'is_server_active':             feature.get('active'),
			'is_server_primary':            feature.get('primary'),
			'is_server_aggregate':          feature.get('aggregate'),
			'is_server_locked':             feature.get('locked'),
			'is_radar_network_up':          feature.get('radarNetworkUp'),
			'collection_time':              parse_timestamp(feature.get('collectionTime')),
			'reporting_host':               feature.get('reportingHost'),
			'last_ping_at':                 parse_timestamp(feature.get('ping', {}).get('timestamp')),
			'ping_responses_ldm':           feature.get('ping', {}).get('targets', {}).get('ldm'),
			'ping_responses_radar':         feature.get('ping', {}).get('targets', {}).get('radar'),
			'ping_responses_server':        feature.get('ping', {}).get('targets', {}).get('server'),
			'ping_responses_misc':          feature.get('ping', {}).get('targets', {}).get('misc'),
			'interface_refresh_at':         parse_timestamp(feature.get('network', {}).get('timestamp')),
			'interfaces':                   [],
		}
		for item in feature['network']:
			if item != 'timestamp':
				interface = {
					'interface_name':       feature.get('network', {}).get(item, {}).get('interface'),
					'is_interface_active':  feature.get('network', {}).get(item, {}).get('active'),
					'packets_out_ok':       feature.get('network', {}).get(item, {}).get('transNoError'),
					'packets_out_error':    feature.get('network', {}).get(item, {}).get('transError'),
					'packets_out_dropped':  feature.get('network', {}).get(item, {}).get('transDropped'),
					'packets_out_overrun':  feature.get('network', {}).get(item, {}).get('transOverrun'),
					'packets_in_ok':        feature.get('network', {}).get(item, {}).get('recvNoError'),
					'packets_in_error':     feature.get('network', {}).get(item, {}).get('recvError'),
					'packets_in_dropped':   feature.get('network', {}).get(item, {}).get('recvDropped'),
					'packets_in_overrun':   feature.get('network', {}).get(item, {}).get('recvOverrun'),
				}
				server['interfaces'].append(interface)
		servers.append(server)
	return servers


@display_spinner('Getting radar station metadata...')
def get_radar_station_data(session: CachedSession) -> dict:
	""" """
	radar_station_data = api_request(session, API_URL_NWS_RADAR_STATIONS)
	stations = []
	for feature in radar_station_data.get('features', {}):
		station_coords = feature.get('geometry', {}).get('coordinates')
		if station_coords and isinstance(station_coords, list):
			station_lat = station_coords[0]
			station_lon = station_coords[1]
		rda = feature.get('properties', {}).get('rda', {})
		if rda is None:
			rda = {}
		elevation_unit = WMI_UNIT_MAP.get(feature.get('properties', {}).get('elevation', {}).get('unitCode'))
		latency_current_unit = WMI_UNIT_MAP.get(feature.get('latency', {}).get('current', {}).get('unitCode'))
		latency_average_unit = WMI_UNIT_MAP.get(feature.get('latency', {}).get('current', {}).get('unitCode'))
		latency_max_unit = WMI_UNIT_MAP.get(feature.get('latency', {}).get('current', {}).get('unitCode'))
		tx_power_unit = WMI_UNIT_MAP.get(rda.get('properties', {}).get('averageTransmitterPower', {}).get('unitCode'))
		rcc_unit = WMI_UNIT_MAP.get(rda.get('properties', {}).get('reflectivityCalibrationCorrection', {}).get('unitCode'))
		station = {
			'station_lat':											station_lat,
			'station_lon':											station_lon,
			'station_id':											feature.get('properties', {}).get('id', {}),
			'station_name':											feature.get('properties', {}).get('name', {}),
			'station_type':											feature.get('properties', {}).get('stationType', {}),
			'station_timezone':										feature.get('properties', {}).get('timeZone'),
			f'elevation_{elevation_unit}':							feature.get('properties', {}).get('elevation', {}).get('value'),
			f'latency_current_{latency_current_unit}':				feature.get('properties', {}).get('latency', {}).get('current', {}).get('value'),
			f'latency_average_{latency_average_unit}':				feature.get('properties', {}).get('latency', {}).get('average', {}).get('value'),
			f'latency_max_{latency_max_unit}':						feature.get('properties', {}).get('latency', {}).get('max', {}).get('value'),
			'latency_l2_last_received_at':							parse_timestamp(feature.get('properties', {}).get('latency', {}).get('levelTwoLastReceivedTime')),
			'max_latency_at':										parse_timestamp(feature.get('properties', {}).get('latency', {}).get('maxLatencyTime')),
			'station_reporting_host':								feature.get('properties', {}).get('latency', {}).get('reportingHost'),
			'station_server_host':									feature.get('properties', {}).get('latency', {}).get('host'),
			'rda_refreshed_at':										parse_timestamp(rda.get('timestamp')),
			'rda_reporting_host':									rda.get('reportingHost', {}),
			'rda_resolution_version':								rda.get('properties', {}).get('resolutionVersion'),
			'rda_nl2_path':											rda.get('properties', {}).get('nl2Path'),
			'rda_volume_coverage_pattern':							rda.get('properties', {}).get('volumeCoveragePattern'),
			'rda_control_status':									rda.get('properties', {}).get('controlStatus'),
			'rda_build_number':										rda.get('properties', {}).get('buildNumber'),
			'rda_alarm_summary':									rda.get('properties', {}).get('alarmSummary'),
			'rda_mode':												rda.get('properties', {}).get('mode'),
			'rda_generator_state':									rda.get('properties', {}).get('generatorState'),
			'rda_super_resolution_status':							rda.get('properties', {}).get('superResolutionStatus'),
			'rda_operability_status':								rda.get('properties', {}).get('operabilityStatus'),
			'rda_status':											rda.get('properties', {}).get('status'),
			f'rda_average_tx_power_{tx_power_unit}':				rda.get('properties', {}).get('averageTransmitterPower', {}).get('value'),
			f'rda_reflectivity_calibration_correction_{rcc_unit}':	rda.get('properties', {}).get('reflectivityCalibrationCorrection', {}).get('value'),
		}
		station = convert_measures(station)
		stations.append(station)
	return stations


@display_spinner('Getting radar station alarms...')
def get_radar_station_alarm_data(session: CachedSession, radar_station_id: str) -> dict:
	""" """
	raise NotImplementedError()


# See: https://www.weather.gov/mlb/text
@display_spinner('Getting text product types...')
def get_product_types_data(session: CachedSession) -> dict:
	""" """
	raise NotImplementedError()


@display_spinner('Getting product issuance locations...')
def get_product_locations_data(session: CachedSession) -> dict:
	""" """
	raise NotImplementedError()


@display_spinner('Getting text products...')
def get_products_data(session: CachedSession) -> dict:
	""" """
	raise NotImplementedError()


def pprint_raw_data_weather(
	location_data,
	local_stations_data,
	nearest_station,
	observations,
	forecast_extended,
	forecast_hourly,
	servers,
	alerts,
	alert_counts,
	radar_stations
):
	console = Console()
	console.print(f'location_data\n=============', style='bold red')
	pprint(location_data)
	console.print(f'local_stations_data\n===================', style='bold red')
	pprint(local_stations_data)
	console.print(f'nearest_station\n===============', style='bold red')
	pprint(nearest_station)
	console.print(f'observations\n============', style='bold red')
	pprint(observations)
	console.print(f'forecast_extended\n=================', style='bold red')
	pprint(forecast_extended)
	console.print(f'forecast_hourly\n===============', style='bold red')
	pprint(forecast_hourly)
	console.print(f'servers\n=======', style='bold red')
	pprint(servers)
	console.print(f'alerts\n======', style='bold red')
	pprint(alerts)
	console.print(f'alert_counts\n============', style='bold red')
	pprint(alert_counts)
	console.print(f'radar_stations\n==============', style='bold red')
	pprint(radar_stations)


def get_weather_for_location(session: CachedSession, address: str) -> dict:
	location_data = get_location_data(session, address)
	local_stations_data = get_local_stations_data(session, location_data)
	nearest_station = local_stations_data[1]['station_id']
	observations = get_station_observations_data(session, nearest_station)
	forecast_extended = get_extended_forecast_data(session, location_data)
	forecast_hourly = get_hourly_forecast_data(session, location_data)
	alerts = get_alerts_data_by_area(session, location_data['state'])
	alert_counts = get_alert_counts_data(session)
	servers = get_radar_server_data(session)
	radar_stations = get_radar_station_data(session)

	pprint_raw_data_weather(location_data,
							local_stations_data,
							nearest_station,
							observations,
							forecast_extended,
							forecast_hourly,
							servers,
							alerts,
							alert_counts,
							radar_stations)

# get_radar_server_data()
# get_radar_station_data
# get_glossary_data()
# get_station_observations_data()