from requests_cache import CachedSession
from nwsc.render.decorators import display_spinner
from nwsc.api.get_weather import process_measurement_values
from nwsc.api.conversions import convert_measures
from nwsc.api.api_request import api_request, parse_timestamp
from nwsc.api import (
	NWS_API_RADAR_SERVERS,
    NWS_API_RADAR_STATIONS,
	NWS_API_RADAR_QUEUES,
)


def process_radar_station_rda_data(radar_station_data: dict) -> dict:
	rda = radar_station_data.get('properties', {}).get('rda', {})
	station = {}
	if rda and isinstance(rda, dict):
		station.update({
			'refreshed_at':				parse_timestamp(rda.get('timestamp')),
			'reporting_host':			rda.get('reportingHost', {}),
			'resolution_version':		rda.get('properties', {}).get('resolutionVersion'),
			'nexrad_l2_path':			rda.get('properties', {}).get('nl2Path'),
			'volume_coverage_pattern':	rda.get('properties', {}).get('volumeCoveragePattern'),
			'control_status':			rda.get('properties', {}).get('controlStatus'),
			'build_number':				rda.get('properties', {}).get('buildNumber'),
			'alarm_summary':			rda.get('properties', {}).get('alarmSummary'),
			'mode':						rda.get('properties', {}).get('mode'),
			'generator_state':			rda.get('properties', {}).get('generatorState'),
			'super_resolution_status':	rda.get('properties', {}).get('superResolutionStatus'),
			'operability_status':		rda.get('properties', {}).get('operabilityStatus'),
			'status':					rda.get('properties', {}).get('status'),
		})
		field_map = {
			'averageTransmitterPower': 				'rda_average_tx_power',
			'reflectivityCalibrationCorrection':	'rda_reflectivity_calibration_correction',
		}
		expected_types = {
			'averageTransmitterPower': 				'wmoUnit:W',
			'reflectivityCalibrationCorrection':	'wmoUnit:dB',
		}
		rda_measures = rda.get('properties', {})
		station.update(process_measurement_values(rda_measures, field_map, expected_types))
	return station


def process_radar_station_performance_data(radar_station_data: dict) -> dict:
	performance = radar_station_data.get('properties', {}).get('performance')
	station = {}
	if performance and isinstance(performance, dict):
		station.update({
			'refreshed_at':					performance.get('timestamp'),
			'performance_checked_at':		performance.get('properties', {}).get('performanceCheckTime'),
			'reporting_host':				performance.get('reportingHost'),
			'ntp_status':					performance.get('properties', {}).get('ntp_status'),
			'command_channel':				performance.get('properties', {}).get('commandChannel'),
			'linearity':					performance.get('properties', {}).get('linearity'),
			'power_source':					performance.get('properties', {}).get('powerSource'),
			'transmitter_recycle_count':	performance.get('properties', {}).get('transmitterRecycleCount'),
			'transitional_power_source':	performance.get('properties', {}).get('transitionalPowerSource'),
			'elevation_encoder_light':		performance.get('properties', {}).get('elevationEncoderLight'),
			'azimuth_encoder_light':		performance.get('properties', {}).get('azimuthEncoderLight'),
		})
		field_map = {
			'fuelLevel': 						'fuel_level',
			'dynamicRange': 					'dynamic_range',
			'transmitterPeakPower': 			'transmitter_peak_power',
			'transmitterImbalance': 			'transmitter_imbalance',
			'transmitterLeavingAirTemperature': 'transmitter_leaving_air_temp',
			'shelterTemperature': 				'shelter_temp',
			'radomeAirTemperature': 			'radome_air_temp',
			'horizontalNoiseTemperature': 		'horizontal_noise_temp',
			'horizontalDeltadbZ0': 				'horizontal_delta',
			'verticalDeltadbZ0': 				'vertical_delta',
			'receiverBias': 					'receiver_bias',
			'horizontalShortPulseNoise': 		'horizontal_short_pulse_noise',
			'horizontalLongPulseNoise': 		'horizontal_long_pulse_noise',
		}
		expected_types = {
			'fuelLevel': 						'wmoUnit:percent',
			'dynamicRange': 					'wmoUnit:dB',
			'transmitterPeakPower': 			'wmoUnit:kW',
			'transmitterImbalance': 			'wmoUnit:dB',
			'transmitterLeavingAirTemperature': 'wmoUnit:degC',
			'shelterTemperature': 				'wmoUnit:degC',
			'radomeAirTemperature': 			'wmoUnit:degC',
			'horizontalNoiseTemperature': 		'wmoUnit:degC',
			'horizontalDeltadbZ0': 				'wmoUnit:dB',
			'verticalDeltadbZ0': 				'wmoUnit:dB',
			'receiverBias': 					'wmoUnit:dB',
			'horizontalShortPulseNoise': 		'wmoUnit:dB_m-1',
			'horizontalLongPulseNoise': 		'wmoUnit:dB_m-1',
		}
		performance_measures = performance.get('properties', {})
		station.update(process_measurement_values(performance_measures, field_map, expected_types))
	return station


