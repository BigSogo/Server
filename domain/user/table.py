from sqlalchemy import Column, Integer, String, LargeBinary
from sqlalchemy.orm import relationship
from globals.db import Base

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    profile_img = Column(String(250))
    email = Column(String(50))
    username = Column(String(10))
    password = Column(String(100))
    description = Column(String(100))
    major = Column(String(100))

    profile = relationship("Profile", back_populates="user")
    questions_writer = relationship("Question", back_populates="writer", foreign_keys="[Question.writer_id]")
    questions_senior = relationship("Question", back_populates="senior", foreign_keys="[Question.senior_id]")
    comments = relationship("Comment", back_populates="writer")