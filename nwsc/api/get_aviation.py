from requests_cache import CachedSession
from loguru import logger
from nwsc.render.decorators import display_spinner
from nwsc.api.api_request import api_request
from nwsc.api import (
    NWS_API_AVIATION_SIGMETS,
    NWS_API_AVIATION_CWSU,
)


def process_sigmets_data(sigmets: dict) -> dict:
    sigmet = {
        'sigmets_url':      sigmets.get('properties', {}).get('id'),
        'issued_at':        sigmets.get('properties', {}).get('issueTime'),
        'effective_at':     sigmets.get('properties', {}).get('start'),
        'expires_at':       sigmets.get('properties', {}).get('end'),
        'fir':              sigmets.get('properties', {}).get('fir'),
        'atsu':             sigmets.get('properties', {}).get('atsu'),
        'sequence':         sigmets.get('properties', {}).get('sequence'),
        'phenomenon':       sigmets.get('properties', {}).get('phenomenon'),
    }
    geometry = sigmets.get('geometry')
    if geometry:
        sigmet.update({'area_polygon': geometry.get('coordinates')})
    return sigmet


def process_sigmets(sigmets_data: list) -> list:
    sigmets = []
    for feature in sigmets_data.get('features', {}):
        sigmets.append(process_sigmets_data(feature))
    return sigmets


def process_cwa_data(cwa: dict) -> dict:
    cwa = {
        'url':                  cwa.get('properties', {}).get('id'),
        'cwsu':                 cwa.get('properties', {}).get('cwsu'),
        'sequence':             cwa.get('properties', {}).get('sequence'),
        'issued_at':            cwa.get('properties', {}).get('issueTime'),
        'effective_at':         cwa.get('properties', {}).get('start'),
        'expires_at':           cwa.get('properties', {}).get('end'),
        'observed_property':    cwa.get('properties', {}).get('observedProperty'),
        'text':                 cwa.get('properties', {}).get('text'),
    }
    geometry = cwa.get('geometry')
    if geometry:
        cwa.update({'area_polygon': geometry.get('coordinates')})
    return cwa


@display_spinner('Getting all SIGMETs...')
def get_all_sigmets(session: CachedSession) -> dict:
    sigmets_data = api_request(session, NWS_API_AVIATION_SIGMETS)
    return process_sigmets(sigmets_data)


@display_spinner('Getting all SIGMETs issued by ATSU...')
def get_all_atsu_sigmets(session: CachedSession, atsu: str) -> list:
    sigmets_data = api_request(session, NWS_API_AVIATION_SIGMETS + atsu)
    return process_sigmets(sigmets_data)


@display_spinner('Getting all SIGMETs issued by ATSU on date...')
def get_all_atsu_sigmets_by_date(session: CachedSession, atsu: str, date_str: str) -> list:
    sigmets_data = api_request(session, NWS_API_AVIATION_SIGMETS + atsu + f'/{date_str}')
    return process_sigmets(sigmets_data)


@display_spinner('Getting SIGMET...')
def get_sigmet(session: CachedSession, atsu: str, date_str: str, time_str) -> list:
    sigmet_data = api_request(session, NWS_API_AVIATION_SIGMETS + atsu + f'/{date_str}/{time_str}')
    return process_sigmets_data(sigmet_data)


@display_spinner('Getting CWSU details...')
def get_cwsu(session: CachedSession, cwsu_id: str) -> dict:
    cwsu_data = api_request(session, NWS_API_AVIATION_CWSU + cwsu_id)
    return {
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


@display_spinner('Getting all CWAs issued by CWSU...')
def get_cwas(session: CachedSession, cwsu_id: str) -> list:
    cwas_data = api_request(session, NWS_API_AVIATION_CWSU + cwsu_id + '/cwas')
    cwas = []
    for feature in cwas_data.get('features', {}):
        cwas.append(process_cwa_data(feature))
    return cwas


@display_spinner('Getting CWA...')
def get_cwa(session: CachedSession, cwsu_id: str, date_str: str, sequence: int) -> dict:
    cwa_data = api_request(session, NWS_API_AVIATION_CWSU + cwsu_id + f'/cwas/{date_str}/{sequence}')
    return process_cwa_data(cwa_data)

