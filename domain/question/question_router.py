from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from domain.question.question_dto import CreateQuestionRequest
from sqlalchemy.orm import Session
from globals.db import session
from domain.question.question_table import Question
from globals.base_response import BaseResponse
from http import HTTPStatus
from typing import Optional, Union

router = APIRouter()

def get_db():
    try:
        yield session
    finally:
        session.close()

@router.post("/question", response_model=BaseResponse[None])
async def create_question(request: CreateQuestionRequest, db: Session = Depends(get_db)) -> BaseResponse[None]:
    question = Question(
        title = request.title,
        content = request.content,
        user_id = request.user_id
    )
    db.add(question)
    db.commit()

    return BaseResponse(code=HTTPStatus.OK, message="생성완료")

@router.get("/question", response_model=BaseResponse)
async def search_question(query: Optional[str] = None) :
    return BaseResponse(
        code = 200,
        message = "검색 성공",
        data = session.query(Question).filter(Question.title.like(f"%{query}%")).all()
    )