from abc import ABC, abstractmethod

class Repository(ABC):

    @abstractmethod
    def add(self, obj):
        pass

    @abstractmethod
    def get(self, obj_id):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def update(self, obj_id, obj):
        pass

    @abstractmethod
    def delete(self, obj_id):
        pass

    @abstractmethod
    def get_by_attribute(self, att_name, att_value):
        pass

class MemoryRepository(Repository):
    def __init__(self):
        self._storage = {}

    def add(self, obj):
        self._storage[obj.id] = obj

    def get(self, obj_id):
        return self._storage.get(obj_id)

    def get_all(self):
        return list(self._storage.values())

    def update(self, obj_id, obj):
        object = self._storage[obj_id]
        if object:
            object.update(obj)
        return self._storage[obj_id]

    def delete(self, obj_id):
        deleted_item = self._storage.get(obj_id)
        if deleted_item:
            del self._storage[obj_id]
        return deleted_item

    def get_by_attribute(self, att_name, att_value):
        return next((obj for obj in self._storage.values() if getattr(obj, att_name) == att_value), None)