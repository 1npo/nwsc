from requests_cache import CachedSession
from nwsc.render.decorators import display_spinner
from nwsc.api.api_request import api_request
from nwsc.api import NWS_API_GLOSSARY


@display_spinner('Getting glossary...')
def get_glossary(session: CachedSession) -> dict:
	"""Get the glossary of weather terms"""
	glossary_data = api_request(session, NWS_API_GLOSSARY)
	glossary = {}
	for entry in glossary_data.get('glossary', {}):
		term = entry.get('term')
		definition = entry.get('definition')
		if term and definition:
			glossary.update({term: definition})
	return glossary
