from fastapi import HTTPException, Depends
from fastapi import status

from db.errors import EntityDoesNotExist
from db.repositories.catalogs import CatalogRepository
from db.repositories.files import FileRepository
from . import router
from routers.files.constants import (
    CATALOG_NOT_EXISTS_ERROR_MSG
)


@router.get(
    '/top',
    status_code=status.HTTP_200_OK,
    name='top_largest_files'
)
async def top_largest_files(
        file_repository: FileRepository = Depends(FileRepository)
):
    return await file_repository.get_top_largest_list()


@router.get(
    path='/top/{dir_name}',
    status_code=status.HTTP_200_OK,
    name='top_largest_files'
)
async def top_largest_files(
        dir_name: str,
        file_repository: FileRepository = Depends(FileRepository),
        catalog_repository: CatalogRepository = Depends(CatalogRepository)
):
    try:
        await catalog_repository.get(catalog_name=dir_name)
        return await file_repository.get_top_largest_list(dir_name=dir_name)
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=CATALOG_NOT_EXISTS_ERROR_MSG
        )
