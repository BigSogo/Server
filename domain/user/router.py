# 기본 모듈
from fastapi import APIRouter, Depends, HTTPException
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from fastapi import Depends
from typing import Optional
from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import os
from redis import Redis

# .env 불러오기
load_dotenv()

# BCrypt
from passlib.context import CryptContext
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

# 관련 모듈
import globals.jwt as jwtUtil
from globals.db import get_db, get_redis
from domain.user.dto import Login, Register, EmailAuthentication, EmailSend, create_user_response
from domain.user.table import User
from globals.base_response import BaseResponse

# 라우터 설정
router = APIRouter()
num_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

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
        major = "|".join(dto.major)
    )

    db.add(user)
    db.commit()

    return BaseResponse(code=200, message=f"{dto.username} created...")

@router.get("/search", response_model=BaseResponse)
async def search_user(query: Optional[str] = None, db: Session = Depends(get_db)) :
    results = db.query(User).filter(User.major.like(f"%{query}%"))

    datas = []
    for user in results :
        datas.append(create_user_response(user))

    return BaseResponse(
        code = 200,
        message = "유저 검색 성공",
        data = datas
    )

@router.post("/email/send", response_model=BaseResponse)
async def email_send(email: EmailSend, db: Session = Depends(get_db), redis: Redis = Depends(get_redis)):
    user: User = db.query(User).filter(User.email == email.email).one_or_none()
    if user is not None:
        raise HTTPException(400, "이메일 중복")
    
    random_code = ''.join(random.sample(num_list, 6))
    redis.set(email.email, random_code)

    sender_email = os.getenv("EMAIL")
    sender_password = os.getenv("PASSWORD")

    email_server = SMTP("smtp.gmail.com", 587)
    email_server.starttls()
    email_server.login(sender_email, sender_password)

    msg = MIMEMultipart()
    msg["FROM"] = sender_email
    msg["To"] = email.email
    msg["Subject"] = "sogo 이메일 인증"
    msg.attach(MIMEText(random_code))

    email_server.send_message(msg)
    email_server.quit()

    return BaseResponse(code=200, message="이메일 전송 성공")

@router.post("/email/authentication", response_model=BaseResponse[bool])
async def email_authentication(email: EmailAuthentication, redis: Redis = Depends(get_redis)):
    code = redis.get(email.email)

    if code == email.code:
        return BaseResponse(code=200, message="성공", data=True)
    else:
        return HTTPException(401, "인증 코드가 다릅니다.")