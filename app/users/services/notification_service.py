from app.users.schemas import SendMassage
from app.utils.email_sender import Messenger


class NotificationService:
    def __init__(self):
        self.messenger = Messenger()

    async def send_massage(self, data: SendMassage) -> str:
        match data.type:
            case "email":
                await self.messenger.send_email(data.value, data.text)
                return "The email was sent successfully"
            case "WhatsUp":
                await self.messenger.send_whatsup(data.value, data.text)
                return "The whatsup-message was sent successfully"
            case "Telegram":
                await self.messenger.send_telegram(data.value, data.text)
                return "The telegram-message was sent successfully"
            case "Viber":
                await self.messenger.send_viber(data.value, data.text)
                return "The viber-message was sent successfully"
            case _:
                raise ValueError(f"Unknown type: {data.type}")
