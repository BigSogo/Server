from fastapi import FastAPI
from globals.db import Base
from globals.db import ENGINE
from domain.user import router as user
from domain.question import router as question
import logging

logging.basicConfig()

Base.metadata.create_all(bind=ENGINE)

app = FastAPI()

app.include_router(profile_router, prefix="/profile", tags=["profile"])
app.include_router(question.router, prefix="/question", tags=["question"])
app.include_router(user.router, prefix="/user", tags=["user"])
