from fastapi import APIRouter, Depends, HTTPException
from http import HTTPStatus
from sqlalchemy.orm import Session

from domain.question.question_table import Question
from domain.user.user_table import User
from domain.question.question_dto import CreateQuestion, GetQuestion, GetQuestionList
from domain.comment.comment_dto import CommentDto
from domain.user.user_dto import UserResponse

from globals.base_response import BaseResponse
from globals.db import get_db
from globals.jwt import get_current_user

from thefuzz import process

router = APIRouter()

@router.post("", response_model=BaseResponse[None])
async def create_question(request: CreateQuestion, db: Session = Depends(get_db), user_data: User = Depends(get_current_user)) -> BaseResponse[None]:
    writer = user_data.id

    question = Question(
        title = request.title,
        content = request.content,
        senior_id = request.senior_id,
        writer_id = writer
    )

    db.add(question)
    db.commit()

    return BaseResponse(code=HTTPStatus.OK, message="생성완료")

@router.get("", response_model=BaseResponse[GetQuestion])
async def get_question(id:int, db: Session = Depends(get_db)):
    question = db.query(Question).get(id)

    if question == None:
        raise HTTPException(404, "데이터를 찾을 수 없습니다.")
    
    writer = __create_user_response(question.writer)

    senior = None if question.senior == None else __create_user_response(question.senior)

    comments = [CommentDto(
        id=comment.id,
        content=comment.content,
        date=comment.date
    ) for comment in question.comments]

    response = GetQuestion(
        id=question.id,
        title=question.title,
        content=question.content,
        date=question.date,
        writer=writer,
        senior=senior,
        comments=comments
    )

    return BaseResponse(code=200, message="조회 성공", data=response)

@router.get("/list", response_model=BaseResponse[list[GetQuestionList]])
async def get_question_list(db: Session = Depends(get_db)):
    questions = db.query(Question).all()
    
    question_list = [GetQuestionList(
        id=question.id,
        title=question.title,
        date=question.date,
        writer=__create_user_response(question.writer),
        senior=None if question.senior == None else __create_user_response(question.senior)
    ) for question in questions]

    return BaseResponse(code=200, message="조회 완료", data=question_list)

@router.get("/search", response_model=BaseResponse[list[GetQuestionList]])
async def search_question(keyword: str, db: Session = Depends(get_db)):
    questions = db.query(Question).order_by(Question.id.desc()).all()

    filtered_questions: list[Question] = __filter_similar_questions(questions, keyword, 55)

    question_list = [GetQuestionList(
        id=question.id,
        title=question.title,
        date=question.date,
        writer=__create_user_response(question.writer),
        senior=None if question.senior == None else __create_user_response(question.senior)
    ) for question in filtered_questions]

    return BaseResponse(code=200, message="조회 성공", data=question_list)

def __create_user_response(user: User):
    return UserResponse(
        id=user.id,
        email=user.email,
        username=user.username,
        description=user.description,
        major=user.major.split('|')
    )

def __filter_similar_questions(questions: list[Question], search_query, similarity_threshold) -> list[Question]:
    contents = [f"{question.title} {question.content}" for question in questions]

    results = process.extract(search_query, contents)

    similar_questions = []

    for result, score in results:
        if score >= similarity_threshold:
            similar_questions.append(questions[contents.index(result)])

    return similar_questions