def process_radar_station_adaptation_data(radar_station_data: dict) -> dict:
	adaptation = radar_station_data.get('properties', {}).get('adaptation')
	station = {}
	if adaptation and isinstance(adaptation, dict):
		station.update({
			'refreshed_at': 									adaptation.get('timestamp'),
			'reporting_host': 									adaptation.get('reportingHost'),
			'transmitter_frequency': 							adaptation.get('transmitterFrequency'),
			'transmitter_power_data_watts_factor': 				adaptation.get('transmitterPowerDataWattsFactor'),
			'antenna_gain_incl_radome': 						adaptation.get('antennaGainIncludingRadome'),
			'coho_power_at_a1j4': 								adaptation.get('cohoPowerAtA1J4'),
			'stalo_power_at_a1j2': 								adaptation.get('staloPowerAtA1J2'),
			'horizontal_receiver_noise_long_pulse': 			adaptation.get('horizontalReceiverNoiseLongPulse'),
			'horizontal_receiver_noise_short_pulse': 			adaptation.get('horizontalReceiverNoiseShortPulse'),
			'transmitter_spectrum_filter_installed': 			adaptation.get('transmitterSpectrumFilterInstalled'),
			'pulse_width_transmitter_out_long_pulse': 			adaptation.get('pulseWidthTransmitterOutputLongPulse'),
			'pulse_width_transmitter_out_short_pulse': 			adaptation.get('pulseWidthTransmitterOutputShortPulse'),
			'ame_noise_source_horizontal_excess_noise_ratio': 	adaptation.get('ameNoiseSourceHorizontalExcessNoiseRatio'),
			'ame_horizontal_test_signal_power': 				adaptation.get('ameHorzizontalTestSignalPower'),
			'path_loss_wg04_circulator':						adaptation.get('pathLossWG04Circulator'),
			'path_loss_wg02_harmonic_filter':					adaptation.get('pathLossWG02HarmonicFilter'),
			'path_loss_wg06_spectrum_filter':					adaptation.get('pathLossWG06SpectrumFilter'),
			'path_loss_ifd_rif_anti_alias_filter':				adaptation.get('pathLossIFDRIFAntiAliasFilter'),
			'path_loss_ifd_burst_anti_alias_filter':			adaptation.get('pathLossIFDBurstAntiAliasFilter'),
			'path_loss_a6_arc_detector':						adaptation.get('pathLossA6ArcDetector'),
			'path_loss_transmitter_coupler_coupling':			adaptation.get('pathLossTransmitterCouplerCoupling'),
			'path_loss_vertical_f_heliax_to_4at16':				adaptation.get('pathLossVerticalIFHeliaxTo4AT16'),
			'path_loss_horizontal_f_heliax_to_4at17':			adaptation.get('pathLossHorzontalIFHeliaxTo4AT17'),
			'path_loss_at4_attenuator':							adaptation.get('pathLossAT4Attenuator'),
			'path_loss_waveguide_klystron_to_switch':			adaptation.get('pathLossWaveguideKlystronToSwitch'),
		})
	station = convert_measures(station)
	return station


