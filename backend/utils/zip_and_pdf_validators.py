from pathlib import Path
from fastapi import UploadFile, HTTPException
from tempfile import NamedTemporaryFile
import shutil
import os
import PyPDF2

def validate_pdf(file: UploadFile) -> Path:
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(400, "Файл должен иметь расширение .pdf")
    
    suffix = Path(file.filename).suffix
    with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = Path(tmp.name)

    if tmp_path.stat().st_size == 0:
        os.unlink(tmp_path)
        raise HTTPException(400, "Файл пуст")
    
    return tmp_path

def is_valid_pdf(file_path: str) -> bool:
    """Проверяет, что файл существует, не пуст и может быть открыт как PDF."""
    if not os.path.exists(file_path):
        return False
    if os.path.getsize(file_path) == 0:
        return False
    try:
        # Попытка открыть PDF
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            # Можно проверить, что есть хотя бы одна страница
            if len(reader.pages) == 0:
                return False
        return True
    except Exception:
        return False