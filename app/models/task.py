from app.backend.db import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.schema import CreateTable

# Используем forward reference вместо прямого импорта
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User


class Task(Base):
    __tablename__ = 'tasks'
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, default=0)
    title = Column(String)
    content = Column(String)
    priority = Column(Integer, default=0)
    completed = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    slug = Column(String, unique=True, index=True, nullable=True)
    user = relationship("User", back_populates="tasks")


# print(CreateTable(Task.__table__))
