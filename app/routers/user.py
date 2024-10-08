from sqlite3 import IntegrityError
from sqlalchemy import func
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.backend.db_depends import get_db
from typing import Annotated
from app.models.task import Task
from app.models.user import User
from app.schemas import CreateUser, UpdateUser
from sqlalchemy import insert, select, update, delete

router = APIRouter(prefix="/user", tags=["user"])


@router.get("/")
async def get_all_users(db: Session = Depends(get_db)):
    users = db.scalars(select(User).where(User.id > 0)).all()
    if users is None:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There are no product'
        )
    return users


@router.get('/user_id/{user_id}')
def user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db.scalars(
        select(User).where(User.id == user_id)
    ).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User was not found")
    return user


@router.post('/create')
def create_user(new_user: CreateUser, db: Session = Depends(get_db)):
    try:
        max_id = db.scalars(
            select(func.max(User.id))
        ).first()
        if max_id is None:
            max_id = 0
        new_id = max_id + 1
        db.execute(
            insert(User).values(
                id=new_id,
                username=new_user.username,
                firstname=new_user.firstname,
                lastname=new_user.lastname,
                age=new_user.age,
                slug=new_user.username
            )
        )
        db.commit()
        return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}
    except IntegrityError:
        raise HTTPException(status_code=400, detail="User with this user_id or username already exists")


@router.patch('/update/{user_id}')
def update_user(user_id: int, updated_user: UpdateUser, db: Session = Depends(get_db)):
    user_to_update = db.scalars(
        select(User).where(User.id == user_id)
    ).first()
    if user_to_update is None:
        raise HTTPException(status_code=404, detail="User was not found")
    db.execute(
        update(User).where(User.id == user_id).values(
            username=updated_user.username,
            firstname=updated_user.firstname,
            lastname=updated_user.lastname,
            age=updated_user.age,
            slug=updated_user.username
        )
    )
    db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'User update is successful!'}


@router.delete('/delete/{user_id}')
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user_to_delete = db.scalars(
        select(User).where(User.id == user_id)
    ).first()
    if user_to_delete is None:
        raise HTTPException(status_code=404, detail="User was not found")

    # Удалить все задачи, связанные с пользователем
    tasks = db.scalars(select(Task).where(Task.user_id == user_id)).all()
    for task in tasks:
        db.delete(task)

    db.delete(user_to_delete)
    db.commit()

    return {'status_code': status.HTTP_200_OK, 'transaction': 'User delete is successful!'}


@router.delete("/delete")
async def delete_user(db: Annotated[Session, Depends(get_db)], user_id: int):
    try:
        user = db.scalar(select(User).where(User.id == user_id))
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='User not found'
            )
        tasks = db.scalars(select(Task).where(Task.user_id == user_id)).all()
        for task in tasks:
            db.delete(task)
        db.delete(user)
        db.commit()
        return {
            'status_code': status.HTTP_200_OK,
            'transaction': 'User delete is successful'
        }
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )


@router.get("/user_id/tasks")
async def tasks_by_user_id(user_id: int, db: Session = Depends(get_db)):
    try:
        user = db.scalar(select(User).where(User.id == user_id))
        if user is None:
            raise HTTPException(
                status_code=404,
                detail=f"User with id {user_id} not found"
            )
        tasks = db.scalars(select(Task).where(Task.user_id == user_id)).all()
        return tasks
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving tasks: {str(e)}"
        )
