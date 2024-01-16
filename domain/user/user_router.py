# 기본 모듈
from fastapi import APIRouter

# BCrypt
from passlib.context import CryptContext
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

# 관련 모듈
from globals.db import session
from domain.user.user_dto import Register
from domain.user.user_table import User

# 라우터 설정
router = APIRouter()

# 회원가입
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