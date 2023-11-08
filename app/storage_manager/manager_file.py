import os

import aiofiles
import aiofiles.os
import psutil

from .errors import FileNotFound
from .manager_abstract import StorageManager

process = psutil.Process(os.getpid())
memory_limit = process.memory_info().rss


async def read_in_chunks(file_object, chunk_size=memory_limit):
    """Lazy function (generator) to read a file piece by piece.
    Default chunk size: 1k."""
    while True:
        data = await file_object.read(chunk_size)
        if not data:
            break
        yield data


class FileStorage(StorageManager):

    def __init__(self, file_obj, file_path):
        self.file_path = file_path
        self.file_obj = file_obj

    async def create(self):
        content = read_in_chunks(self.file_obj)
        async with aiofiles.open(os.path.join(self.file_path, self.file_obj.filename), 'wb') as f:
            async for piece in content:
                await f.write(piece)

    async def remove(self):
        try:
            await aiofiles.os.remove(
                os.path.join(self.file_path, self.file_obj.filename)
            )
        except Exception:
            raise FileNotFound
