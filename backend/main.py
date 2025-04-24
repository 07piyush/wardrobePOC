from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from typing import List, Dict
import tempfile
from PIL import Image
import os
from functools import lru_cache

from services.storage import StorageService
from services.processor import ImageProcessor
from services.recommender import OutfitRecommender

app = FastAPI(
    title="StyleDNA AI",
    description="AI-Powered Fashion Image Processor & Outfit Recommender",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@lru_cache()
def get_storage_service():
    return StorageService()

@lru_cache()
def get_image_processor():
    return ImageProcessor()

@lru_cache()
def get_outfit_recommender():
    return OutfitRecommender()

@app.get("/")
async def root():
    return {"message": "Welcome to StyleDNA AI API"}

@app.post("/upload-image")
async def upload_image(
    file: UploadFile = File(...),
    storage_service: StorageService = Depends(get_storage_service)
):
    try:
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file.filename.split('.')[-1]}") as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_path = temp_file.name
        
        try:
            # Process image
            with Image.open(temp_path) as img:
                # Resize image
                img = img.resize((512, 512), Image.Resampling.LANCZOS)
                # Save processed image
                img.save(temp_path, quality=85, optimize=True)
            
            # Upload to Firebase Storage
            image_url = storage_service.upload_file(temp_path, "test_user")
            if not image_url:
                raise HTTPException(status_code=500, detail="Failed to upload image to storage")
            
            return {
                "message": "Image uploaded and processed successfully",
                "temp_path": temp_path,
                "filename": file.filename,
                "image_url": image_url
            }
        finally:
            # Clean up temp file
            try:
                os.unlink(temp_path)
            except:
                pass
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

@app.get("/recommend")
async def recommend_outfit(
    weather: str,
    event_type: str,
    outfit_recommender: OutfitRecommender = Depends(get_outfit_recommender)
) -> List[Dict]:
    try:
        # Mock wardrobe data for testing
        wardrobe = [
            {
                "clothing_type": "shirt",
                "image_url": "https://example.com/shirt.jpg",
                "dominant_color": {"r": 255, "g": 0, "b": 0},
                "tags": ["red", "casual", "cotton"]
            },
            {
                "clothing_type": "pants",
                "image_url": "https://example.com/pants.jpg",
                "dominant_color": {"r": 0, "g": 0, "b": 255},
                "tags": ["blue", "formal", "denim"]
            }
        ]
        
        # Get recommendations
        recommendations = outfit_recommender.recommend_outfits(
            wardrobe=wardrobe,
            weather=weather,
            event_type=event_type
        )
        
        return recommendations
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting recommendations: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 