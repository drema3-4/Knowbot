from tempfile import TemporaryDirectory
from fastapi import APIRouter, BackgroundTasks, UploadFile, File, Depends, HTTPException
import shutil
import os
import zipfile
from pathlib import Path
import tempfile

from services.vector_store_service import VectorStoreService
from api.dependencies import get_vector_store_service
from utils.zip_and_pdf_validators import is_valid_pdf
from core.config import settings
from api.routers.upload import process_pdf


router = APIRouter(prefix="/upload")

@router.post("/zip")
async def upload_zip(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    vector_store_service: VectorStoreService = Depends(get_vector_store_service)
):
    if not file.filename.lower().endswith(".zip"):
        raise HTTPException(400, "Файл должен иметь расширение .zip")
    
    zip_tmp = await save_upload_file_tmp(file, suffix=".zip")
    extract_dir = tempfile.mkdtemp(prefix="knowbot_extract_")

    background_tasks.add_task(
        process_zip_file,
        zip_tmp,
        extract_dir,
        vector_store_service
    )

    return {"message": "ZIP-архив принят, обработка начата"}

async def save_upload_file_tmp(upload_file: UploadFile, suffix: str = None) -> Path:
    """Сохраняет загруженный файл во временный файл и возвращает путь."""
    if suffix is None:
        suffix = Path(upload_file.filename).suffix
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        shutil.copyfileobj(upload_file.file, tmp)
        tmp_path = Path(tmp.name)
    return tmp_path

def process_zip_file(zip_path: Path, extract_dir: str, vector_store_service: VectorStoreService):
    try:
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(extract_dir)
        process_extracted_folder(extract_dir, vector_store_service)
    
    except Exception as e:
        print(f"Ошибка обработки zip: {e}")
    
    finally:
        if zip_path.exists():
            os.unlink(zip_path)
        if os.path.exists(extract_dir):
            shutil.rmtree(extract_dir)
            print(f"Временная папка {extract_dir} удалена")

def process_extracted_folder(folder_path: str, vector_store_service: VectorStoreService):
    print("Обработка началась")
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            print(f"Обрабатываем файл '{file}'")
            if file.lower().endswith(".pdf"):
                pdf_path = os.path.join(root, file)

                if not is_valid_pdf(pdf_path):
                    print(f"Файл {pdf_path} не является корректным PDF, пропускаем")
                    continue

                try:
                    vector_store_service.add_pdf_document_by_path(pdf_path)
                
                except Exception as e:
                    print(f"Ошибка при добавлении PDF {file}: {e}")


    print("Обработка завершена")