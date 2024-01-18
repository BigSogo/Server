# 기본 모듈
from fastapi import FastAPI
import logging

# 관련 모듈
from globals.db import Base
from globals.db import ENGINE
from domain.user import router as user
from domain.question import router as question
from domain.profile import router as profile

logging.basicConfig()

Base.metadata.create_all(bind=ENGINE)

app = FastAPI()

# 라우터 설정
app.include_router(profile.router, prefix="/profile", tags=["profile"])
app.include_router(question.router, prefix="/question", tags=["question"])
app.include_router(user.router, prefix="/user", tags=["user"])
