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
    if not file.filename.lower().endswith(".pdf"):
        print(f"Файл должен быть .pdf формата")
        return

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

async def process_zip(
    file: UploadFile = File(...),
    vector_store_service: VectorStoreService = Depends(get_vector_store_service)
) -> None:
    if not file.filename.lower().endswith(".zip"):
        print("Файл должен быть .zip формата")
        return

    with tempfile.NamedTemporaryFile(delete=False, suffix=".zip") as tmp:
        content = await file.read()
        tmp.write(content)
        tmp.flush()
        zip_path = tmp.name

    validate_result, valid_pdfs, extract_temp_dir = vector_store_service.validate_zip_by_path(zip_path)

    if validate_result:
        for valid_pdf in valid_pdfs:
            vector_store_service.add_pdf_document_by_path(valid_pdf)

            destination = Path(settings.DOCUMENTS_DIRECTORY) / os.path.basename(valid_pdf)
            shutil.move(valid_pdf, destination)

    if os.path.exists(zip_path):
        os.unlink(zip_path)

    shutil.rmtree(extract_temp_dir, ignore_errors=True)