def process_radar_station_data(radar_station_data: dict) -> dict:
	station_coords = radar_station_data.get('geometry', {}).get('coordinates')
	if station_coords and isinstance(station_coords, list):
		station_lat = station_coords[0]
		station_lon = station_coords[1]
	station = {
		'lat':									station_lat,
		'lon':									station_lon,
		'server_host':							radar_station_data.get('properties', {}).get('latency', {}).get('host'),
		'reporting_host':						radar_station_data.get('properties', {}).get('latency', {}).get('reportingHost'),
		'id':									radar_station_data.get('properties', {}).get('id', {}),
		'name':									radar_station_data.get('properties', {}).get('name', {}),
		'type':									radar_station_data.get('properties', {}).get('stationType', {}),
		'timezone':								radar_station_data.get('properties', {}).get('timeZone'),
		'latency_nexrad_l2_last_received_at':	parse_timestamp(radar_station_data.get('properties', {}).get('latency', {}).get('levelTwoLastReceivedTime')),
		'latency_max_at':						parse_timestamp(radar_station_data.get('properties', {}).get('latency', {}).get('maxLatencyTime')),
	}
	elevation_measures = radar_station_data.get('properties', {})
	station.update(process_measurement_values(elevation_measures,
											  {'elevation': 'elevation'},
											  {'elevation': 'wmoUnit:m'}))
	for latency_type in ('current', 'average', 'max'):
		latency_measures = radar_station_data.get('properties', {}).get('latency', {})
		station.update(process_measurement_values(latency_measures,
												  {latency_type: f'latency_{latency_type}'},
												  {latency_type: 'nwsUnit:s'}))
	station.update(process_radar_station_rda_data(radar_station_data))
	station.update(process_radar_station_performance_data(radar_station_data))
	station.update(process_radar_station_adaptation_data(radar_station_data))
	return station


def process_radar_server_data(radar_server_data: dict) -> dict:
	server = {
		'host':                  			radar_server_data.get('id'),
		'type':                  			radar_server_data.get('type'),
		'up_since':              			parse_timestamp(radar_server_data.get('hardware', {}).get('uptime')),
		'hardware_refresh_at':   			parse_timestamp(radar_server_data.get('hardware', {}).get('timestamp')),
		'cpu':                   			radar_server_data.get('hardware', {}).get('cpuIdle'),
		'memory':                			radar_server_data.get('hardware', {}).get('memory'),
		'io_utilization':        			radar_server_data.get('hardware', {}).get('ioUtilization'),
		'disk':                  			radar_server_data.get('hardware', {}).get('disk'),
		'load_1':                			radar_server_data.get('hardware', {}).get('load1'),
		'load_5':                			radar_server_data.get('hardware', {}).get('load5'),
		'load_15':               			radar_server_data.get('hardware', {}).get('load15'),
		'command_last_executed':        	radar_server_data.get('command', {}).get('lastExecuted'),
		'command_last_executed_at':     	parse_timestamp(radar_server_data.get('command', {}).get('lastExecutedTime')),
		'command_last_nexrad_data_at':  	parse_timestamp(radar_server_data.get('command', {}).get('lastNexradDataTime')),
		'command_last_received':        	radar_server_data.get('command', {}).get('lastReceived'),
		'command_last_received_at':     	parse_timestamp(radar_server_data.get('command', {}).get('lastReceivedTime')),
		'command_last_refresh_at':      	parse_timestamp(radar_server_data.get('command', {}).get('timestamp')),
		'ldm_refresh_at':               	parse_timestamp(radar_server_data.get('ldm', {}).get('timestamp')),
		'ldm_latest_product_at':        	parse_timestamp(radar_server_data.get('ldm', {}).get('latestProduct')),
		'ldm_oldest_product_at':        	parse_timestamp(radar_server_data.get('ldm', {}).get('oldestProduct')),
		'ldm_storage_size':             	radar_server_data.get('ldm', {}).get('storageSize'),
		'ldm_count':                    	radar_server_data.get('ldm', {}).get('count'),
		'is_ldm_active':                	radar_server_data.get('ldm', {}).get('active'),
		'is_server_active':             	radar_server_data.get('active'),
		'is_server_primary':            	radar_server_data.get('primary'),
		'is_server_aggregate':          	radar_server_data.get('aggregate'),
		'is_server_locked':             	radar_server_data.get('locked'),
		'is_radar_network_up':          	radar_server_data.get('radarNetworkUp'),
		'collection_time':              	parse_timestamp(radar_server_data.get('collectionTime')),
		'reporting_host':               	radar_server_data.get('reportingHost'),
		'last_ping_at':                 	parse_timestamp(radar_server_data.get('ping', {}).get('timestamp')),
		'ping_responses_ldm':           	radar_server_data.get('ping', {}).get('targets', {}).get('ldm'),
		'ping_responses_radar':         	radar_server_data.get('ping', {}).get('targets', {}).get('radar'),
		'ping_responses_server':        	radar_server_data.get('ping', {}).get('targets', {}).get('server'),
		'ping_responses_misc':          	radar_server_data.get('ping', {}).get('targets', {}).get('misc'),
		'network_interfaces_refreshed_at':	parse_timestamp(radar_server_data.get('network', {}).get('timestamp')),
		'interfaces':                   	[],
	}
	for item in radar_server_data.get('network', {}):
		if item != 'timestamp':
			server['interfaces'].append({
				'interface_name':       radar_server_data.get('network', {}).get(item, {}).get('interface'),
				'is_interface_active':  radar_server_data.get('network', {}).get(item, {}).get('active'),
				'packets_out_ok':       radar_server_data.get('network', {}).get(item, {}).get('transNoError'),
				'packets_out_error':    radar_server_data.get('network', {}).get(item, {}).get('transError'),
				'packets_out_dropped':  radar_server_data.get('network', {}).get(item, {}).get('transDropped'),
				'packets_out_overrun':  radar_server_data.get('network', {}).get(item, {}).get('transOverrun'),
				'packets_in_ok':        radar_server_data.get('network', {}).get(item, {}).get('recvNoError'),
				'packets_in_error':     radar_server_data.get('network', {}).get(item, {}).get('recvError'),
				'packets_in_dropped':   radar_server_data.get('network', {}).get(item, {}).get('recvDropped'),
				'packets_in_overrun':   radar_server_data.get('network', {}).get(item, {}).get('recvOverrun'),
			})
	return server


