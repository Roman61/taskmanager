from fastapi import APIRouter, Depends, status, HTTPException, Query, Body
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.backend.db_depends import get_db
from typing import Annotated
from app.models.task import Task
from app.models.user import User
from app.schemas import CreateUser, UpdateUser, UpdateTask
from sqlalchemy import insert, select, update, delete, func
from slugify import slugify
from app.schemas import CreateTask

router = APIRouter(prefix="/task", tags=["task"])


async def get_current_user(db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == 1).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


@router.get("/")
async def get_all_tasks(db: Annotated[Session, Depends(get_db)]):
    try:
        tasks = db.scalars(select(Task).where(Task.completed == False)).all()
        if not tasks:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="There are no tasks"
            )
        return tasks
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )


@router.get("/task_id")
async def task_by_id(task_id: int, db: Session = Depends(get_db)):
    try:
        task = db.scalars(select(Task).where(Task.id == task_id)).first()
        if task is None:
            raise HTTPException(status_code=404, detail="Task was not found")
        return task
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_task(user_id: int, task: CreateTask, db: Session = Depends(get_db)):
    try:
        user = db.scalar(select(User).where(User.id == user_id))
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User was not found")

        max_id = db.scalars(
            select(func.max(Task.id))
        ).first()
        if max_id is None:
            max_id = 0
        new_id = max_id + 1

        slug = slugify(task.title)
        existing_task = db.scalar(select(Task).where(Task.slug == slug))
        if existing_task:
            slug = f"{slug}-{new_id}"

        new_task = Task(
            id=new_id,
            title=task.title,
            content=task.content,
            priority=task.priority,
            user_id=user.id,
            slug=slug,
        )
        db.add(new_task)
        db.commit()
        db.refresh(new_task)
        return {"status_code": status.HTTP_201_CREATED, "transaction": "Successful"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}",
        )


@router.put("/update")
async def update_task(task_id: int, user_id: int, updated_task: UpdateTask, db: Session = Depends(get_db)):
    try:
        task_to_update = db.scalars(select(Task).where(Task.id == task_id)).first()
        if task_to_update is None:
            raise HTTPException(status_code=404, detail="Task was not found")
        db.execute(
            update(Task).where(Task.id == task_id).values(
                title=updated_task.title,
                content=updated_task.content,
                priority=updated_task.priority,
                completed=False,
                user_id=user_id,
                slug=updated_task.title
            )
        )
        db.commit()
        return {
            'status_code': status.HTTP_200_OK,
            'transaction': 'Task update is successful!'
        }
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )


@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int, db: Session = Depends(get_db)):
    try:
        task = db.get(Task, task_id)
        if task:
            db.delete(task)
            db.commit()
            return {"status_code": status.HTTP_204_NO_CONTENT, "transaction": "Successful"}
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}",
        )