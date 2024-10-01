from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, create_engine

Base = declarative_base()


class CreateUser(Base):
    __tablename__ = "User"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    firstname = Column(String)
    lastname = Column(String)
    age = Column(Integer)


class UpdateUser(Base):
    __tablename__ = "UpdateUser"
    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String)
    lastname = Column(String)
    age = Column(Integer)


class CreateTask(Base):
    __tablename__ = "Task"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(String)
    priority = Column(Integer)


class UpdateTask(Base):
    __tablename__ = "UpdateTask"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(String)
    priority = Column(Integer)


class DBEngine:
    def __init__(self):
        self.sqlite_database = "sqlite:///metanit.db"
        self.engine = create_engine(self.sqlite_database)
        Base.metadata.create_all(bind=self.engine)


if __name__ == "__main__":
    db_engine = DBEngine()
