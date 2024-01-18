from sqlalchemy import Column, Integer, Text, String
from sqlalchemy.orm import relationship
from globals.db import Base

class Profile(Base):
    __tablename__ = "profile"
    __table_args__ = {
        'mysql_engine':'InnoDB'
    }

    id = Column(Integer, primary_key=True, index=True)
    user = relationship("User", back_populates="profile", uselist=False)
    major = Column(Text)
    subject = Column(String(100))
    content = Column(Text)
    portfolio_url = Column(String(100))
    tag = Column(String(100))
