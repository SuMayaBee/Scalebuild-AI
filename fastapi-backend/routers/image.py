from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.image_service import generate_and_upload_image

router = APIRouter()

class ImagePrompt(BaseModel):
    prompt: str

@router.post("/generate-image")
async def create_image(image_prompt: ImagePrompt):
    try:
        image_url = generate_and_upload_image(image_prompt.prompt)
        return {"url": image_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
