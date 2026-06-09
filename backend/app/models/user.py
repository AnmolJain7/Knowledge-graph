from sqlalchemy import Column, Integer, String

from app.core.database import base

class User(base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100),nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String(20),nullable=False)
    address = Column(String(255),nullable=False)

    phone_number = Column(String(15),unique=True,nullable=False)
