import os
from fastapi import APIRouter, UploadFile, File, HTTPException
from services import storage_service

router = APIRouter()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Uploads a file to Google Cloud Storage.
    """
    bucket_name = os.getenv("GCS_BUCKET_NAME")
    if not bucket_name:
        raise HTTPException(status_code=500, detail="GCS_BUCKET_NAME environment variable not set.")

    try:
        file_url = storage_service.upload_to_gcs(file, bucket_name)
        return {"filename": file.filename, "url": file_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
