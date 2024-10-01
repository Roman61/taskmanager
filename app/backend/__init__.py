from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy import Integer, Column, String


engine = create_engine("sqlite:///taskmanager.db", echo=True)
SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase): ...


