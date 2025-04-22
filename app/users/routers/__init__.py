from .admin import router as admin_router
from .auth import router as auth_router


routers = [auth_router, admin_router]
