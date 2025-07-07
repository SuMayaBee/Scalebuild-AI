import os
from google.cloud import storage

def upload_to_gcs(file, filename: str, content_type: str, bucket_name: str):
    """Uploads a file to the given GCS bucket."""

    # Initialize the GCS client
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(filename)

    # Upload the file
    blob.upload_from_file(file, content_type=content_type)

    # Return the public URL
    return blob.public_url
