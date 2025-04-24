from email.message import EmailMessage

from aiosmtplib import send

from app.core.config import settings
from app.utils.base_messenger import BaseMessenger


async def send_welcome_email(to_email: str, user_name: str):
    msg = EmailMessage()
    msg["From"] = settings.SMTP_FROM
    msg["To"] = to_email
    msg["Subject"] = "Добро пожаловать!"
    msg.set_content(f"Hello, {user_name}! Welcome on our app.")

    await send(
        msg,
        hostname=settings.SMTP_HOST,
        port=settings.SMTP_PORT,
        start_tls=True,
        username=settings.SMTP_USERNAME,
        password=settings.SMTP_PASSWORD,
    )


class Messenger(BaseMessenger):
    def __init__(self):
        self._smtp_config = {
            "hostname": settings.SMTP_HOST,
            "port": settings.SMTP_PORT,
            "start_tls": True,
            "username": settings.SMTP_USERNAME,
            "password": settings.SMTP_PASSWORD,
        }

    async def send_letter(self, to_email: str, text: str, subject: str = "Message"):
        msg = EmailMessage()
        msg["From"] = settings.SMTP_FROM
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.set_content(text)

        await send(msg, **self._smtp_config)

    async def send_email(self, to: str, text: str):
        await self.send_letter(to, text)

    async def send_whatsup(self, to: str, text: str):
        await self.send_letter(to, text, subject="WhatsUp message")

    async def send_telegram(self, to: str, text: str):
        await self.send_letter(to, text, subject="Telegram message")

    async def send_viber(self, to: str, text: str):
        await self.send_letter(to, text, subject="Viber message")
