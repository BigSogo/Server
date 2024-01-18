from sqlalchemy import Column, Integer
from globals.db import Base

class Comment(Base):
    __tablename__ = "profile"
    __table_args__ = {
        'mysql_engine':'InnoDB'
    }

    id = Column(Integer, primary_key=true)