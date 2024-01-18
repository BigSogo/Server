from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

from dotenv import load_dotenv
import redis
import os

load_dotenv()

user_name = os.getenv('USER_NAME')
user_pwd = os.getenv("USER_PWD")
db_host = os.getenv("DB_HOST")
db_name = os.getenv("DB_NAME")

REDIS_HOST: str = os.getenv("REDIS_HOST")
REDIS_PORT: int = os.getenv("REDIS_PORT")
REDIS_DATABASE: int = os.getenv("REDIS_DATABASE")

pool = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DATABASE, decode_responses=True)


DATABASE =  'mariadb+pymysql://%s:%s@%s/%s?charset=utf8' % (
    user_name,
    user_pwd,
    db_host,
    db_name
)

ENGINE = create_engine(
    DATABASE,
    echo=True
)

session = scoped_session(
    sessionmaker(
        autocommit = False,
        autoflush = False,
        bind = ENGINE
    )
)

def get_db():
    try:
        yield session
    finally:
        session.close()

def get_redis():
    return pool

Base = declarative_base()
Base.query = session.query_property()

metadata = MetaData()