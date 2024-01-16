from fastapi import APIRouter

from passlib.context import CryptContext

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

from globals.db import session
from domain.user.dto.register_dto import Register
from domain.user.model.user_table import User

router = APIRouter()

@router.post("/register")
async def register(dto: Register):
    user = User(
        email = dto.email,
        username = dto.username,
        password = bcrypt_context.hash(dto.password),
        major = dto.major
    )

    session.add(user)
    session.commit()

    return f"{dto.username} created..."