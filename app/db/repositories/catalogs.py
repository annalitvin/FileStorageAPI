from typing import Optional

from core.db import database
from db.errors import EntityDoesNotExist
from schemas.catalogs import CatalogRead, CreateCatalog


def get_query_string(kwargs):
    query_condition = ''
    field_name = list(kwargs.keys())[0]

    match f'{field_name}':
        case 'catalog_id':
            query_condition = f"catalog_id='{kwargs.get('catalog_id')}'"
        case 'catalog_name':
            query_condition = f"catalog_name='{kwargs.get('catalog_name')}'"
        case 'id':
            query_condition = f"id='{kwargs.get('id')}'"

    query = f"SELECT id, catalog_id, catalog_name, source, created_at FROM catalogs WHERE " + query_condition
    return query


class CatalogRepository:

    def __call__(self):
        pass

    async def _get_instance(self, **kwargs):
        query_string = get_query_string(kwargs)
        data = await database.fetch_one(query_string)
        return data

    @database.transaction()
    async def create(self, catalog: CreateCatalog):
        values = {
            "catalog_id": catalog.catalog_id,
            "catalog_name": catalog.catalog_name,
            "source": catalog.source,
            "created_at": catalog.created_at
        }
        query = (
            "INSERT INTO catalogs(catalog_id, catalog_name, source, created_at) VALUES (:catalog_id, :catalog_name, :source, :created_at)"
        )
        await database.execute(query=query, values=values)
        catalog_instance = await self.get(catalog_id=catalog.catalog_id)
        return catalog_instance

    async def get(self, **kwargs) -> Optional[CatalogRead]:
        db_catalog = await self._get_instance(**kwargs)

        if db_catalog is None:
            raise EntityDoesNotExist

        return CatalogRead(**db_catalog)
