from fastapi import APIRouter, Depends
from domain.question.question_dto import CreateQuestionRequest
from sqlalchemy.orm import Session
from globals.db import session
from domain.question.question_table import Question
from globals.base_response import BaseResponse
from http import HTTPStatus

router = APIRouter()

def get_db():
    try:
        yield session
    finally:
        session.close()

@router.post("/question", response_class=BaseResponse[None])
async def create_question(request: CreateQuestionRequest, db: Session = Depends(get_db)):
    question = Question(
        title = request.title,
        content = request.content,
        userId = request.userId
    )
    db.add(question)
    db.commit()

    return BaseResponse(code=HTTPStatus.OK, message="생성완료")