from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import EmailStr
from app.config import settings

conf = ConnectionConfig(
    MAIL_USERNAME="your_email@example.com",
    MAIL_PASSWORD="your_email_password",
    MAIL_FROM="your_email@example.com",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,    # Use this instead of MAIL_TLS
    MAIL_SSL_TLS=False,    # Use this instead of MAIL_SSL
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
)


async def send_verification_email(email: EmailStr, verification_link: str):
    message = MessageSchema(
        subject="Email Verification",
        recipients=[email],
        body=f"Please verify your email by clicking on this link: {verification_link}",
        subtype="plain"
    )
    fm = FastMail(conf)
    await fm.send_message(message)
