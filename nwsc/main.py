__version__ = '0.1.0'


import os
import sys
import argparse
import pandas as pd
from pathlib import Path
from datetime import datetime

from loguru import logger
from requests_cache import CachedSession, SQLiteCache, FileCache

from nwsc.config import ConfigManager
from nwsc.render.decorators import display_spinner
from nwsc.render.pprint_raw import pprint_raw_nws_data, nws_data_to_json
from nwsc.render.rich_print import (
    rich_print_current_conditions,
	rich_print_extended_forecast,
	rich_print_settings,
	rich_print_overview,
	)


class LogFilter:
    def __init__(self, level):
        self.level = level
	
    def __call__(self, record):
        levelno = logger.level(self.level).no
        return record["level"].no >= levelno


log_filter = LogFilter('INFO')
LOG_FMT_TERM = '[<level>{level: <8}</level>] <level>{message}</level>'
logger.remove()
logger.add(sys.stderr, format=LOG_FMT_TERM, filter=log_filter, level=0)


parser = argparse.ArgumentParser(prog='nws',
								 formatter_class=argparse.RawDescriptionHelpFormatter,
								 description=f'nws v{__version__} - Lightweight NWS API Client for the Terminal')
parser.add_argument('--debug', action='store_true', help='Display debugging information in the terminal')
parser.add_argument('--save', action='store_true', help='Save the current observations to an Excel file')
parser_location = parser.add_mutually_exclusive_group()
parser_location.add_argument('--address', action='store', type=str, help='Get the weather from the station nearest to this address (default: address in user settings)')
parser_location.add_argument('--station', action='store', type=str, help='Get the weather from this 4-letter station ID (default: nearest station to the address in user settings)')
subparsers = parser.add_subparsers(dest='command')
parser_current = subparsers.add_parser('current', help='Get the current observations')
parser_overview = subparsers.add_parser('overview', help='Get the current observations plus the 3 day forecast')
parser_forecast = subparsers.add_parser('forecast', help='Get the weather forecast')
parser_forecast.add_argument('forecast-type', nargs='?', choices=['3day', '7day', 'hourly'], help='The type of forecast to get (default: 3day)')
parser_forecast.add_argument('--save', action='store_true', help='Save the forecast to an Excel file')
parser_set = subparsers.add_parser('set', help='Change a setting')
parser_set.add_argument('set', action='store', type=str, help='Change the value of this setting')
parser_set.add_argument('value', action='store', type=str, help='Change the setting to this value')
parser_get = subparsers.add_parser('get', help='Display the current value of a setting (or display all settings of none specified)')
parser_get.add_argument('get', action='store', type=str, nargs='?', default=None, help='Print the current value of this setting (or print all if setting not specified)')


def df_to_file(
	config: ConfigManager,
	name: str,
	df: pd.DataFrame,
	index=False
):
	"""Save the given dataframe to a file
	
	:param config: An instance of ConfigManager
	:param name: The name of the export (eg 'current', 'overview', 'forecast')
	:param df: The dataframe to save to a file
	"""
	output_dir = config.get('exports_dir')
	if not os.path.isfile(output_dir):
		Path(output_dir).mkdir(parents=True, exist_ok=True)

	timestamp = datetime.now().strftime('%Y-%m-%d_%I%M%S%p')
	output_file = f'nws_api_export_{name}_{timestamp}.xlsx'
	output_path = os.path.join(output_dir, output_file)
	with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
		df.to_excel(writer, index=index, sheet_name=name)
	logger.info(f'Saved {name} to file: {output_path}')


def main():
	config = ConfigManager()
	params, other = parser.parse_known_args()
	address = params.address if params.address else config.get('address')
	backend = SQLiteCache()
	session = CachedSession('nwsc_cache', backend=backend, use_cache_dir=True)
	with session:
		if params.debug:
			log_filter.level = 'DEBUG'
		
		if params.command == 'get':
			if not params.get:
				rich_print_settings(config.get_all())
			else:
				print(f'{params.get} = {config.get(params.get)}')
			exit(0)

		if params.command == 'set':
			config.set(params.set, params.value)
			logger.info(f'Set "{params.set}" to "{params.value}"')
			exit(0)
		
		if params.command == 'overview':
			#forecast_df = extended_forecast_to_dforecast_hourlyf(address, periods=6)
			#current_df = current_observations_to_df(address)
			#rich_print_overview(current_df.iloc[0], forecast_df)
			#if params.save:
			#	df_to_file(config, 'current', current_df)
			#	df_to_file(config, 'forecast', forecast_df)
			exit(0)

		if params.command == 'forecast':
			#match params.forecast_type:
			#	case 'hourly':
			#		forecast_df = hourly_forecast_to_df(address)
			#	case '7day':
			#		forecast_df = extended_forecast_to_df(address)
			#	case '3day':
			#		forecast_df = extended_forecast_to_df(address, periods=6)
			#	case _:
			#		forecast_df = extended_forecast_to_df(address, periods=6)
			#rich_print_extended_forecast(forecast_df)
			#if params.save:
			#	df_to_file(config, 'forecast', forecast_df)
			exit(0)

		if params.command in (None, 'current'):
			#current_df = current_observations_to_df(address)
			#rich_print_current_conditions(current_df.iloc[0])
			#if params.save:
			#	df_to_file(config, 'observations', current_df.iloc[0], index=True)
			pprint_raw_nws_data(session, '3121 S Las Vegas Blvd, Las Vegas, NV 89109')
			#nws_data_to_json(session, '3121 S Las Vegas Blvd, Las Vegas, NV 89109')
			exit(0)
