"""
Enhanced Image Generation Service for Presentations
Replaces Together AI with DALL-E and UploadThing with Google Cloud Storage
"""
import os
import base64
import io
from typing import Optional
from openai import OpenAI
from services.storage_service import upload_to_gcs
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class EnhancedImageService:
    """Enhanced image generation service using DALL-E and GCS"""
    
    def __init__(self):
        self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.gcs_bucket = os.getenv("GCS_BUCKET_NAME", "deck123")
    
    async def generate_presentation_image(
        self, 
        prompt: str, 
        model: str = "dall-e-3",
        size: str = "1024x1024",
        quality: str = "standard"
    ) -> str:
        """
        Generate image using DALL-E and upload to Google Cloud Storage
        
        Args:
            prompt: Text description for image generation
            model: DALL-E model to use (dall-e-3 or dall-e-2)
            size: Image dimensions (1024x1024, 1024x1792, or 1792x1024 for DALL-E 3)
            quality: Image quality (standard or hd for DALL-E 3)
            
        Returns:
            str: Public URL of the uploaded image in GCS
        """
        try:
            print(f"🎨 Generating image with DALL-E {model}...")
            print(f"📝 Prompt: {prompt}")
            
            # Generate image with DALL-E
            response = self.openai_client.images.generate(
                model=model,
                prompt=prompt,
                size=size,
                quality=quality,
                n=1,
                response_format="b64_json"
            )
            
            if not response.data or not response.data[0].b64_json:
                raise Exception("No image data received from DALL-E")
            
            # Decode base64 image
            image_b64 = response.data[0].b64_json
            image_data = base64.b64decode(image_b64)
            print(f"✅ Image generated successfully ({len(image_data)} bytes)")
            
            # Create filename based on prompt
            safe_prompt = "".join(c for c in prompt[:30] if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_prompt = safe_prompt.replace(' ', '_')
            filename = f"presentation_{safe_prompt}_{model.replace('-', '_')}.png"
            
            # Upload to Google Cloud Storage
            print(f"☁️ Uploading to GCS as: {filename}")
            file_obj = io.BytesIO(image_data)
            
            public_url = upload_to_gcs(
                file=file_obj,
                filename=filename,
                content_type="image/png",
                bucket_name=self.gcs_bucket
            )
            
            print(f"✅ Image uploaded successfully to: {public_url}")
            return public_url
            
        except Exception as e:
            print(f"❌ Error generating image: {e}")
            raise e
    
    async def generate_with_dalle_2(self, prompt: str) -> str:
        """Generate image using DALL-E 2 (fallback option)"""
        return await self.generate_presentation_image(
            prompt=prompt,
            model="dall-e-2",
            size="1024x1024",
            quality="standard"
        )
    
    async def generate_high_quality(self, prompt: str) -> str:
        """Generate high-quality image using DALL-E 3"""
        return await self.generate_presentation_image(
            prompt=prompt,
            model="dall-e-3",
            size="1024x1024",
            quality="hd"
        )
    
    async def generate_landscape(self, prompt: str) -> str:
        """Generate landscape image using DALL-E 3"""
        return await self.generate_presentation_image(
            prompt=prompt,
            model="dall-e-3",
            size="1792x1024",
            quality="standard"
        )
    
    async def generate_portrait(self, prompt: str) -> str:
        """Generate portrait image using DALL-E 3"""
        return await self.generate_presentation_image(
            prompt=prompt,
            model="dall-e-3",
            size="1024x1792",
            quality="standard"
        )

# Create service instance
enhanced_image_service = EnhancedImageService()

# Backward compatibility functions
async def generate_presentation_image(prompt: str, model: str = "dall-e-3") -> str:
    """Generate image for presentations"""
    return await enhanced_image_service.generate_presentation_image(prompt, model)

def generate_and_upload_image(prompt: str) -> str:
    """Synchronous wrapper for backward compatibility"""
    import asyncio
    return asyncio.run(enhanced_image_service.generate_presentation_image(prompt))
