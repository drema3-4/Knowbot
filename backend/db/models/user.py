from sqlalchemy import Column, Integer, String

from db.base import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    user_name = Column(String, nullable=False, unique=True)