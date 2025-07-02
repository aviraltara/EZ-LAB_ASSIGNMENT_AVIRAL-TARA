from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas import UserCreate
from app.database import SessionLocal
from app.models import User
from app.auth.utils import hash_password
from app.utils.email import send_verification_email
from itsdangerous import URLSafeTimedSerializer
from app.config import settings
from app.users.services import get_user_by_email


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

serializer = URLSafeTimedSerializer(settings.SECRET_KEY)
@router.post("/signup")
def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    from app.users.services import get_user_by_email
    user = get_user_by_email(db, user_data.email)

    if user:
        raise HTTPException(status_code=400, detail="User already exists")
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_pwd = hash_password(user_data.password)
    new_user = User(email=user_data.email, password=hashed_pwd, role="client", is_verified=False)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = serializer.dumps(user_data.email, salt="email-verify")
    verification_link = f"http://localhost:8000/users/verify-email?token={token}"
    send_verification_email(user_data.email, verification_link)

    return {"message": "User created. Check your email to verify account.", "verification_url": verification_link}

@router.get("/verify-email")
def verify_email(token: str, db: Session = Depends(get_db)):
    try:
        email = serializer.loads(token, salt="email-verify", max_age=3600)
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        user.is_verified = True
        db.commit()
        return {"message": "Email verified successfully."}
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
