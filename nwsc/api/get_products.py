from requests_cache import CachedSession
from loguru import logger
from nwsc.render.decorators import display_spinner
from nwsc.api.api_request import api_request
from nwsc.api import (
	API_URL_NWS_PRODUCT_TYPES,
	API_URL_NWS_PRODUCT_LOCATIONS,
	API_URL_NWS_PRODUCTS,
)


"""
example type: RR2
example location: APX

- [x] /products - get full product listing
- [x] /products/locations - get all locations
- [x] /products/types - get all types
- [x] /products/{productId} - get product
- [x] /products/types/{typeId} - get listing by type
- [x] /products/types/{typeId}/locations - get locations by type
- [x] /products/locations/{locationId}/types - get types by location
- [x] /products/types/{typeId}/locations/{locationId} - get listing by type and location
"""


def process_product_listing_data(product_listing_data: dict) -> list:
	product_listing = []
	for listing in product_listing_data.get('@graph', {}):
		product_listing.append({
			'product_id':		listing.get('id'),
			'product_wmo_id':	listing.get('wmoCollectiveId'),
			'issuing_office':	listing.get('issuingOffice'),
			'issued_at':		listing.get('issuanceTime'),
			'product_code':		listing.get('productCode'),
			'product_name':		listing.get('productName'),
		})
	return product_listing


def process_product_types_data(product_types_data: list) -> list:
	product_types = []
	for product_type in product_types_data.get('@graph', {}):
		product_types.append({
			'product_code':	product_type.get('productCode'),
			'product_name': product_type.get('productName'),
		})
	return product_types


def process_product_locations_data(product_locations_data: dict) -> list:
	product_locations = []
	product_locations_data = product_locations_data.get('locations', {})
	if product_locations_data and isinstance(product_locations_data, dict):
		for location, code in product_locations_data.items():
			product_locations.append({
				'location_code': location,
				'location_name': code,
			})
		return product_locations
	return []


# See: https://www.weather.gov/mlb/text
@display_spinner('Getting all product types...')
def get_product_types(session: CachedSession) -> list:
	product_types_data = api_request(session, API_URL_NWS_PRODUCT_TYPES)
	return process_product_types_data(product_types_data)


@display_spinner('Getting product types available from the issuing location...')
def get_product_types_by_location(session: CachedSession, location_id: str) -> list:
	product_types_data = api_request(session, API_URL_NWS_PRODUCT_LOCATIONS + f'/{location_id}/types')
	return process_product_types_data(product_types_data)


@display_spinner('Getting all product issuing locations...')
def get_product_locations(session: CachedSession) -> list:
	product_locations_data = api_request(session, API_URL_NWS_PRODUCT_LOCATIONS)
	return process_product_locations_data(product_locations_data)


@display_spinner('Getting product issuing locations by type...')
def get_product_locations_by_type(session: CachedSession, type_id: str) -> list:
	product_locations_data = api_request(session, API_URL_NWS_PRODUCT_TYPES + f'/{type_id}/locations')
	logger.debug(f'{type_id=}, URL={API_URL_NWS_PRODUCT_TYPES}/{type_id}/locations')
	logger.debug(product_locations_data)
	return process_product_locations_data(product_locations_data)


@display_spinner('Getting listing of all products...')
def get_product_listing(session: CachedSession) -> list:
	product_listing_data = api_request(session, API_URL_NWS_PRODUCTS)
	return process_product_listing_data(product_listing_data)


@display_spinner('Getting listing of all products by type...')
def get_product_listing_by_type(session: CachedSession, type_id: str) -> list:
	product_listing_data = api_request(session, API_URL_NWS_PRODUCT_TYPES + f'/{type_id}')
	return process_product_listing_data(product_listing_data)


@display_spinner('Getting listing of all products by type from the issuing location...')
def get_product_listing_by_type_and_location(session: CachedSession, type_id: str, location_id: str):
	product_listing_data = api_request(session, API_URL_NWS_PRODUCT_TYPES + f'/{type_id}/locations/{location_id}')
	return process_product_listing_data(product_listing_data)


@display_spinner('Getting product content...')
def get_product(session: CachedSession, product_id: str) -> dict:
	""" """
	product_data = api_request(session, API_URL_NWS_PRODUCTS + product_id)
	return {
		'product_id':		product_data.get('id'),
		'product_wmo_id':	product_data.get('wmoCollectiveId'),
		'issuing_office':	product_data.get('issuingOffice'),
		'issued_at':		product_data.get('issuanceTime'),
		'product_code':		product_data.get('productCode'),
		'product_name':		product_data.get('productName'),
		'product_text':		product_data.get('productText'),
	}

