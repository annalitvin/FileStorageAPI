import aiofiles.os

from pathlib import Path

from .errors import CatalogNotFoundError
from .manager_abstract import StorageManager


class CatalogStorage(StorageManager):

    def __init__(self, file_path):
        self.file_path = file_path

    async def create(self):
        await aiofiles.os.mkdir(self.file_path)

    async def remove(self):
        try:
            await aiofiles.os.rmdir(self.file_path)
        except Exception:
            raise CatalogNotFoundError

    async def is_empty(self):
        if await aiofiles.os.path.isdir(self.file_path):
            if not await aiofiles.os.listdir(self.file_path):
                return True
            return False
        else:
            raise CatalogNotFoundError

    def is_exists(self):
        return Path(self.file_path).exists()
