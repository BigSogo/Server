from fastapi import APIRouter, Depends, HTTPException
from domain.question.question_dto import CreateQuestion, GetQuestion
from sqlalchemy.orm import Session
from globals.db import get_db
from domain.question.question_table import Question
from globals.base_response import BaseResponse
from http import HTTPStatus
from globals.jwt import get_current_user

router = APIRouter()

@router.post("/question", response_model=BaseResponse[None])
async def create_question(request: CreateQuestion, db: Session = Depends(get_db), userData: dict = Depends(get_current_user)) -> BaseResponse[None]:
    request.user_id = userData['user']['id']
    question = Question(
        title = request.title,
        content = request.content,
        user_id = request.user_id
    )
    db.add(question)
    db.commit()

    return BaseResponse(code=HTTPStatus.OK, message="생성완료")

@router.get("/question/{question_id}", response_model=BaseResponse[GetQuestion])
async def get_question(question_id:int, db: Session = Depends(get_db)):
    question = db.query(Question).filter(Question.id == question_id).one_or_none()
    if question == None:
        HTTPException(404, "데이터를 찾을 수 없습니다.")
    else:
        return BaseResponse(code=200, message="조회 성공", data=question)

async def get_question_list():
    pass