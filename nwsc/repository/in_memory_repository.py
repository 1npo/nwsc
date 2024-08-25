from nwsc.repository.base_repository import IRepository


class InMemoryRepository(IRepository):
    def __init__(self):
        self._repository = []

    def get_all(self) -> list:
        return self._repository

    def get_by_id(
        self,
        id: int
    ) -> dict:
        return next((item for item in self._repository if item.get('id') == id), None)
    
    def get_by_filter(
        self,
        filter: dict
    ) -> list:
        if len(filter) == 1:
            key = list(filter.keys())[0]
            value = list(filter.values())[0]
            return [next((item for item in self._repository if item.get(key) == value), None)]
        else:
            records = []
            for key, value in filter.items():
                records.append(next((item for item in self._repository if item.get(key) == value), None))
            return records
    
    def create(
        self,
        item: dict
    ) -> dict:
        item.get('id') = len(self._repository) + 1
        self._repository.append(item)
        return item
    
    def update(
        self,
        item: dict
    ) -> bool:
        index = next((i for i, obj in enumerate(self._repository) if obj.get('id') == item.get('id')), None)
        if index is not None:
            self._repository[index] = item
            return True
    
        return False
    
    def delete(
        self,
        id
    ) -> bool:
        index = next((i for i, obj in enumerate(self._repository) if obj.get('id') == id), None)
        if index is not None:
            self._repository.pop(index)
            return True
        return False