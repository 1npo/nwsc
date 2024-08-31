from typing import List
from nwsc.repository.base import BaseRepository
from nwsc.model import NWSItem


class InMemoryRepository(BaseRepository):
    def __init__(self):
        self._repository = []

    def get_all(self) -> list:
        return self._repository

    def get(self, id: int) -> dict:
        return next((obj for obj in self._repository if obj.get('id') == id), None)
    
    def filter_by(self, filter: dict) -> List[NWSItem]:
        if len(filter) == 1:
            key = list(filter.keys())[0]
            value = list(filter.values())[0]
            return [next((obj for obj in self._repository if obj.get(key) == value), None)]
        else:
            items = []
            for key, value in filter.items():
                items.append(next((obj for obj in self._repository if obj.get(key) == value), None))
            return items
    
    def create(self, item: NWSItem) -> NWSItem:
        item.id = len(self._repository) + 1
        self._repository.append(item)
        return item
    
    def update(self, item: NWSItem) -> bool:
        index = next((i for i, obj in enumerate(self._repository) if obj.get('id') == item.id), None)
        if index is not None:
            self._repository[index] = item
            return True
        return False
    
    def delete(self, item: NWSItem) -> bool:
        index = next((i for i, obj in enumerate(self._repository) if obj.get('id') == item.id), None)
        if index is not None:
            self._repository.pop(index)
            return True
        return False
    
    def serialize(self, item):
        raise NotImplementedError
    
    def deserialize(self, data):
        raise NotImplementedError
