# TODO: Figure out when, how, and if these functions should be used to
# update `nwsc.api.VALID_NWS_*` globals. In the meantime, only use the
# hardcoded values.


import json
from typing import Union
from string import Template
from requests_cache import CachedSession
from loguru import logger
from rich.pretty import pprint
from nwsc.api.api_request import api_request
from nwsc.api import (
    API_URL_NWS_ZONES,
    API_URL_NWS_OFFICES,
    INVALID_ENUM_MESSAGE_DELIMITER,
    FAILED_TO_GET_ENUM_MESSAGE,
)


def process_error_response(parameter_errors: dict, failure_message: str) -> Union[dict, None]:
    enums = []
    if isinstance(parameter_errors, list):
        for error in parameter_errors:
            if isinstance(error, dict):
                message = error.get('message')
                if message and INVALID_ENUM_MESSAGE_DELIMITER in message:
                    enum_str = message.split(INVALID_ENUM_MESSAGE_DELIMITER)[1]
                    enum_list = json.loads(enum_str)
                    if enum_list and isinstance(enum_list, list):
                        enums.extend(enum_list)
    if not enums:
        logger.warning(failure_message)
        return None
    return enums


def get_valid_zones(session: CachedSession) -> list:
    enum_data = api_request(session, API_URL_NWS_ZONES + 'DEADBEEF')
    parameter_errors = enum_data.get('parameterErrors', {})
    failure_message = Template(FAILED_TO_GET_ENUM_MESSAGE).substitute(enum_type='zones')
    return process_error_response(parameter_errors, failure_message)


def get_valid_forecast_offices(session: CachedSession) -> list:
    enum_data = api_request(session, API_URL_NWS_OFFICES + 'DEADBEEF')
    parameter_errors = enum_data.get('parameterErrors', {})
    failure_message = Template(FAILED_TO_GET_ENUM_MESSAGE).substitute(enum_type='forecast offices')
    return process_error_response(parameter_errors, failure_message)
