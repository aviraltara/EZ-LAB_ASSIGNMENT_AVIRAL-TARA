from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: str  # 'ops' or 'client'

class UserOut(BaseModel):
    id: int
    email: EmailStr
    role: str
    is_verified: bool

    class Config:
        orm_mode = True


class FileOut(BaseModel):
    id: int
    filename: str
    owner_id: int

    class Config:
        from_attributes = True  # use 'from_attributes' for Pydantic v2 instead of 'orm_mode'
