from sqlalchemy import Column, Integer, Text, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
import datetime
from globals.db import Base

class Comment(Base):
    __tablename__ = "comment"
    __table_args__ = {
        'mysql_engine':'InnoDB'
    }

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)
    date = Column(TIMESTAMP, default=datetime.datetime.utcnow)

    writer_id = Column(Integer, ForeignKey("user.id"))
    question_id = Column(Integer, ForeignKey("question.id"))

    writer = relationship("User", back_populates="comments")
    question = relationship("Question", back_populates="comments")