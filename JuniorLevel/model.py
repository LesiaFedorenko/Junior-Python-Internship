from datetime import datetime

from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.sqltypes import DateTime

Base = declarative_base()


class Appartment(Base):
    __tablename__ = "appartments"
    id = Column(Integer, primary_key=True, autoincrement=True)
    img_url = Column(String(250), nullable=False)
    title = Column(String(150), nullable=False)
    date = Column(DateTime, nullable=False)
    city = Column(String(150), nullable=False)
    bed=Column(String(150), nullable=False)
    description =Column(String(250), nullable=False)
    price = Column(String(150), nullable=False)
    