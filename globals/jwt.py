# 기본 모듈
import os
import jwt
import time
import bcrypt
from dotenv import load_dotenv
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# 환경변수 불러오기
load_dotenv()

# Bearer 가져오는 인스턴스
security = HTTPBearer()

# JWT Secret Key
JWT_SECRET_KEY =  os.getenv("JWT_SECRET_KEY")

# 기타 모듈
from globals.db import session
from domain.user.user_dto import Login
from domain.user.user_table import User
from globals.base_response import BaseResponse

# JWT 발급
def generate_token(dto: Login) :
    try :
        user = session.query(User).filter(User.email == dto.email).first()

        if user and bcrypt.checkpw(dto.password.encode('utf-8'), user.password.encode('utf-8')):
            payload = {
                'expire' : int(time.time()) + (5 * 7 * 24 * 60 * 60),
                'id' : user.id
            }

            return BaseResponse(
                    code = 200,
                    message = "발급 성공",
                    data = "Bearer " + jwt.encode(
                    payload,
                    JWT_SECRET_KEY,
                    algorithm='HS256'
                )
            )
        else :
            return "발급 실패 (1)"
    except :
        return "발급 실패 (2)"

# 사용자 가져오기
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials:
        token = credentials.credentials
        info = verify_token(token)
        return {"user": info}
    
# 토큰 검증
def verify_token(token) :
    try :
        return jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
    except :
        return "검증 실패"
