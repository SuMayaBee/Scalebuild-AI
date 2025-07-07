"""
Test script for presentation image generation service
"""
import asyncio
import os
from services.presentation_image_service import presentation_image_service

async def test_image_generation():
    """Test DALL-E image generation and GCS upload"""
    
    print("🔍 Testing Image Generation Service...")
    print("=" * 50)
    
    # Test 1: Check OpenAI connection
    print("1. Testing OpenAI connection...")
    openai_ok = presentation_image_service.test_openai_connection()
    print(f"   OpenAI Status: {'✅ Connected' if openai_ok else '❌ Failed'}")
    
    # Test 2: Check GCS connection
    print("\n2. Testing Google Cloud Storage connection...")
    gcs_ok = presentation_image_service.test_gcs_connection()
    print(f"   GCS Status: {'✅ Connected' if gcs_ok else '❌ Failed'}")
    
    # Test 3: Generate a test image (only if both services work)
    if openai_ok and gcs_ok:
        print("\n3. Testing image generation...")
        try:
            test_prompt = "A modern office workspace with computers and plants, professional lighting"
            print(f"   Prompt: {test_prompt}")
            print("   Generating image with DALL-E 3...")
            
            image_url = await presentation_image_service.generate_presentation_image(
                prompt=test_prompt,
                model="dalle3",
                size="1024x1024"
            )
            
            print(f"   ✅ Image generated successfully!")
            print(f"   📸 URL: {image_url}")
            
            return image_url
            
        except Exception as e:
            print(f"   ❌ Image generation failed: {e}")
            return None
    else:
        print("\n3. ⏭️  Skipping image generation (services not available)")
        return None

async def test_dalle2_fallback():
    """Test DALL-E 2 fallback"""
    print("\n4. Testing DALL-E 2 fallback...")
    try:
        test_prompt = "A simple presentation slide background with geometric shapes"
        print(f"   Prompt: {test_prompt}")
        print("   Generating image with DALL-E 2...")
        
        image_url = await presentation_image_service.generate_presentation_image(
            prompt=test_prompt,
            model="dalle2",
            size="1024x1024"
        )
        
        print(f"   ✅ DALL-E 2 generation successful!")
        print(f"   📸 URL: {image_url}")
        
        return image_url
        
    except Exception as e:
        print(f"   ❌ DALL-E 2 generation failed: {e}")
        return None

async def main():
    """Main test function"""
    print("🧪 Presentation Image Service Test")
    print("=" * 50)
    
    # Check environment variables
    print("Environment Check:")
    openai_key = os.getenv("OPENAI_API_KEY")
    gcs_bucket = os.getenv("GCS_BUCKET_NAME")
    gcs_creds = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    
    print(f"   OPENAI_API_KEY: {'✅ Set' if openai_key else '❌ Missing'}")
    print(f"   GCS_BUCKET_NAME: {'✅ Set' if gcs_bucket else '❌ Missing'} ({gcs_bucket})")
    print(f"   GOOGLE_APPLICATION_CREDENTIALS: {'✅ Set' if gcs_creds else '❌ Missing'} ({gcs_creds})")
    
    if gcs_creds and not os.path.exists(gcs_creds):
        print(f"   ⚠️  Credentials file not found: {gcs_creds}")
    
    print()
    
    # Run tests
    image_url_1 = await test_image_generation()
    image_url_2 = await test_dalle2_fallback()
    
    print("\n" + "=" * 50)
    print("📊 Test Summary:")
    print(f"   DALL-E 3: {'✅ Success' if image_url_1 else '❌ Failed'}")
    print(f"   DALL-E 2: {'✅ Success' if image_url_2 else '❌ Failed'}")
    
    if image_url_1 or image_url_2:
        print("\n🎉 Image generation service is working!")
        print("Ready to integrate with FastAPI endpoints.")
    else:
        print("\n🔧 Please check your environment configuration.")

if __name__ == "__main__":
    asyncio.run(main())
