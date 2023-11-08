from uuid import uuid4
from datetime import datetime
from typing import Optional

from fastapi import UploadFile

from db.errors import EntityDoesNotExist
from schemas.files import FileRead
from core.db import database


def get_query_string(kwargs):
    query_condition = ''
    field_name = list(kwargs.keys())[0]

    match f'{field_name}':
        case 'file_id':
            query_condition = f"file_id='{kwargs.get('file_id')}'"
        case 'filename':
            query_condition = f"file_name='{kwargs.get('filename')}'"

    query = (f"SELECT id, file_id, catalog_id, file_name, content_type, file_size, created_at "
             f"FROM files WHERE " + query_condition)
    return query


class FileRepository:

    def __call__(self):
        pass

    async def _get_instance(self, **kwargs):
        query_string = get_query_string(kwargs)
        data = await database.fetch_one(query_string)
        return data

    @database.transaction()
    async def create(self, file: UploadFile, catalog_db) -> Optional[FileRead]:
        created_at = datetime.today()
        file_id = str(uuid4())
        values = {
            "file_id": file_id,
            "catalog_id": catalog_db.id,
            "file_name": file.filename,
            "file_size": file.size,
            "content_type": file.content_type,
            "created_at": created_at
        }
        query = ("INSERT INTO files(file_id, catalog_id, file_name, file_size, content_type, created_at) "
                 "VALUES (:file_id, :catalog_id, :file_name, :file_size, :content_type, :created_at)")
        await database.execute(query=query, values=values)
        file_instance = await self.get(filename=file.filename)
        return file_instance

    async def get(self, **kwargs) -> Optional[FileRead]:
        db_file = await self._get_instance(**kwargs)

        if db_file is None:
            raise EntityDoesNotExist

        return FileRead(**db_file)

    async def update(self, file_name) -> Optional[FileRead]:
        updated_at = datetime.today()
        values = {
            "updated_at": updated_at,
            "file_name": file_name
        }
        query = "UPDATE files SET updated_at = :updated_at WHERE file_name = :file_name"
        await database.execute(query=query, values=values)
        file_instance = await self.get(filename=file_name)
        return file_instance

    async def get_top_largest_list(
            self, dir_name: str = None, limit: int = 10, offset: int = 0
    ) -> list[FileRead]:
        query = ("SELECT id, file_id, catalog_id, file_name, content_type, file_size "
                 "FROM public.get_full_info_about_top_largest_file(:limit, :offset, :dir_name)")
        results = await database.fetch_all(
            query=query,
            values=dict(limit=limit, offset=offset, dir_name=dir_name)
        )
        return [FileRead(**file) for file in results]
