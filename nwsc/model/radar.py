from typing import List, Dict
from datetime import datetime
from dataclasses import dataclass


@dataclass
class RadarStationAlarm:
    status: str
    message: str
    active_channel: int
    event_at: datetime


@dataclass
class RadarStationRDA:
    pass


@dataclass
class RadarStation:
    pass


@dataclass
class NetworkInterface:
    interface_name: str
    interface_refresh_at: datetime
    is_interface_active: bool
    packets_out_ok: int
    packets_out_error: int
    packets_out_dropped: int
    packets_out_overrun: int
    packets_in_ok: int
    packets_in_error: int
    packets_in_dropped: int
    packets_in_overrun: int


@dataclass
class RadarServer:
    server_host: str
    server_type: str
    server_up_since: datetime
    server_hardware_refresh_at: datetime
    server_cpu: float
    server_memory: float
    server_io_utilization: float
    server_disk: int
    server_load_1: float
    server_load_5: float
    server_load_15: float
    server_ports: List[NetworkInterface]
    command_last_executed: str
    command_last_executed_at: datetime
    command_last_nexrad_data_at: datetime
    command_last_received: str
    command_last_received_at: datetime
    command_last_refresh_at: datetime
    ldm_latest_product: datetime
    ldm_oldest_product: datetime
    ldm_storage_size: int
    ldm_count: int
    is_ldm_active: bool
    is_server_active: bool
    is_server_primary: bool
    is_server_aggregate: bool
    is_server_locked: bool
    is_radar_network_up: bool
    collection_time: datetime
    reporting_host: str
    last_ping_at: datetime
    ping_responses_ldm: Dict[str, bool]
    ping_responses_radar: Dict[str, bool]
    ping_responses_server: Dict[str, bool]
    ping_responses_misc: Dict[str, bool]
