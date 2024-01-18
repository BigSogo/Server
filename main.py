from fastapi import FastAPI
from globals.db import Base
from globals.db import ENGINE
from domain.user import user_router
from domain.question import question_router
from domain.profile import profile_router
import logging

logging.basicConfig()

Base.metadata.create_all(bind=ENGINE)

app = FastAPI()

app.include_router(question_router.router, prefix="/question", tags=["question"])
app.include_router(user_router.router, prefix="/user", tags=["user"])
app.include_router(profile_router, prefix="/profile", tags=["profile"])
