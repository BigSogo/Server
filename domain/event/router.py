# 기본 모듈
from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from typing import List

# 관련 모듈
from globals.jwt import get_db
from domain.event.table import Event
from globals.base_response import BaseResponse

router = APIRouter()

@router.get("", response_model=List[Event])
async def get_event(db: Session = Depends(get_db)) :
    return db.query(Event).all()

@router.post("", response_model=BaseResponse)
async def upload_event(file: UploadFile = File(...), db: Session = Depends(get_db)) :
    image = await file.read()

    db_image = Event(event_img=image)
    db.add(db_image)
    db.commit()

    return BaseResponse(
        code = 200,
        message = "이미지 업로드 성공",
        data = None
    )

