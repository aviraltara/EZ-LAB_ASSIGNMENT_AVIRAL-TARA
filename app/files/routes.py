import os
import uuid
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from app.database import SessionLocal
from app.models import User, File as FileModel
from app.files.services import save_file_to_disk, generate_secure_link
from jose import JWTError, jwt
from app.config import settings
from app.schemas import FileOut

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email = payload.get("sub")
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(status_code=401, detail="Invalid user")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.post("/upload")
def upload_file(file: UploadFile = File(...), user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if user.role != "ops":
        raise HTTPException(status_code=403, detail="Only ops users can upload files")

    allowed_types = ["application/vnd.openxmlformats-officedocument.wordprocessingml.document",  # .docx
                     "application/vnd.openxmlformats-officedocument.presentationml.presentation",  # .pptx
                     "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"]  # .xlsx

    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Invalid file type")

    filename = save_file_to_disk(file, UPLOAD_DIR)

    db_file = FileModel(filename=filename, uploader_id=user.id)
    db.add(db_file)
    db.commit()

    return {"message": "File uploaded successfully", "filename": filename}


@router.get("/list", response_model=list[FileOut])
def list_files(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    files = db.query(FileModel).all()
    return files


@router.get("/download-file/{file_id}")
def get_download_link(file_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if user.role != "client":
        raise HTTPException(status_code=403, detail="Only client users can get download links")

    db_file = db.query(FileModel).filter(FileModel.id == file_id).first()
    if not db_file:
        raise HTTPException(status_code=404, detail="File not found")

    link = generate_secure_link(file_id, user.email)
    return {"download-link": link, "message": "success"}


@router.get("/secure-download/{token}")
def secure_download(token: str, db: Session = Depends(get_db)):
    from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
    serializer = URLSafeTimedSerializer(settings.SECRET_KEY)

    try:
        data = serializer.loads(token, salt="download-link", max_age=300)
        file_id = data["file_id"]
        allowed_user = data["email"]

        file = db.query(FileModel).filter(FileModel.id == file_id).first()
        if not file:
            raise HTTPException(status_code=404, detail="File not found")

        filepath = os.path.join(UPLOAD_DIR, file.filename)
        if not os.path.exists(filepath):
            raise HTTPException(status_code=404, detail="File no longer exists")

        from fastapi.responses import FileResponse
        return FileResponse(path=filepath, filename=file.filename, media_type='application/octet-stream')

    except SignatureExpired:
        raise HTTPException(status_code=403, detail="Link expired")
    except BadSignature:
        raise HTTPException(status_code=403, detail="Invalid token")
