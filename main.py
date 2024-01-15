from fastapi import FastAPI

from register import register_router;

application = FastAPI()

application.include_router(register_router.router)  