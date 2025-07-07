from services.storage_service import upload_to_gcs
import io
import os

async def save_document_to_gcs(document_content: str, document_type: str, generated_for: str):
    """Save document to Google Cloud Storage as a text file"""
    try:
        # Create filename
        safe_name = "".join(c for c in generated_for if c.isalnum() or c in (' ', '-', '_')).strip()
        file_name = f"{document_type.replace(' ', '_')}_{safe_name.replace(' ', '_')[:30]}.txt"
        
        # Create file object
        file_obj = io.BytesIO(document_content.encode('utf-8'))
        
        bucket_name = os.getenv("GCS_BUCKET_NAME")
        if not bucket_name:
            raise Exception("GCS_BUCKET_NAME environment variable is not set")
        
        # Upload to Google Cloud Storage
        public_url = upload_to_gcs(file_obj, file_name, "text/plain", bucket_name)
        return public_url
    except Exception as e:
        print(f"Error saving document to GCS: {e}")
        raise e
