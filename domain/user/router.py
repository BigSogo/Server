# 기본 모듈
from fastapi import APIRouter, Depends
from dotenv import load_dotenv
from globals.base_response import BaseResponse
from sqlalchemy.orm import Session
from fastapi import Depends

# .env 불러오기
load_dotenv()

# BCrypt
from passlib.context import CryptContext
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

# 관련 모듈
import globals.jwt as jwtUtil
from globals.db import get_db
from domain.user.dto import Login, Register
from domain.user.table import User
from globals.base_response import BaseResponse

# 라우터 설정
router = APIRouter()

# 로그인
@router.post("/login", response_model=BaseResponse[str])
async def login(dto: Login, db: Session = Depends(get_db)) :
    return BaseResponse(code=200, message="발급 완료", data = jwtUtil.generate_token(dto, db))

# 테스트 라우터
@router.get("/test")
async def test(current_user: dict = Depends(jwtUtil.get_current_user)) :
    return current_user

# 회원가입
@router.post("", response_model=BaseResponse[None])
async def register(dto: Register, db: Session = Depends(get_db)):
    user = User(
        email = dto.email,
        username = dto.username,
        password = bcrypt_context.hash(dto.password),
    )

    db.add(user)
    db.commit()

    return BaseResponse(code=200, message=f"{dto.username} created...")