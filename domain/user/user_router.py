# 기본 모듈
from fastapi import APIRouter
from dotenv import load_dotenv

# .env 불러오기
load_dotenv()

# BCrypt
from passlib.context import CryptContext
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

# 관련 모듈
import globals.jwt as jwtUtil
from globals.db import session
from domain.user.user_dto import Login, Register
from domain.user.user_table import User

# 라우터 설정
router = APIRouter()

# 로그인
@router.post("/login")
async def login(dto: Login) :
    return jwtUtil.generate_token(dto)

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