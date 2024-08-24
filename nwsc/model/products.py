
from datetime import datetime
from dataclasses import dataclass


@dataclass
class ProductType:
    code: str
    name: str


@dataclass
class ProductLocation:
    code: str
    name: str


@dataclass
class Product:
    id: str
    wmo_id: str
    type: ProductType
    text: str
    issuing_office: str
    issued_at: datetime

