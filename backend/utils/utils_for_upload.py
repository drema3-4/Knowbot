from fastapi import UploadFile, File, Depends
import tempfile
import os
from pathlib import Path
import shutil

from services.vector_store_service import VectorStoreService
from api.dependencies import get_vector_store_service
from core.config import settings


async def process_pdf(
    file: UploadFile = File(...),
    vector_store_service: VectorStoreService = Depends(get_vector_store_service)
    ) -> None:
    """Обрабатывает pdf из запроса: вроверяет, сохраняет на диск, добавляет в векторную БД."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        content = await file.read()
        tmp.write(content)
        tmp.flush()
        tmp_path = tmp.name

    if vector_store_service.validate_pdf_by_path(tmp_path):
        vector_store_service.add_pdf_document_by_path(tmp_path)

        destination = Path(settings.DOCUMENTS_DIRECTORY) / file.filename
        shutil.move(tmp_path, destination)
    
    else:
        os.unlink(tmp_path)