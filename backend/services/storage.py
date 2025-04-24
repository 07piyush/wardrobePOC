import firebase_admin
from firebase_admin import credentials, storage
import os
from datetime import datetime
from typing import Optional
import tempfile
import logging
from PIL import Image

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StorageService:
    def __init__(self):
        # Initialize Firebase Admin SDK
        try:
            cred = credentials.Certificate(os.getenv('FIREBASE_CREDENTIALS_PATH'))
            firebase_admin.initialize_app(cred, {
                'storageBucket': os.getenv('FIREBASE_STORAGE_BUCKET')
            })
            self.bucket = storage.bucket()
            logger.info("Firebase Storage initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Firebase Storage: {e}")
            raise
    
    def _optimize_image(self, file_path: str) -> str:
        """Optimize image size before upload to reduce storage costs."""
        try:
            with Image.open(file_path) as img:
                # Resize if image is too large
                max_size = (1024, 1024)
                img.thumbnail(max_size, Image.Resampling.LANCZOS)
                
                # Create temporary file for optimized image
                temp_file = tempfile.NamedTemporaryFile(suffix='.jpg', delete=False)
                img.save(temp_file.name, 'JPEG', quality=85, optimize=True)
                return temp_file.name
        except Exception as e:
            logger.error(f"Error optimizing image: {e}")
            return file_path
    
    def upload_file(self, file_path: str, user_id: str) -> Optional[str]:
        """
        Upload a file to Firebase Storage and return the download URL.
        Optimizes image size before upload to reduce costs.
        """
        try:
            # Optimize image before upload
            optimized_path = self._optimize_image(file_path)
            
            # Generate unique blob name
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            file_extension = os.path.splitext(file_path)[1]
            blob_name = f"{user_id}/{timestamp}{file_extension}"
            
            # Upload file
            blob = self.bucket.blob(blob_name)
            blob.upload_from_filename(optimized_path)
            
            # Make the file publicly accessible
            blob.make_public()
            
            # Clean up temporary file if it was created
            if optimized_path != file_path:
                os.unlink(optimized_path)
            
            logger.info(f"File uploaded successfully: {blob_name}")
            return blob.public_url
            
        except Exception as e:
            logger.error(f"Error uploading file to Firebase Storage: {e}")
            return None
    
    def get_download_url(self, blob_name: str) -> Optional[str]:
        """
        Get the download URL for a file in Firebase Storage.
        """
        try:
            blob = self.bucket.blob(blob_name)
            return blob.public_url
        except Exception as e:
            logger.error(f"Error getting download URL: {e}")
            return None
    
    def delete_file(self, blob_name: str) -> bool:
        """
        Delete a file from Firebase Storage.
        """
        try:
            blob = self.bucket.blob(blob_name)
            blob.delete()
            logger.info(f"File deleted successfully: {blob_name}")
            return True
        except Exception as e:
            logger.error(f"Error deleting file from Firebase Storage: {e}")
            return False 