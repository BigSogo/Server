from fastapi import APIRouter

router = APIRouter()

@router.get("/register")
async def hello():
    return "hello"