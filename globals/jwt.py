# 기본 모듈
import os
import jwt
import time
import bcrypt
from dotenv import load_dotenv

# 환경변수 불러오기
load_dotenv()

# JWT Secret Key
JWT_SECRET_KEY =  os.getenv("JWT_SECRET_KEY")

# 기타 모듈
from globals.db import session
from domain.user.user_dto import Login
from domain.user.user_table import User

# JWT 발급
def generate_token(dto: Login) :
    try :
        user = session.query(User).filter(User.email == dto.email).first()

        if user and bcrypt.checkpw(dto.password.encode('utf-8'), user.password.encode('utf-8')):
            payload = {
                'expire' : int(time.time()) + (5 * 7 * 24 * 60 * 60),
                'email' : user.email
            }

            return jwt.encode(
                payload,
                JWT_SECRET_KEY,
                algorithm='HS256'
            )
        else :
            return "발급 실패 (1)"
    except :
        return "발급 실패 (2)"

# 토큰 검증
def verify_token(token) :
    try :
        return jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
    except :
        return "검증 실패"
