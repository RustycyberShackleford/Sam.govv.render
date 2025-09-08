import os, mimetypes
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

def _drive_service():
    creds_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "service-account.json")
    scopes = ["https://www.googleapis.com/auth/drive.file"]
    creds = service_account.Credentials.from_service_account_file(creds_path, scopes=scopes)
    return build("drive", "v3", credentials=creds, cache_discovery=False)

def upload_to_drive(file_path: str, folder_id: str) -> str:
    service = _drive_service()
    fname = os.path.basename(file_path)
    mime_type, _ = mimetypes.guess_type(file_path)
    media = MediaFileUpload(file_path, mimetype=mime_type or "application/octet-stream")
    file_metadata = {"name": fname, "parents": [folder_id]}
    created = service.files().create(body=file_metadata, media_body=media, fields="id").execute()
    return created["id"]
