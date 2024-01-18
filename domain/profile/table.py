from sqlalchemy import Column, Integer, Text, String, ForeignKey
from sqlalchemy.orm import relationship
from globals.db import Base

class Profile(Base):
    __tablename__ = "profile"
    __table_args__ = {
        'mysql_engine':'InnoDB'
    }

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship("User", back_populates="profile", uselist=False)
    major = Column(String(100))
    subject = Column(String(100))
    content = Column(Text)
    portfolio_url = Column(String(100))
