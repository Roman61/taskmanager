from app.backend.db import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.schema import CreateTable

# Используем forward reference вместо прямого импорта
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .task import Task


class User(Base):
    __tablename__ = 'users'
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, default=0)
    username = Column(String)
    firstname = Column(String)
    lastname = Column(String)
    age = Column(Integer)
    slug = Column(String, unique=True, index=True, nullable=True)
    tasks = relationship("Task", back_populates="user")


# print(CreateTable(User.__table__))
