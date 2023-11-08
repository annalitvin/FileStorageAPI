from abc import ABC, abstractmethod


class StorageManager(ABC):

    @abstractmethod
    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    async def create(self):
        pass

    @abstractmethod
    async def remove(self):
        pass