@display_spinner('Getting radar station alarms...')
def get_radar_station_alarms(session: CachedSession, radar_station_id: str) -> dict:
	""" """
	radar_alarm_data = api_request(session, NWS_API_RADAR_STATIONS + radar_station_id + '/alarms')
	radar_alarms = []
	for alarm in radar_alarm_data.get('@graph', {}):
		radar_alarms.append({
			'status':			alarm.get('status'),
			'message':			alarm.get('message'),
			'event_at':			alarm.get('timestamp'),
			'active_channel':	alarm.get('activeChannel'),
		})
	return radar_alarms


@display_spinner('Getting radar stations...')
def get_radar_stations(session: CachedSession) -> list:
	""" """
	radar_stations_data = api_request(session, NWS_API_RADAR_STATIONS)
	stations = []
	for feature in radar_stations_data.get('features', {}):
		stations.append(process_radar_station_data(feature))
	return stations


@display_spinner('Getting radar station details...')
def get_radar_station(session: CachedSession, station_id: str) -> dict:
	""" """
	radar_station_data = api_request(session, NWS_API_RADAR_STATIONS + station_id)
	return process_radar_station_data(radar_station_data)


# See:
# - https://www.ncdc.noaa.gov/wct/data.php
#
# LDM = Local Data Manager
# RDS = Remote Data Server
# TDS = THREDDs Data Server
#
# NOTE: The official API documentation doesn't include a schema for the radar
# servers and stations endpoints, so some field meanings are inferred from the data.
@display_spinner('Getting radar servers...')
def get_radar_servers(session: CachedSession) -> list:
	""" """
	radar_servers_data = api_request(session, NWS_API_RADAR_SERVERS)
	servers = []
	for feature in radar_servers_data.get('@graph', {}):
		servers.append(process_radar_server_data(feature))
	return servers


@display_spinner('Getting radar server details...')
def get_radar_server(session: CachedSession, server_id: str) -> dict:
	""" """
	radar_server_data = api_request(session, NWS_API_RADAR_SERVERS + server_id)
	return process_radar_server_data(radar_server_data)


@display_spinner('Getting radar queue for host and station...')
def get_radar_queue(session: CachedSession, ldm_host: str, station_id: str) -> dict:
	""" """
	radar_queue_data = api_request(session, NWS_API_RADAR_QUEUES + ldm_host + f'?station={station_id}')
	radar_queue = []
	for item in radar_queue_data.get('@graph', {}):
		radar_queue.append({
			'host':					item.get('host'),
			'arrived_at':			item.get('arrivalTime'),
			'created_at':			item.get('createdAt'),
			'station_id':			item.get('stationId'),
			'type':					item.get('type'),
			'feed':					item.get('feed'),
			'resolution_version':	item.get('resolutionVersion'),
			'sequence_number':		item.get('sequenceNumber'),
			'size':					item.get('size'),
		})
	return radar_queue