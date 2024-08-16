
from datetime import datetime
from dataclasses import dataclass


@dataclass
class ProductType:
    product_code: str
    product_name: str


@dataclass
class ProductLocation:
    location_code: str
    location_name: str


@dataclass
class Product:
    product_id: str
    product_wmo_id: str
    issuing_office: str
    product_type: ProductType
    product_text: str

