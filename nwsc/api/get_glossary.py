from requests_cache import CachedSession
from nwsc.decorators import display_spinner
from nwsc.api.api_request import api_request
from nwsc.api import API_URL_NWS_GLOSSARY


@display_spinner('Getting glossary...')
def get_glossary_data(session: CachedSession) -> dict:
	"""Get the glossary of weather terms"""
	glossary_data = api_request(session, API_URL_NWS_GLOSSARY)
	glossary = {}
	for entry in glossary_data['glossary']:
		term = entry.get('term')
		definition = entry.get('definition')
		if term and definition:
			glossary.update({term: definition})
	return glossary
