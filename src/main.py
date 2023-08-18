"""src/main.py"""

from fastapi import FastAPI

from src.ticket.routers import router as ticket_router
from src.user.base_config import auth_backend, fastapi_users
from src.user.routers import router as user_router
from src.user.schemas import UserCreate, UserRead, UserUpdate

app = FastAPI(title="Support App")


@app.get("/", name="Welcome Page")
def root():
    """Welcome Page"""
    return {"message": "Welcome"}


app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)

app.include_router(user_router, prefix="/user", tags=["auth"])
app.include_router(ticket_router, prefix="/ticket", tags=["ticket"])
