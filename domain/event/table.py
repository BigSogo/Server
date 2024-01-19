from sqlalchemy import Column, Integer, Text
from globals.db import Base

class Event(Base):
    __tablename__ = "event"
    __table_args__ = {
        'mysql_engine':'InnoDB'
    }

    id = Column(Integer, primary_key=True, index=True)
    image_url = Column(Text)
