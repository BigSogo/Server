# 기본 모듈
import os
import jwt
import time
import bcrypt
from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# 환경변수 불러오기
load_dotenv()

# Bearer 가져오는 인스턴스
security = HTTPBearer()

# JWT Secret Key
JWT_SECRET_KEY =  os.getenv("JWT_SECRET_KEY")

# 기타 모듈
from globals.db import get_db
from domain.user.dto import Login
from domain.user.table import User
from sqlalchemy.orm import Session

# JWT 발급
def generate_token(dto: Login, db: Session) :
    user = db.query(User).filter(User.email == dto.email).one_or_none()

    if user != None and bcrypt.checkpw(dto.password.encode('utf-8'), user.password.encode('utf-8')):
        payload = {
            'expire' : int(time.time()) + (5 * 7 * 24 * 60 * 60),
            'id' : user.id
        }

        return "Bearer " + jwt.encode(
            payload,
            JWT_SECRET_KEY,
            algorithm='HS256'
        )
    else :
        raise HTTPException(400, "잘못된 정보")

# 사용자 가져오기
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    if credentials:
        token = credentials.credentials
        info = verify_token(token)
        return db.query(User).get(info['id'])
    else:
        HTTPException(403, "권한없음")
    
# 토큰 검증
def verify_token(token) :
    try :
        return jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
    except :
        raise HTTPException(403, "권한없음")
