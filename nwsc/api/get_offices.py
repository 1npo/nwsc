from requests_cache import CachedSession
from loguru import logger
from nwsc.render.decorators import display_spinner
from nwsc.api.api_request import api_request
from nwsc.api import (
    NWS_API_OFFICES,
    VALID_NWS_FORECAST_OFFICES,
)


InvalidOfficeException = ValueError(
    f'Invalid forecast office. Please specify a valid forecast office: '
    f'{", ".join(VALID_NWS_FORECAST_OFFICES)}'
)


def process_headline_data(headline: dict) -> dict:
    return {
            'id':                   headline.get('id'),
            'name':                 headline.get('name'),
            'title':                headline.get('title'),
            'issued_at':            headline.get('issuanceTime'),
            'url':                  headline.get('link'),
            'content':              headline.get('content'),
            'headline_summary':     headline.get('summary'),
            'office_url':           headline.get('office'),
            'is_important':         headline.get('important'),
        }


@display_spinner('Getting office headlines...')
def get_office_headlines(session: CachedSession, office_id: str) -> dict:
    if office_id not in VALID_NWS_FORECAST_OFFICES:
        raise InvalidOfficeException
    headlines_data = api_request(session, NWS_API_OFFICES + office_id + '/headlines')
    headlines = []
    for headline in headlines_data.get('@graph', {}):
        headlines.append(process_headline_data(headline))
    return headlines


@display_spinner('Getting headline from office...')
def get_office_headline(session: CachedSession, office_id: str, headline_id: str) -> dict:
    if office_id not in VALID_NWS_FORECAST_OFFICES:
        raise InvalidOfficeException
    headline_data = api_request(session, NWS_API_OFFICES + office_id + '/headlines/' + headline_id)
    return process_headline_data(headline_data)


@display_spinner('Getting forecast office details...')
def get_office(session: CachedSession, office_id: str) -> dict:
    if office_id not in VALID_NWS_FORECAST_OFFICES:
        raise InvalidOfficeException
    office_data = api_request(session, NWS_API_OFFICES + office_id)
    return {
        'office_id':            office_data.get('id'),
        'office_name':          office_data.get('name'),
        'street_address':       office_data.get('address', {}).get('streetAddress'),
        'city':                 office_data.get('address', {}).get('addressLocality'),
        'state':                office_data.get('address', {}).get('addressRegion'),
        'zip_code':             office_data.get('address', {}).get('postalCode'),
        'phone_number':         office_data.get('telephone'),
        'fax_number':           office_data.get('faxNumber'),
        'email':                office_data.get('email'),
        'office_url':           office_data.get('sameAs'),
        'office_parent_url':    office_data.get('parentOrganization'),
        'nws_region':           office_data.get('nwsRegion'),
        'counties':             office_data.get('responsibleCounties'),
        'forecast_zones':       office_data.get('responsibleForecastZones'),
        'fire_zones':           office_data.get('responsibleFireZones'),
        'observation_stations': office_data.get('approvedObservationStations'),
    }
