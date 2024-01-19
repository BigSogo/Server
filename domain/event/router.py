# 기본 모듈
from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from google.cloud import storage
import uuid

# 관련 모듈
from globals.db import get_db
from globals.firebase import get_bucket
from domain.event.table import Event
from globals.base_response import BaseResponse
from domain.event.dto import create_event_response

router = APIRouter()

# 이벤트 리스트 가져오기
@router.get("/list", response_model=BaseResponse)
async def get_event_list(db: Session = Depends(get_db)) :
    results = db.query(Event).all()

    datas = []
    for event in results :
        datas.append(create_event_response(event))

    return BaseResponse(
        code = 200,
        message = "이벤트 리스트 조회 성공",
        data = datas
    )

# 이벤트 만들기
@router.post("", response_model=BaseResponse)
async def create_event(file: UploadFile = File(...), db: Session = Depends(get_db), bucket: storage.Bucket = Depends(get_bucket)) :
    filename = f"{uuid.uuid4()}-{file.filename}"

    blob = bucket.blob(filename)
    blob.upload_from_string(await file.read(), content_type=file.content_type)

    blob.make_public()

    event = Event(
        image_url = blob.public_url
    )

    db.add(event)
    db.commit()

    return BaseResponse(
        code = 200,
        message = "이벤트 업로드 성공",
        data = blob.public_url
    )