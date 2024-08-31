
from datetime import datetime
from dataclasses import dataclass


@dataclass
class ProductType:
    code: str
    name: str
    id: int = None # repository item id


@dataclass
class ProductLocation:
    code: str
    name: str
    id: int = None # repository item id


@dataclass
class Product:
    product_id: str
    wmo_id: str
    name: str
    code: str
    text: str
    issuing_office: str
    issued_at: datetime
    id: int = None # repository item id
