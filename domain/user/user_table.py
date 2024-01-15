from sqlalchemy import Column, Integer, String
from globals.db import Base


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String)
    password = Column(String)
    name = Column(String)
    description = Column(String)
    major = Column(String)