from fastapi import APIRouter

from globals.db import session
from domain.user.dto import register_dto
from domain.user.model import user_table

router = APIRouter()

@router.post("/register")
async def register(dto: register_dto.Register):
    user = user_table()

    user.email = dto.email
    user.name = dto.name
    user.username = dto.username
    user.password = dto.password
    user.major = dto.major

    await session.add(user)
    await session.commit()

    return f"{dto.name} created..."