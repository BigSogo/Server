from fastapi import APIRouter, Depends, HTTPException
from http import HTTPStatus
from sqlalchemy.orm import Session
from thefuzz import process

from domain.question.table import Question
from domain.user.table import User
from domain.question.dto import CreateQuestion, GetQuestion, GetQuestionList
from domain.comment.dto import CommentDto
from domain.user.dto import create_user_response

from globals.base_response import BaseResponse
from globals.db import get_db
from globals.jwt import get_current_user

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
    
    writer = create_user_response(question.writer)

    senior = None if question.senior == None else create_user_response(question.senior)

    comments = [CommentDto(
        id=comment.id,
        content=comment.content,
        date=comment.date,
        writer=comment.writer
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
        content=question.content,
        date=question.date,
        writer=create_user_response(question.writer),
        senior=None if question.senior == None else create_user_response(question.senior)
    ) for question in questions]

    return BaseResponse(code=200, message="조회 완료", data=question_list)

@router.get("/my", response_model=BaseResponse[list[GetQuestionList]])
async def get_my_question(db: Session = Depends(get_db), user_data: User = Depends(get_current_user)):
    questions = db.query(Question).filter(Question.writer_id == user_data.id).all()

    question_list = [GetQuestionList( 
        id=question.id,
        title=question.title,
        content=question.content,
        date=question.date,
        writer=create_user_response(question.writer),
        senior=None if question.senior == None else create_user_response(question.senior)
    ) for question in questions]

    return BaseResponse(code=200, message="조회 성공", data=question_list)

@router.get("/search", response_model=BaseResponse[list[GetQuestionList]])
async def search_question(keyword: str, db: Session = Depends(get_db)):
    questions = db.query(Question).order_by(Question.id.desc()).all()

    filtered_questions: list[Question] = __filter_similar_questions(questions, keyword, 55)

    question_list = [GetQuestionList(
        id=question.id,
        title=question.title,
        content=question.content,
        date=question.date,
        writer=create_user_response(question.writer),
        senior=None if question.senior == None else create_user_response(question.senior)
    ) for question in filtered_questions]

    return BaseResponse(code=200, message="조회 성공", data=question_list)

@router.put("/{question_id}", response_model=BaseResponse[None])
async def update_question(question_id: int, request: CreateQuestion, db: Session = Depends(get_db), user_data: User = Depends(get_current_user)):
    question = db.query(Question).get(question_id)
    if question is None:
        raise HTTPException(404, "데이터를 찾을 수 없습니다.")
    if question.writer_id == user_data.id:
        raise HTTPException(403, "권한이 없습니다")

    question.title = request.title
    question.content = request.content
    question.senior_id = request.senior_id

    db.commit()
    return BaseResponse(code=HTTPStatus.OK, message="수정 완료")

@router.delete("/{question_id}", response_model=BaseResponse[None])
async def delete_question(question_id: int, db: Session = Depends(get_db), user_data: User = Depends(get_current_user)):
    question = db.query(Question).get(question_id)
    if question is None:
        raise HTTPException(404, "데이터를 찾을 수 없습니다.")
    if question.writer == user_data.id:
        raise HTTPException(403, "권한이 없습니다")

    db.delete(question)
    db.commit()
    return BaseResponse(code=HTTPStatus.OK, message="삭제 완료")

def __filter_similar_questions(questions: list[Question], search_query, similarity_threshold) -> list[Question]:
    contents = [f"{question.title} {question.content}" for question in questions]

    results = process.extract(search_query, contents)

    similar_questions = []

    for result, score in results:
        if score >= similarity_threshold:
            similar_questions.append(questions[contents.index(result)])

    return similar_questions