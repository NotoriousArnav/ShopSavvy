from .catalouge import router as catalouge_router
from .auth import router as auth_router

routers = [
    catalouge_router,
    auth_router
]
