from openai import OpenAI
import base64
from services.storage_service import upload_to_gcs
import io
import os
from typing import Optional, Dict, Any
import asyncio
from datetime import datetime

client = OpenAI()

class PresentationImageService:
    """Enhanced image service for presentations with DALL-E and GCS storage"""
    
    def __init__(self):
        self.client = OpenAI()
    
    async def generate_presentation_image(
        self, 
        prompt: str, 
        size: str = "1024x1024",
        quality: str = "standard"
    ) -> Dict[str, Any]:
        """
        Generate image using DALL-E 3 for presentations
        Returns both the GCS URL and metadata
        """
        try:
            # Run the sync OpenAI call in a thread pool
            response = await asyncio.to_thread(
                self.client.images.generate,
                model="dall-e-3",
                prompt=prompt,
                size=size,
                quality=quality,
                n=1,
                response_format="b64_json"
            )

            if response.data and response.data[0].b64_json:
                image_data = base64.b64decode(response.data[0].b64_json)
                
                # Create descriptive filename
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                safe_prompt = prompt[:30].replace(' ', '_').replace('/', '_').replace('\\', '_')
                file_name = f"presentation_images/{safe_prompt}_{timestamp}.png"
                
                file_obj = io.BytesIO(image_data)
                bucket_name = os.getenv("GCS_BUCKET_NAME")
                
                if not bucket_name:
                    raise Exception("GCS_BUCKET_NAME is not set")

                # Upload to GCS
                public_url = await asyncio.to_thread(
                    upload_to_gcs, 
                    file_obj, 
                    file_name, 
                    "image/png", 
                    bucket_name
                )
                
                return {
                    "url": public_url,
                    "prompt": prompt,
                    "model": "dall-e-3",
                    "size": size,
                    "quality": quality,
                    "filename": file_name,
                    "success": True
                }
            else:
                raise Exception("Failed to generate image or no image data returned.")

        except Exception as e:
            print(f"Error generating presentation image: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def generate_slide_image(
        self, 
        prompt: str, 
        context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate image specifically optimized for slide content
        """
        # Enhance prompt for better slide imagery
        enhanced_prompt = f"Professional, high-quality image for a presentation slide: {prompt}"
        if context:
            enhanced_prompt = f"{enhanced_prompt}. Context: {context}"
        
        # Use landscape orientation for slides
        return await self.generate_presentation_image(
            enhanced_prompt, 
            size="1792x1024",  # Landscape format for slides
            quality="hd"
        )

# Global service instance
presentation_image_service = PresentationImageService()

# Keep backward compatibility
def generate_and_upload_image(prompt: str):
    """Backward compatible function for existing code"""
    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
            response_format="b64_json"
        )

        if response.data and response.data[0].b64_json:
            image_data = base64.b64decode(response.data[0].b64_json)
            
            file_name = f"{prompt[:50].replace(' ', '_')}.png"
            file_obj = io.BytesIO(image_data)

            bucket_name = os.getenv("GCS_BUCKET_NAME")
            if not bucket_name:
                raise Exception("GCS_BUCKET_NAME is not set")

            # Pass the file-like object and metadata directly
            public_url = upload_to_gcs(file_obj, file_name, "image/png", bucket_name)
            return public_url
        else:
            raise Exception("Failed to generate image or no image data returned.")

    except Exception as e:
        print(f"An error occurred: {e}")
        raise e
