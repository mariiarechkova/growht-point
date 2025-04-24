from fastapi import APIRouter

from app.users.schemas import SendMassage
from app.users.services.notification_service import NotificationService


router = APIRouter(prefix="/api/sender", tags=["Send message"])


@router.post("/send_email")
async def send_message(data: SendMassage):
    service = NotificationService()
    result = await service.send_massage(data)
    return {"detail": result}
