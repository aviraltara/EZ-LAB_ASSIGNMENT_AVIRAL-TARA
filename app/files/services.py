import uuid
from fastapi import UploadFile
from itsdangerous import URLSafeTimedSerializer
from app.config import settings

def save_file_to_disk(file: UploadFile, upload_dir: str) -> str:
    ext = file.filename.split(".")[-1]
    unique_name = f"{uuid.uuid4()}.{ext}"
    file_path = f"{upload_dir}/{unique_name}"

    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())

    return unique_name

def generate_secure_link(file_id: int, email: str) -> str:
    serializer = URLSafeTimedSerializer(settings.SECRET_KEY)
    token = serializer.dumps({"file_id": file_id, "email": email}, salt="download-link")
    return f"http://localhost:8000/files/secure-download/{token}"
