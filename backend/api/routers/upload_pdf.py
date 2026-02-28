import os
import shutil
from pathlib import Path
from tempfile import NamedTemporaryFile
from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks, Depends

from services.vector_store_service import VectorStoreService
from utils.zip_and_pdf_validators import validate_pdf
from core.config import settings
from api.dependencies import get_vector_store_service


router = APIRouter(prefix="/upload")

@router.post("/pdf")
async def upload_pdf(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    vector_store_service: VectorStoreService = Depends(get_vector_store_service)
):

    tmp_path = validate_pdf(file)

    original_filename = os.path.basename(file.filename)
    target_path = Path(settings.DOCUMENTS_DIRECTORY) / original_filename

    target_path.parent.mkdir(parents=True, exist_ok=True)

    if target_path.exists():
        os.unlink(tmp_path)
        raise HTTPException(400, f"Файл с именем '{original_filename}' уже есть в хранилище")
    
    shutil.move(str(tmp_path), str(target_path))
    
    background_tasks.add_task(
        process_pdf,
        target_path,
        vector_store_service
    )

    return {"message": "PDF принят, обработка начата"}

def process_pdf(pdf_path: Path, vector_store_service: VectorStoreService):
    try:
        vector_store_service.add_pdf_document_by_path(str(pdf_path))

        print(f"Файл {pdf_path} успешно обработан")

    except Exception as e:
        print(f"Ошибка при обработке файла {pdf_path}: {e}")