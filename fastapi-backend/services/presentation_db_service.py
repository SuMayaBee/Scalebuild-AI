from prisma import Prisma
from typing import List, Optional, Dict, Any
import json
import asyncio
from datetime import datetime

class PresentationDBService:
    """Database service for managing presentations and generated images"""
    
    def __init__(self):
        self.db = Prisma()
        self._connected = False
    
    def _format_presentation_result(self, presentation_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Helper to format presentation data for API response"""
        result = presentation_dict.copy()
        
        # Parse content back to dict if it was stored as JSON string
        if isinstance(result.get("content"), str):
            try:
                result["content"] = json.loads(result["content"])
            except:
                result["content"] = {"slides": []}
        
        # Convert datetime objects to ISO string format
        if result.get("createdAt"):
            result["createdAt"] = result["createdAt"].isoformat() if hasattr(result["createdAt"], 'isoformat') else str(result["createdAt"])
        if result.get("updatedAt"):
            result["updatedAt"] = result["updatedAt"].isoformat() if hasattr(result["updatedAt"], 'isoformat') else str(result["updatedAt"])
        
        return result
    
    async def connect(self):
        """Connect to the database"""
        if not self._connected:
            await self.db.connect()
            self._connected = True
    
    async def disconnect(self):
        """Disconnect from the database"""
        if self._connected:
            await self.db.disconnect()
            self._connected = False
    
    async def ensure_connected(self):
        """Ensure database connection is active"""
        if not self._connected:
            await self.connect()
    
    # User Management
    async def get_or_create_user(self, email: str, name: Optional[str] = None) -> Dict[str, Any]:
        """Get or create a user by email"""
        await self.ensure_connected()
        
        user = await self.db.user.find_unique(where={"email": email})
        if not user:
            user = await self.db.user.create(
                data={
                    "email": email,
                    "name": name or email.split("@")[0]
                }
            )
        return user.dict()
    
    # Presentation Management
    async def create_presentation(
        self, 
        title: str, 
        content: Dict[str, Any], 
        user_email: str,
        theme: str = "default",
        language: str = "English",
        tone: str = "Professional"
    ) -> Dict[str, Any]:
        """Create a new presentation"""
        await self.ensure_connected()
        
        # Get or create user
        user = await self.get_or_create_user(user_email)
        
        # Ensure content is properly formatted JSON
        if not content:
            content = {"slides": []}
        
        presentation = await self.db.presentation.create(
            data={
                "title": title,
                "content": json.dumps(content) if isinstance(content, dict) else content,
                "userId": user["id"],
                "theme": theme,
                "language": language,
                "tone": tone
            },
            include={"user": True}  # Include user data in response
        )
        
        # Convert back to dict format expected by response model
        result = self._format_presentation_result(presentation.dict())
        
        return result
    
    async def get_presentation(self, presentation_id: str) -> Optional[Dict[str, Any]]:
        """Get presentation by ID"""
        await self.ensure_connected()
        
        presentation = await self.db.presentation.find_unique(
            where={"id": presentation_id},
            include={"user": True}
        )
        
        if not presentation:
            return None
            
        return self._format_presentation_result(presentation.dict())
    
    async def update_presentation(
        self, 
        presentation_id: str, 
        content: Optional[Dict[str, Any]] = None,
        title: Optional[str] = None
    ) -> Dict[str, Any]:
        """Update presentation content"""
        await self.ensure_connected()
        
        update_data = {}
        if content:
            update_data["content"] = json.dumps(content) if isinstance(content, dict) else content
        if title:
            update_data["title"] = title
            
        presentation = await self.db.presentation.update(
            where={"id": presentation_id},
            data=update_data,
            include={"user": True}
        )
        
        return self._format_presentation_result(presentation.dict())
    
    async def get_user_presentations(self, user_email: str) -> List[Dict[str, Any]]:
        """Get all presentations for a user"""
        await self.ensure_connected()
        
        user = await self.db.user.find_unique(where={"email": user_email})
        if not user:
            return []
        
        presentations = await self.db.presentation.find_many(
            where={"userId": user.id},
            order_by={"updatedAt": "desc"}
        )
        return [p.dict() for p in presentations]
    
    async def delete_presentation(self, presentation_id: str) -> bool:
        """Delete a presentation"""
        await self.ensure_connected()
        
        try:
            await self.db.presentation.delete(where={"id": presentation_id})
            return True
        except:
            return False
    
    # Generated Image Management
    async def save_generated_image(
        self, 
        url: str, 
        prompt: str, 
        user_email: str,
        model: str = "dall-e-3",
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Save generated image metadata"""
        await self.ensure_connected()
        
        # Get or create user
        user = await self.get_or_create_user(user_email)
        
        image_data = {
            "url": url,
            "prompt": prompt,
            "userId": user["id"],
            "model": model
        }
        
        # Add metadata if provided
        if metadata:
            image_data.update(metadata)
        
        image = await self.db.generatedimage.create(data=image_data)
        return image.dict()
    
    async def get_user_images(self, user_email: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Get generated images for a user"""
        await self.ensure_connected()
        
        user = await self.db.user.find_unique(where={"email": user_email})
        if not user:
            return []
        
        images = await self.db.generatedimage.find_many(
            where={"userId": user.id},
            order_by={"createdAt": "desc"},
            take=limit
        )
        return [img.dict() for img in images]
    
    async def get_image_by_url(self, url: str) -> Optional[Dict[str, Any]]:
        """Get image metadata by URL"""
        await self.ensure_connected()
        
        image = await self.db.generatedimage.find_first(where={"url": url})
        return image.dict() if image else None

# Global service instance
presentation_db_service = PresentationDBService()

# Utility function for managing database connection lifecycle
async def with_db_connection(func, *args, **kwargs):
    """Execute a function with database connection management"""
    await presentation_db_service.connect()
    try:
        result = await func(*args, **kwargs)
        return result
    finally:
        await presentation_db_service.disconnect()
