# 기본 모듈
from fastapi import APIRouter, Depends
from dotenv import load_dotenv
from globals.base_response import BaseResponse
from sqlalchemy.orm import Session
from fastapi import Depends, UploadFile, File, HTTPException
from typing import Optional
from google.cloud import storage
import uuid

# .env 불러오기
load_dotenv()

# BCrypt
from passlib.context import CryptContext
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

# 관련 모듈
import globals.jwt as jwtUtil
from globals.db import get_db
from domain.user.dto import Login, Register, create_user_response
from domain.user.table import User
from globals.base_response import BaseResponse
from globals.jwt import get_current_user
from globals.firebase import get_bucket

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

# 프로필 사진 업데이트
@router.patch("/update-image", response_model=BaseResponse)
async def update_image(file: UploadFile = File(...), db: Session = Depends(get_db), current_user: dict = Depends(get_current_user), bucket: storage.Bucket = Depends(get_bucket)) :
    user = db.query(User).filter(User.id == id).first()

    filename = f"{uuid.uuid4()}-{file.filename}"

    blob = bucket.blob(filename)
    blob.upload_from_string(await file.read(), content_type=file.content_type)

    user.profile_img = blob.public_url

    return BaseResponse(
        code = 200,
        message = "이미지 저장 성공",
        data = user.profile_img
    )
