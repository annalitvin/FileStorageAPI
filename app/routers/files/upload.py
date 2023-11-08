import os.path
import traceback

from datetime import datetime
from uuid import uuid4

from fastapi import HTTPException, Response, Request
from fastapi import UploadFile, status
from fastapi import Depends

from core.db import database
from core.config import settings
from db.errors import EntityDoesNotExist
from db.repositories.catalogs import CatalogRepository
from db.repositories.files import FileRepository
from storage_manager.manager_catalog import CatalogStorage
from storage_manager.manager_file import FileStorage
from . import router
from schemas.catalogs import CreateCatalog
from routers.files.constants import (
    CATALOG_NOT_EXISTS_ERROR_MSG,
    FILE_NOT_EXISTS_ERROR_MSG
)

MEDIA_ROOT_DIR = settings.media_root_dir
ROOT_CATALOG_ID = settings.root_catalog_id


@router.post(
    "/files/{dir_name}",
    status_code=status.HTTP_201_CREATED,
    name="create_upload_file"
)
async def create_upload_file(
        request: Request,
        response: Response,
        dir_name: str,
        file: UploadFile,
        file_repository: FileRepository = Depends(FileRepository),
        catalog_repository: CatalogRepository = Depends(CatalogRepository)
):
    try:
        async with database.transaction():
            file_db = await file_repository.get(filename=file.filename)
            await file_repository.update(file.filename)
    except EntityDoesNotExist:
        file_path = os.path.join(MEDIA_ROOT_DIR, dir_name)

        file_storage = FileStorage(file, file_path)
        catalog_storage = CatalogStorage(file_path)

        if catalog_storage.is_exists():
            catalog_db = await catalog_repository.get(catalog_name=dir_name)
        else:
            await catalog_storage.create()
            try:
                catalog = CreateCatalog(
                    catalog_id=str(uuid4()),
                    catalog_name=dir_name,
                    source=file_path,
                    created_at=datetime.today()
                )
                catalog_db = await catalog_repository.create(catalog)
            except Exception:
                traceback.print_exc()
                await catalog_storage.remove()
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=CATALOG_NOT_EXISTS_ERROR_MSG
                )

        try:
            await file_storage.create()
            file_db = await file_repository.create(file, catalog_db)
        except Exception:
            traceback.print_exc()
            await file_storage.remove()
            if await catalog_storage.is_empty():
                await catalog_storage.remove()
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=FILE_NOT_EXISTS_ERROR_MSG
            )
    file_download_url = request.url_for("download_file", id=f"{file_db.file_id}")
    response.headers["Location"] = file_download_url.path
    return {'message': f'Successfuly uploaded {file_db.file_id}'}


@router.post(
    "/files",
    status_code=status.HTTP_201_CREATED,
    name="create_upload_rfile"
)
async def create_upload_rfile(
        request: Request,
        response: Response,
        file: UploadFile,
        file_repository: FileRepository = Depends(FileRepository),
        catalog_repository: CatalogRepository = Depends(CatalogRepository),
):
    try:
        async with database.transaction():
            file_db = await file_repository.get(filename=file.filename)
            await file_repository.update(file.filename)
    except EntityDoesNotExist:
        file_storage = FileStorage(file, MEDIA_ROOT_DIR)

        await file_storage.create()
        try:
            async with database.transaction():
                catalog_db = await catalog_repository.get(catalog_id=ROOT_CATALOG_ID)
                file_db = await file_repository.create(file, catalog_db)
        except Exception:
            traceback.print_exc()
            await file_storage.remove()
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=FILE_NOT_EXISTS_ERROR_MSG
            )
    file_download_url = request.url_for("download_file", id=f"{file_db.file_id}")
    response.headers["Location"] = file_download_url.path
    return {'message': f'Successfuly uploaded {file_db.file_id}'}
