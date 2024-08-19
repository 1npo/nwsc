from requests_cache import CachedSession
from loguru import logger
from nwsc.render.decorators import display_spinner
from nwsc.api.api_request import api_request
from nwsc.api import (
	NWS_API_PRODUCT_TYPES,
	NWS_API_PRODUCT_LOCATIONS,
	NWS_API_PRODUCTS,
)


def process_product_data(products_data: dict) -> list:
	products = []
	for product in products_data:
		products.append({
			'product_id':		product.get('id'),
			'product_wmo_id':	product.get('wmoCollectiveId'),
			'issuing_office':	product.get('issuingOffice'),
			'issued_at':		product.get('issuanceTime'),
			'product_code':		product.get('productCode'),
			'product_name':		product.get('productName'),
		})
	return products


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
	product_types_data = api_request(session, NWS_API_PRODUCT_TYPES)
	return process_product_types_data(product_types_data)


@display_spinner('Getting product types available from the issuing location...')
def get_product_types_by_location(session: CachedSession, location_id: str) -> list:
	product_types_data = api_request(session, NWS_API_PRODUCT_LOCATIONS + f'/{location_id}/types')
	return process_product_types_data(product_types_data)


@display_spinner('Getting all product issuing locations...')
def get_product_locations(session: CachedSession) -> list:
	product_locations_data = api_request(session, NWS_API_PRODUCT_LOCATIONS)
	return process_product_locations_data(product_locations_data)


@display_spinner('Getting product issuing locations by type...')
def get_product_locations_by_type(session: CachedSession, type_id: str) -> list:
	product_locations_data = api_request(session, NWS_API_PRODUCT_TYPES + f'/{type_id}/locations')
	return process_product_locations_data(product_locations_data)


@display_spinner('Getting listing of all products...')
def get_products(session: CachedSession) -> list:
	products_data = api_request(session, NWS_API_PRODUCTS)
	return process_product_data(products_data.get('@graph', {}))


@display_spinner('Getting listing of all products by type...')
def get_products_by_type(session: CachedSession, type_id: str) -> list:
	products_data = api_request(session, NWS_API_PRODUCT_TYPES + f'/{type_id}')
	return process_product_data(products_data.get('@graph', {}))


@display_spinner('Getting listing of all products by type from the issuing location...')
def get_products_by_type_and_location(session: CachedSession, type_id: str, location_id: str):
	products_data = api_request(session, NWS_API_PRODUCT_TYPES + f'/{type_id}/locations/{location_id}')
	return process_product_data(products_data.get('@graph', {}))


@display_spinner('Getting product content...')
def get_product(session: CachedSession, product_id: str) -> dict:
	""" """
	product_data = api_request(session, NWS_API_PRODUCTS + product_id)
	product = process_product_data([product_data])[0]
	product.update({'product_text': product_data.get('productText')})
	return product

