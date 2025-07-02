from fastapi import FastAPI
from app.auth.routes import router as auth_router
from app.users.routes import router as user_router
from app.files.routes import router as file_router
from app.database import Base, engine

# Create DB tables
Base.metadata.create_all(bind=engine)

# ✅ This must exist
app = FastAPI()

# Include routes
app.include_router(auth_router, prefix="/auth")
app.include_router(user_router, prefix="/users")
app.include_router(file_router, prefix="/files")
