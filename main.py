from fastapi import FastAPI
from globals.db import Base
from globals.db import ENGINE
from domain.user import user_router;

Base.metadata.create_all(bind=ENGINE)

app = FastAPI()

app.include_router(user_router.router)