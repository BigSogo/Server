from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from domain.comment.dto import CreateComment, UpdateComment
from domain.user.table import User
from domain.comment.table import Comment

from globals.base_response import BaseResponse
from globals.jwt import get_current_user
from globals.db import get_db

router = APIRouter()

@router.post("", response_model=BaseResponse[None])
async def craete_comment(comment: CreateComment, db: Session = Depends(get_db), user_data: User = Depends(get_current_user)):
    new_comment = Comment(
        content=comment.content,
        question_id=comment.question_id,
        writer_id=user_data.id
    )

    db.add(new_comment)
    db.commit()

    return BaseResponse(code=200, message="생성 완료")

@router.put("", response_model=BaseResponse[None])
async def update_comment(comment_data: UpdateComment, db: Session = Depends(get_db), user_data: User = Depends(get_current_user)):
    comment = db.query(Comment).get(comment_data.comment_id)
    
    if user_data.id != comment.writer_id:
        HTTPException(403, "권한이 없습니다")
    if comment:
        HTTPException(404, "찾을 수 없습니다")

    comment.content = comment_data.content

    db.commit()

    return BaseResponse(code=200, message="수정 완료")

@router.delete("/{comment_id}", response_model=BaseResponse[None])
async def delete_comment(comment_id: int, db: Session = Depends(get_db), user_data: User = Depends(get_current_user)):
    comment = db.query(Comment).get(comment_id)

    if comment:
        HTTPException(404, "찾을 수 없습니다")
    if comment.writer_id == user_data.id:
        HTTPException(403, "권한이 없습니다")

    db.delete(comment)
    db.commit()

    return BaseResponse(code=200, message="삭제 완료")
