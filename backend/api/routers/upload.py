from fastapi import APIRouter, UploadFile, File, BackgroundTasks, Depends

from services.vector_store_service import VectorStoreService
from api.dependencies import get_vector_store_service
from utils.utils_for_upload import process_pdf


router = APIRouter(prefix="/upload")

@router.post("/pdf")
async def upload_pdf(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    vector_store_service: VectorStoreService = Depends(get_vector_store_service)
):
    background_tasks.add_task(
        process_pdf,
        file,
        vector_store_service
    )

    return {"message": "PDF принят, обработка начата"}