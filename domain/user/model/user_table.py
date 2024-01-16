from sqlalchemy import Column, Integer, String, TEXT
from globals.db import Base

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(50))
    username = Column(String(10))
    password = Column(String(100))
    description = Column(TEXT)
    major = Column(String(50))