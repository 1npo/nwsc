"""
"""


from requests_cache import CachedSession
from loguru import logger
from nwsc.render.decorators import display_spinner
from nwsc.api.api_request import api_request, parse_timestamp
from nwsc.api.geocode import uscb_geocode
from nwsc.api.conversion import convert_measures
from nwsc.api import (
	API_URL_NWS_POINTS,
	API_URL_NWS_STATIONS,
	METAR_CLOUD_COVER_MAP,
	WMI_UNIT_MAP
)


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
		'observed_at':      parse_timestamp(observations_data.get('properties', {}).get('timestamp')),
		'icon_url':         observations_data.get('properties', {}).get('icon'),
		'text_description': observations_data.get('properties', {}).get('textDescription'),
	}
	for api_name, new_name in observation_type_names.items():
		if api_name == 'cloudLayers':
			cloud_layers = {}
			for layer in observations_data.get('properties', {}).get(api_name):
				layer_amount = METAR_CLOUD_COVER_MAP.get(layer.get('amount'))
				layer_unit = WMI_UNIT_MAP.get(layer.get('base', {}).get('unitCode', {}))
				layer_height = layer.get('base', {}).get('value')
				if layer_height:
					layer_name = f'{layer_height}{layer_unit}'
				else:
					layer_name = 'None'
				cloud_layers.update({layer_name: layer_amount})
			observations[new_name] = cloud_layers
		else:
			observation_unit = WMI_UNIT_MAP.get(observations_data.get('properties', {}).get(api_name, {}).get('unitCode'))
			observations[f'{new_name}_{observation_unit}'] = observations_data.get('properties', {}).get(api_name, {}).get('value')
	observations = convert_measures(observations)
	return observations


def get_forecast_data(session: CachedSession, forecast_url: str) -> dict:
	"""Get the forecast for the given location"""
	forecast_data = api_request(session, forecast_url)
	len_periods = len(forecast_data.get('properties', {}).get('periods'))
	forecast = {}
	for i in range(0, len_periods):
		period = forecast_data.get('properties', {}).get('periods', {})
		if period and isinstance(period, list):
			period = period[i]
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

