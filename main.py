# 기본 모듈
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import logging

# 관련 모듈
from globals.db import Base
from globals.db import ENGINE
from domain.user import router as user
from domain.question import router as question
from domain.profile import router as profile
from domain.comment import router as comment

logging.basicConfig()

Base.metadata.create_all(bind=ENGINE)

app = FastAPI()

# 라우터 설정
app.include_router(profile.router, prefix="/profile", tags=["profile"])
app.include_router(question.router, prefix="/question", tags=["question"])
app.include_router(user.router, prefix="/user", tags=["user"])
app.include_router(comment.router, prefix="/comment", tags=["comment"])

# CORS 설정
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn_kwargs = {
        "host": "0.0.0.0",
        "port": 8080,
        "workers": 10,
        "loop": "uvloop",
        "http": "httptools",
        "forwarded_allow_ips": "*"
    }

    uvicorn.run("main:app", **uvicorn_kwargs, log_level="debug")
