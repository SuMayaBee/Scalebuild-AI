"""
Test script for the enhanced presentation image generation service
"""
import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def test_image_generation():
    """Test the DALL-E image generation service"""
    print("Testing Enhanced Image Generation Service...")
    
    try:
        # Import the service
        from services.image_service import PresentationImageService
        
        # Create service instance
        service = PresentationImageService()
        
        # Test prompt
        test_prompt = "modern office workspace with computers and plants, professional lighting"
        
        print(f"Generating image for prompt: '{test_prompt}'")
        print("Using DALL-E 3 and uploading to Google Cloud Storage...")
        
        # Generate image
        image_url = await service.generate_presentation_image(test_prompt)
        
        print(f"✅ Success! Image generated and uploaded:")
        print(f"📸 URL: {image_url}")
        
        return image_url
        
    except Exception as e:
        print(f"❌ Error during image generation: {e}")
        return None

async def test_database_connection():
    """Test database connection and operations"""
    print("\nTesting Database Connection...")
    
    try:
        from services.presentation_db_service import presentation_db_service
        from prisma import Prisma
        
        # Initialize database connection
        db = Prisma()
        await db.connect()
        
        print("✅ Database connected successfully!")
        
        # Test creating a test presentation
        test_presentation = await presentation_db_service.create_presentation(
            title="Test Presentation",
            content={"slides": [{"title": "Test Slide"}]},
            user_email="test@example.com",
            theme="default"
        )
        
        print(f"✅ Test presentation created: {test_presentation['id']}")
        
        # Clean up - delete the test presentation
        await presentation_db_service.delete_presentation(test_presentation['id'])
        print("✅ Test presentation cleaned up")
        
        await db.disconnect()
        
    except Exception as e:
        print(f"❌ Database error: {e}")

if __name__ == "__main__":
    print("🚀 Starting Presentation Service Tests\n")
    
    # Test image generation
    image_url = asyncio.run(test_image_generation())
    
    # Test database connection
    asyncio.run(test_database_connection())
    
    print("\n🎉 All tests completed!")
