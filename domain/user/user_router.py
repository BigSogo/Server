# 기본 모듈
import jwt
from fastapi import APIRouter
from dotenv import load_dotenv
import time
import os

# .env 불러오기
load_dotenv()

# BCrypt
import bcrypt
from passlib.context import CryptContext
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

# 관련 모듈
from globals.db import session
from domain.user.user_dto import Login, Register
from domain.user.user_table import User

# 라우터 설정
router = APIRouter()

# 로그인
@router.post("/login")
async def login(dto: Login) :
    user = session.query(User).filter(User.email == dto.email).first()

    if user and bcrypt.checkpw(dto.password.encode('utf-8'), user.password.encode('utf-8')):
        payload = {
            'expire' : int(time.time()) + (5 * 7 * 24 * 60 * 60),
            'email' : user.email
        }

        return jwt.encode(
            payload,
            os.getenv("JWT_SECRET_KEY"),
            algorithm='HS256'
        )

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