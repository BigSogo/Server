# 기본 모듈
from fastapi import APIRouter, Depends, HTTPException
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from fastapi import Depends, UploadFile, File, HTTPException
from typing import Optional
from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import os
from redis import Redis
from google.cloud import storage
import uuid
from markdown_it import MarkdownIt

# 마크다운 설정
md = MarkdownIt()

# .env 불러오기
load_dotenv()

# BCrypt
from passlib.context import CryptContext
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

# 관련 모듈
import globals.jwt as jwtUtil
from globals.db import get_db, get_redis
from domain.user.dto import Login, Register, EmailAuthentication, EmailSend, create_user_response, UserResponse
from domain.user.table import User
from globals.base_response import BaseResponse
from globals.jwt import get_current_user
from globals.firebase import get_bucket

# 라우터 설정
router = APIRouter()
num_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

# 로그인
@router.post("/login", response_model=BaseResponse[str])
async def login(dto: Login, db: Session = Depends(get_db)) :
    return BaseResponse(code=200, message="발급 완료", data = jwtUtil.generate_token(dto, db))

# 테스트 라우터
@router.get("", response_model=BaseResponse[UserResponse])
async def myinfo(current_user: User = Depends(jwtUtil.get_current_user)) :
    if current_user is None:
        HTTPException(403, "권한이 없습니다")
    return BaseResponse(code=200, message="조회 성공", data=create_user_response(current_user))

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

@router.post("/email/send", response_model=BaseResponse[None])
async def email_send(email: EmailSend, db: Session = Depends(get_db), redis: Redis = Depends(get_redis)):
    user: User = db.query(User).filter(User.email == email.email).one_or_none()
    if user is not None:
        raise HTTPException(400, "이메일 중복")
    
    random_code = ''.join(random.sample(num_list, 6))
    redis.setex(email.email, 300, random_code)

    sender_email = os.getenv("EMAIL")
    sender_password = os.getenv("PASSWORD")

    email_server = SMTP("smtp.gmail.com", 587)
    email_server.starttls()
    email_server.login(sender_email, sender_password)

    markdown_message = f"""
    # **SOGO**에 오신 것을 환영합니다 !

    **인증코드는 아래와 같습니다**

    - {random_code}

    **감사합니다!**
    """

    html_message = md.render(markdown_message)

    msg = MIMEMultipart()
    msg["FROM"] = sender_email
    msg["To"] = email.email
    msg["Subject"] = "sogo 이메일 인증"
    msg.attach(MIMEText(html_message, "html"))

    email_server.send_message(msg)
    email_server.quit()

    return BaseResponse(code=200, message="이메일 전송 성공")

@router.get("/email/duplicate", response_model=BaseResponse[bool])
async def email_duplicate(email:str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).one_or_none()

    return BaseResponse(code=200, message="중복 체크 완료", data=True if user is None else False)

@router.post("/email/auth", response_model=BaseResponse[bool])
async def email_authentication(email: EmailAuthentication, redis: Redis = Depends(get_redis)):
    
    code = redis.get(email.email)
    print(code)

    if code == email.code:
        redis.delete(email.email)
        return BaseResponse(code=200, message="성공", data=True)
    else:
        return BaseResponse(code=200, message="실패", data=False)

# 프로필 사진 업데이트
@router.patch("/update-image", response_model=BaseResponse)
async def update_image(file: UploadFile = File(...), db: Session = Depends(get_db), current_user: dict = Depends(get_current_user), bucket: storage.Bucket = Depends(get_bucket)) :
    user = db.query(User).filter(User.id == current_user.id).first()

    filename = f"{uuid.uuid4()}-{file.filename}"

    blob = bucket.blob(filename)
    blob.upload_from_string(await file.read(), content_type=file.content_type)

    blob.make_public()
    user.profile_img = blob.public_url

    db.add(user)
    db.commit()

    return BaseResponse(
        code = 200,
        message = "이미지 저장 성공",
        data = user.profile_img
    )
