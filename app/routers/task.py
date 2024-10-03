from fastapi import APIRouter, Depends, status, HTTPException
# Сессия БД
from sqlalchemy.orm import Session
# Функция подключения к БД
from app.backend.db_depends import get_db
# Аннотации, Модели БД и Pydantic.
from typing import Annotated
from app.models.task import Task
from app.schemas import CreateUser, UpdateUser
# Функции работы с записями.
from sqlalchemy import insert, select, update, delete
# Функция создания slug-строки
from slugify import slugify
from app.schemas import CreateTask

router = APIRouter(prefix="/task", tags=["task"])


@router.get("/")
async def get_all_tasks(db: Annotated[Session, Depends(get_db)]):
    tasks = db.scalars(select(Task).where(Task.completed == False)).all()
    if tasks is None:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There are no task'
        )
    return tasks


@router.get("/task_id")
async def task_by_id():
    pass


@router.post("/create")
async def create_task(db: Annotated[Session, Depends(get_db)], createtask: CreateTask, user_id):
    if user_id:
        db.execute(insert(Task).values(title=createtask.title,
                                        content=createtask.content,
                                        priority=createtask.priority,
                                        user_id=user_id,
                                        slug=slugify(createtask.title)))
        db.commit()
        return {
            'status_code': status.HTTP_201_CREATED,
            'transaction': 'Successful'
        }
    else:
        return {
            'status_code': status.HTTP_404_NOT_FOUND,
            'transaction': 'User was not found'
        }


@router.put("/update")
async def update_task():
    pass


@router.delete("/delete")
async def delete_task(db: Annotated[Session, Depends(get_db)], task_id: int):
    task = db.scalar(select(Task).where(Task.id == task_id))
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There is no category found'
        )
    db.execute(update(Task).where(Task.id == task_id).values(is_active=False))
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Category delete is successful'
    }
