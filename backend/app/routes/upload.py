from fastapi import APIRouter, UploadFile, HTTPException
import imghdr
from ..services.storage import StorageService
from ..services.processor import ImageProcessor

router = APIRouter()

ALLOWED_MIME_TYPES = ["image/jpeg", "image/png"]

@router.post("/upload-image")
async def upload_image(file: UploadFile):
    """
    Upload and process an image file
    """
    # Validate file type
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(status_code=400, detail="Invalid file type")
    
    # Read file content
    content = await file.read()
    
    # Validate actual content is an image
    if not imghdr.what(None, h=content):
        raise HTTPException(status_code=400, detail="Invalid content type")
        
    # Process image
    processor = ImageProcessor()
    processed_image = processor.process_image(content)
    
    # Upload to storage
    storage = StorageService()
    url = storage.upload_image(processed_image, file.filename)
    
    return {"url": url} 