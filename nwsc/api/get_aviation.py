from typing import List
from requests_cache import CachedSession
from nwsc.render.decorators import display_spinner
from nwsc.api.api_request import api_request
from nwsc.api import (
    NWS_API_AVIATION_SIGMETS,
    NWS_API_AVIATION_CWSU,
)
from nwsc.model.aviation import SIGMET, CenterWeatherAdvisory, CentralWeatherServiceUnit


def process_sigmet_data(sigmet_data: dict) -> SIGMET:
    sigmet_dict = {
        'url':              sigmet_data.get('properties', {}).get('id'),
        'issued_at':        sigmet_data.get('properties', {}).get('issueTime'),
        'effective_at':     sigmet_data.get('properties', {}).get('start'),
        'expires_at':       sigmet_data.get('properties', {}).get('end'),
        'fir':              sigmet_data.get('properties', {}).get('fir'),
        'atsu':             sigmet_data.get('properties', {}).get('atsu'),
        'sequence':         sigmet_data.get('properties', {}).get('sequence'),
        'phenomenon':       sigmet_data.get('properties', {}).get('phenomenon'),
        'area_polygon':     None,
    }
    geometry = sigmet_data.get('geometry')
    if geometry:
        sigmet_dict.update({'area_polygon': geometry.get('coordinates')})
    return SIGMET(**sigmet_dict)


def process_sigmets(sigmets_data: list) -> List[SIGMET]:
    sigmets = []
    for feature in sigmets_data.get('features', {}):
        sigmets.append(process_sigmet_data(feature))
    return sigmets


@display_spinner('Getting all SIGMETs...')
def get_all_sigmets(session: CachedSession) -> List[SIGMET]:
    sigmets_data = api_request(session, NWS_API_AVIATION_SIGMETS)
    return process_sigmets(sigmets_data)


@display_spinner('Getting all SIGMETs issued by ATSU...')
def get_all_atsu_sigmets(
    session: CachedSession,
    atsu: str
) -> List[SIGMET]:
    sigmets_data = api_request(session, NWS_API_AVIATION_SIGMETS + atsu)
    return process_sigmets(sigmets_data)


@display_spinner('Getting all SIGMETs issued by ATSU on date...')
def get_all_atsu_sigmets_by_date(
    session: CachedSession,
    atsu: str,
    date_str: str
) -> List[SIGMET]:
    sigmets_data = api_request(session, NWS_API_AVIATION_SIGMETS + atsu + f'/{date_str}')
    return process_sigmets(sigmets_data)


@display_spinner('Getting SIGMET...')
def get_sigmet(
    session: CachedSession,
    atsu: str,
    date_str: str,
    time_str
) -> SIGMET:
    sigmet_data = api_request(session, NWS_API_AVIATION_SIGMETS + atsu + f'/{date_str}/{time_str}')
    return process_sigmet_data(sigmet_data)


def process_cwa_data(cwa_data: dict) -> CenterWeatherAdvisory:
    cwa_dict = {
        'url':                      cwa_data.get('properties', {}).get('id'),
        'text':                     cwa_data.get('properties', {}).get('text'),
        'cwsu':                     cwa_data.get('properties', {}).get('cwsu'),
        'sequence':                 cwa_data.get('properties', {}).get('sequence'),
        'issued_at':                cwa_data.get('properties', {}).get('issueTime'),
        'effective_at':             cwa_data.get('properties', {}).get('start'),
        'expires_at':               cwa_data.get('properties', {}).get('end'),
        'observed_property_url':    cwa_data.get('properties', {}).get('observedProperty'),
        'area_polygon':             None,
    }
    geometry = cwa_data.get('geometry')
    if geometry:
        cwa_dict.update({'area_polygon': geometry.get('coordinates')})
    return CenterWeatherAdvisory(**cwa_dict)


@display_spinner('Getting CWSU details...')
def get_cwsu(
    session: CachedSession,
    cwsu_id: str
) -> CentralWeatherServiceUnit:
    cwsu_data = api_request(session, NWS_API_AVIATION_CWSU + cwsu_id)
    cwsu_dict = {
        'id':           cwsu_data.get('id'),
        'name':         cwsu_data.get('name'),
        'street':       cwsu_data.get('street'),
        'city':         cwsu_data.get('city'),
        'state':        cwsu_data.get('state'),
        'zip_code':     cwsu_data.get('zipCcode'),
        'email':        cwsu_data.get('email'),
        'fax':          cwsu_data.get('fax'),
        'phone':        cwsu_data.get('phone'),
        'url':          cwsu_data.get('url'),
        'nws_region':   cwsu_data.get('nwsRegion'),
    }
    return CentralWeatherServiceUnit(**cwsu_dict)


@display_spinner('Getting all CWAs issued by CWSU...')
def get_cwas(
    session: CachedSession,
    cwsu_id: str
) -> List[CenterWeatherAdvisory]:
    cwas_data = api_request(session, NWS_API_AVIATION_CWSU + cwsu_id + '/cwas')
    cwas = []
    for feature in cwas_data.get('features', {}):
        cwas.append(process_cwa_data(feature))
    return cwas


@display_spinner('Getting CWA...')
def get_cwa(
    session: CachedSession,
    cwsu_id: str,
    date_str: str,
    sequence: int
) -> CenterWeatherAdvisory:
    cwa_data = api_request(session, NWS_API_AVIATION_CWSU + cwsu_id + f'/cwas/{date_str}/{sequence}')
    return process_cwa_data(cwa_data)
