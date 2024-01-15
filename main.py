from fastapi import FastAPI

from router import helloRouter

application = FastAPI()

application.include_router(helloRouter.router)