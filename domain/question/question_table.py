from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
import datetime
from globals.db import Base
from domain.question.comment_table import Comment
from domain.user.user_table import User


class Question(Base):
    __tablename__ = "question"
    __table_args__= {
        'mysql_engine':'InnoDB'
    }
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100))
    content = Column(Text)
    date = Column(TIMESTAMP, default=datetime.datetime.utcnow)
    
    writer_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE", onupdate="CASCADE"))
    senior_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=True)

    writer = relationship("User", back_populates="questions_writer", foreign_keys=[writer_id])
    senior = relationship("User", back_populates="questions_senior", foreign_keys=[senior_id])
    comments = relationship("Comment", back_populates="question")