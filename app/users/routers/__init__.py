from .admin import router as admin_router
from .auth import router as auth_router
from .sender_messages_router import router as sender_messages_router


routers = [auth_router, admin_router, sender_messages_router]
