from sqlalchemy import Column, Integer
from db.base import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)