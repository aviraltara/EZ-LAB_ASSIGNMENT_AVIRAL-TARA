from sqlalchemy.orm import Session
from app.models import User
from app.auth.utils import hash_password

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_client_user(db: Session, email: str, password: str):
    hashed_pwd = hash_password(password)
    new_user = User(email=email, password=hashed_pwd, role="client", is_verified=False)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def verify_user_email(db: Session, email: str):
    user = get_user_by_email(db, email)
    if user:
        user.is_verified = True
        db.commit()
    return user
