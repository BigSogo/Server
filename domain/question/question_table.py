from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
import datetime
from globals.db import Base


class Question(Base):
    __tablename__ = "question"
    __table_args__= {
        'mysql_engine':'InnoDB'
    }
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100))
    content = Column(Text)
    date = Column(TIMESTAMP, default=datetime.datetime.utcnow)
    
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE", onupdate="CASCADE"))
    user = relationship("User", back_populates="questions")