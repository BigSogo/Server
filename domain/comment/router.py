from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from domain.comment.dto import CreateComment
from domain.user.table import User
from domain.comment.table import Comment

from globals.base_response import BaseResponse
from globals.jwt import get_current_user
from globals.db import get_db

router = APIRouter()

@router.post("", response_model=BaseResponse[None])
async def craete_comment(comment: CreateComment, db: Session = Depends(get_db), user_data: User = Depends(get_current_user)):
    pass