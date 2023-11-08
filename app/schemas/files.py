from datetime import datetime
from uuid import UUID
from pydantic import BaseModel


class FileRead(BaseModel):
    id: int
    file_id: UUID
    catalog_id: int
    file_name: str
    content_type: str
    file_size: int
