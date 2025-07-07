from fastapi import APIRouter, HTTPException
from models.background_removal import RemoveBgRequest, RemoveBgResponse
from services.background_removal_service import remove_background_from_url

router = APIRouter()

@router.post("/logo/remove-bg", response_model=RemoveBgResponse)
async def remove_background(request: RemoveBgRequest):
    """Remove the background from a logo image and upload it to Google Cloud Storage."""
    try:
        result = await remove_background_from_url(request.image_url)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
