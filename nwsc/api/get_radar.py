from requests_cache import CachedSession
from loguru import logger
from nwsc.render.decorators import display_spinner
from nwsc.api.conversions import convert_measures
from nwsc.api.api_request import api_request, parse_timestamp
from nwsc.api import (
	API_URL_NWS_RADAR_SERVERS,
    API_URL_NWS_RADAR_STATIONS,
	WMI_UNIT_MAP,
)


def parse_radar_server_data(radar_server_data: dict) -> dict:
	pass


def parse_radar_station_data(radar_station_data: dict) -> dict:
	station_coords = radar_station_data.get('geometry', {}).get('coordinates')
	if station_coords and isinstance(station_coords, list):
		station_lat = station_coords[0]
		station_lon = station_coords[1]
	elevation_unit = WMI_UNIT_MAP.get(radar_station_data.get('properties', {}).get('elevation', {}).get('unitCode'))
	latency_current_unit = WMI_UNIT_MAP.get(radar_station_data.get('latency', {}).get('current', {}).get('unitCode'))
	latency_average_unit = WMI_UNIT_MAP.get(radar_station_data.get('latency', {}).get('current', {}).get('unitCode'))
	latency_max_unit = WMI_UNIT_MAP.get(radar_station_data.get('latency', {}).get('current', {}).get('unitCode'))
	tx_power_unit = WMI_UNIT_MAP.get(rda.get('properties', {}).get('averageTransmitterPower', {}).get('unitCode'))
	rcc_unit = WMI_UNIT_MAP.get(rda.get('properties', {}).get('reflectivityCalibrationCorrection', {}).get('unitCode'))
	station = {
		'station_lat':											station_lat,
		'station_lon':											station_lon,
		'station_id':											radar_station_data.get('properties', {}).get('id', {}),
		'station_name':											radar_station_data.get('properties', {}).get('name', {}),
		'station_type':											radar_station_data.get('properties', {}).get('stationType', {}),
		'station_timezone':										radar_station_data.get('properties', {}).get('timeZone'),
		f'elevation_{elevation_unit}':							radar_station_data.get('properties', {}).get('elevation', {}).get('value'),
		f'latency_current_{latency_current_unit}':				radar_station_data.get('properties', {}).get('latency', {}).get('current', {}).get('value'),
		f'latency_average_{latency_average_unit}':				radar_station_data.get('properties', {}).get('latency', {}).get('average', {}).get('value'),
		f'latency_max_{latency_max_unit}':						radar_station_data.get('properties', {}).get('latency', {}).get('max', {}).get('value'),
		'nexrad_l2_latency_last_received_at':					parse_timestamp(radar_station_data.get('properties', {}).get('latency', {}).get('levelTwoLastReceivedTime')),
		'max_latency_at':										parse_timestamp(radar_station_data.get('properties', {}).get('latency', {}).get('maxLatencyTime')),
		'station_reporting_host':								radar_station_data.get('properties', {}).get('latency', {}).get('reportingHost'),
		'station_server_host':									radar_station_data.get('properties', {}).get('latency', {}).get('host'),
		'rda_refreshed_at':										parse_timestamp(rda.get('timestamp')),
	}
	rda = radar_station_data.get('properties', {}).get('rda', {})
	if rda and isinstance(rda, dict):
		station.update({
			'rda_reporting_host':									rda.get('reportingHost', {}),
			'rda_resolution_version':								rda.get('properties', {}).get('resolutionVersion'),
			'rda_nexrad_l2_path':									rda.get('properties', {}).get('nl2Path'),
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
		})
	performance = radar_station_data.get('properties', {}).get('performance')
	if performance and isinstance(performance, dict):
		station.update({
			'refreshed_at':						performance.get('timestamp'),
			'performance_checked_at':			performance.get('properties', {}).get('performanceCheckTime'),
			'reporting_host':					performance.get('reportingHost'),
			'ntp_status':						performance.get('properties', {}).get('ntp_status'),
			'command_channel':					performance.get('properties', {}).get('commandChannel'),
			'linearity':						performance.get('properties', {}).get('linearity'),
			'power_source':						performance.get('properties', {}).get('powerSource'),
			'fuel_level':						performance.get('properties', {}).get('fuelLevel'),
			'dynamic_range':					performance.get('properties', {}).get('dynamicRange'),
			'transmitter_peak_power':			performance.get('properties', {}).get('transmitterPeakPower'),
			'transmitter_recycle_count':		performance.get('properties', {}).get('transmitterRecycleCount'),
			'transmitter_imbalance':			performance.get('properties', {}).get('transmitterImbalance'),
			'transmitter_leaving_air_temp_c':	performance.get('properties', {}).get('transmitterLeavingAirTemperature'),
			'shelter_temp_c':					performance.get('properties', {}).get('shelterTemperature'),
			'radome_air_temp_c':				performance.get('properties', {}).get('radomeAirTemperature'),
			'horizontal_noise_temp_c':			performance.get('properties', {}).get('horizontalNoiseTemperature'),
			'transitional_power_source':		performance.get('properties', {}).get('transitionalPowerSource'),
			'elevation_encoder_light':			performance.get('properties', {}).get('elevationEncoderLight'),
			'azimuth_encoder_light':			performance.get('properties', {}).get('azimuthEncoderLight'),
			'horizontal_delta_db':				performance.get('properties', {}).get('horizontalDeltadbZ0'),
			'vertical_delta_db':				performance.get('properties', {}).get('verticalDeltadbZ0'),
			'receiver_bias':					performance.get('properties', {}).get('receiverBias'),
			'horizontal_short_pulse_noise':		performance.get('properties', {}).get('horizontalShortPulseNoise'),
			'horizontal_long_pulse_noise':		performance.get('properties', {}).get('horizontalLongPulseNoise'),
		})
	adaptation = radar_station_data.get('properties', {}).get('adaptation')
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


@display_spinner('Getting radar station metadata...')
def get_radar_stations(session: CachedSession) -> list:
	""" """
	radar_station_data = api_request(session, API_URL_NWS_RADAR_STATIONS)
	stations = []
	for feature in radar_station_data.get('features', {}):
		station = parse_radar_station_data(feature)
		station = convert_measures(station)
		stations.append(station)
	return stations


@display_spinner('Getting radar station alarms...')
def get_radar_station_alarms(session: CachedSession, radar_station_id: str) -> dict:
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


# See:
# - https://www.ncdc.noaa.gov/wct/data.php
#
# LDM = Local Data Manager
# RDS = Remote Data Server
# TDS = THREDDs Data Server
#
# NOTE: The official API documentation doesn't include a schema for the radar
# servers and stations endpoints, so some field meanings are inferred from the data.
@display_spinner('Getting radar server metadata...')
def get_radar_servers(session: CachedSession) -> list:
	""" """
	radar_server_data = api_request(session, API_URL_NWS_RADAR_SERVERS)
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
