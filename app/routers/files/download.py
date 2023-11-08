import os

from uuid import UUID

from fastapi import HTTPException, Depends
from fastapi.responses import FileResponse
from fastapi import status

from db.errors import EntityDoesNotExist
from db.repositories.catalogs import CatalogRepository
from db.repositories.files import FileRepository
from . import router
from routers.files.constants import FILE_NOT_EXISTS_ERROR_MSG


@router.get(
    '/files/{id}',
    status_code=status.HTTP_200_OK,
    name='download_file'
)
async def download_file(
        id: UUID,
        file_repository: FileRepository = Depends(FileRepository),
        catalog_repository: CatalogRepository = Depends(CatalogRepository)
):
    try:
        file = await file_repository.get(file_id=id)
        catalog = await catalog_repository.get(id=file.catalog_id)
        return FileResponse(
            path=os.path.join(
                catalog.source, file.file_name
            ),
            media_type=file.content_type,
            filename=file.file_name
        )
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=FILE_NOT_EXISTS_ERROR_MSG
        )


@router.head(
    '/files/{id}',
    status_code=status.HTTP_200_OK,
    name='retrieve_file_metadata'
)
async def retrieve_file_metadata(
        id: UUID,
        file_repository: FileRepository = Depends(FileRepository),
        catalog_repository: CatalogRepository = Depends(CatalogRepository)
):
    try:
        file = await file_repository.get(file_id=id)
        catalog = await catalog_repository.get(id=file.catalog_id)
        return FileResponse(
            path=os.path.join(
                catalog.source, file.file_name
            ),
            media_type=file.content_type,
            filename=file.file_name
        )
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=FILE_NOT_EXISTS_ERROR_MSG
        )
