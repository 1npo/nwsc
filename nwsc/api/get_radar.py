from requests_cache import CachedSession
from loguru import logger
from nwsc.decorators import display_spinner
from nwsc.api.conversion import convert_measures
from nwsc.api.api_request import api_request, parse_timestamp
from nwsc.api import (
	API_URL_NWS_SERVERS,
    API_URL_NWS_RADAR_STATIONS,
	WMI_UNIT_MAP,
)


# See:
# - https://www.ncdc.noaa.gov/wct/data.php
# -
#
# LDM = Local Data Manager
# RDS = Remote Data Server
# TDS = THREDDs Data Server
#
# NOTE: The official API documentation doesn't include a schema for the radar
# servers and stations endpoints, so some field meanings are inferred from the data.
@display_spinner('Getting radar server metadata...')
def get_radar_server_data(session: CachedSession) -> list:
	""" """
	radar_server_data = api_request(session, API_URL_NWS_SERVERS)
	servers = []
	for feature in radar_server_data.get('@graph', {}):
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
def get_radar_station_data(session: CachedSession) -> list:
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
	radar_alarm_data = api_request(session, API_URL_NWS_RADAR_STATIONS + radar_station_id + '/alarms')
	radar_alarms = []
	for alarm in radar_alarm_data.get('@graph', {}):
		alarm = {
			'alarm_status':		alarm.get('status'),
			'alarm_message':	alarm.get('message'),
			'alarm_event_at':	alarm.get('timestamp'),
			'active_channel':	alarm.get('activeChannel'),
		}
		radar_alarms.append(alarm)
	return radar_alarms
