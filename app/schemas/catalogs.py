from datetime import datetime
from uuid import UUID
from pydantic import BaseModel


class CreateCatalog(BaseModel):
    catalog_id: UUID
    catalog_name: str
    source: str
    created_at: datetime


class CatalogRead(BaseModel):
    id: int
    catalog_id: UUID
    catalog_name: str
    source: str
    created_at: datetime
