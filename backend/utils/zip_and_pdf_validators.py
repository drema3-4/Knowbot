from pathlib import Path
from fastapi import UploadFile, HTTPException
from tempfile import NamedTemporaryFile
import shutil
import os

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