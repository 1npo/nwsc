import os
import json
from datetime import datetime
from pathlib import Path

from loguru import logger


NWS_DATA_EXPIRATION_DATE_FMT = '%a, %d %b %Y %H:%M:%S %Z'
DEFAULT_CACHE_PATH = Path(os.path.expanduser('~')) / '.config/nws/cache.json'


class CacheManager:
    """An abstraction for managing a persistent cache file"""
    def __init__(self, cache_path: str = DEFAULT_CACHE_PATH):
        self.cache = {'locations': {}, 'weather': {}}
        self.cache_path = cache_path
        self.cache_root = Path(cache_path).parent

        if os.path.isfile(self.cache_path):
            self.load_cache()
        else:
            # Initialize an empty cache file for a clean start
            Path(self.cache_root).mkdir(parents=True, exist_ok=True)
            self.save_cache()
    
    def load_cache(self):
        with open(self.cache_path, 'r') as file:
            self.cache = json.load(file)
    
    def save_cache(self):
        with open(self.cache_path, 'w') as file:
            json.dump(self.cache, file)
    
    def get_cached_location(self, address: str) -> tuple | None:
        return self.cache['locations'].get(address)

    def get_cached_weather(self, station: str) -> tuple | None:
        if station not in self.cache['weather']:
            return None
        if self.is_weather_expired(station):
            return None
        return self.cache['weather'][station]

    def add_location_to_cache(self, address: str, location_data: tuple):
        self.cache['locations'].update({address: location_data})
        self.save_cache()
    
    def add_weather_to_cache(self, station: str, weather_data: dict):
        self.cache['weather'].update({station: weather_data})
        self.save_cache()

    def clear_weather_cache(self):
        self.cache['weather'] = {}
        self.save_cache()

    def clear_location_cache(self):
        self.cache['locations'] = {}
        self.save_cache()

    def is_location_cached(self, address: str) -> bool:
        return True if address in self.cache['locations'] else False
    
    def is_weather_cached(self, station: str) -> bool:
        return True if station in self.cache['weather'] else False
    
    def is_weather_expired(self, station: str) -> bool | None:
        if not station:
            return None
        if station not in self.cache['weather']:
            return None
        weather_expiration = self.cache['weather'][station]['expires']
        weather_expiration = datetime.strptime(weather_expiration, NWS_DATA_EXPIRATION_DATE_FMT)
        if weather_expiration <= datetime.now():
            return True
        else:
            return False
