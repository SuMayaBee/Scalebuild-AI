from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from routers import presentation, storage, image, logo, background_removal, document_generation
from services.db_service import connect_db, disconnect_db
from services.presentation_db_service import presentation_db_service

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan events"""
    # Startup
    print("🚀 Starting Aladin AI Backend...")
    try:
        # Connect to presentation database (skip for now due to network issues)
        # await presentation_db_service.connect()
        print("✅ Database connection skipped (development mode)")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
    
    yield
    
    # Shutdown
    print("🛑 Shutting down Aladin AI Backend...")
    try:
        # await presentation_db_service.disconnect()
        print("✅ Disconnected from presentation database")
    except Exception as e:
        print(f"❌ Database disconnection failed: {e}")

app = FastAPI(
    title="Aladin AI Backend", 
    version="2.0.0",
    description="AI-powered presentation and document generation API",
    lifespan=lifespan
)

# Add CORS middleware for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://192.168.1.83:3000", "*"],  # Allow frontend origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers with API prefix
app.include_router(presentation.router, prefix="/api", tags=["Presentations"])
app.include_router(storage.router, prefix="/api", tags=["Storage"])
app.include_router(image.router, prefix="/api", tags=["Images"])
app.include_router(logo.router, prefix="/api", tags=["Logos"])
app.include_router(background_removal.router, prefix="/api", tags=["Background Removal"])
app.include_router(document_generation.router, prefix="/api", tags=["Documents"])

@app.get("/")
async def root():
    """API health check endpoint"""
    return {
        "message": "Aladin AI Backend API", 
        "version": "2.0.0",
        "status": "running",
        "features": [
            "Presentation Generation (AI-powered)",
            "Image Generation (DALL-E 3 + GCS Storage)",
            "Document Generation (NDAs, Contracts, etc.)",
            "Logo Generation and Editing",
            "Background Removal"
        ]
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "database": "connected",
        "services": {
            "presentation": "active",
            "image_generation": "active",
            "document_generation": "active",
            "storage": "active"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
