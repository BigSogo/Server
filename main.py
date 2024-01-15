from fastapi import FastAPI

from domain.user import user_router;

application = FastAPI()

application.include_router(user_router.router)  