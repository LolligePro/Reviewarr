from fastapi import APIRouter, HTTPException
from sqlalchemy import func

from db import User, init_db
from models import UserModel, UserCreateModel, UserUpdateModel

router = APIRouter(prefix="/user", tags=["user"])
session = init_db()


@router.post("/create", response_model=UserModel)
def create_user(user: UserCreateModel):
    max_id = session.query(func.max(User.id)).scalar() or 0
    new_id = max_id + 1
    db_user = User(id=new_id, **user.model_dump())
    session.add(db_user)
    session.commit()
    return db_user


@router.post("/update", response_model=UserModel)
def update_user(user: UserUpdateModel):
    db_user = session.query(User).where(user.id == User.id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User does not exist")

    for field, value in user.model_dump(exclude_unset=True).items():
        setattr(db_user, field, value)

    session.commit()
    return db_user


@router.get("/get/{id}", response_model=UserModel)
def get_user(id: int):
    db_user = session.query(User).where(id == User.id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User does not exist")
    return db_user


@router.delete("/delete/{id}", response_model=UserModel)
def delete_user(id: int):
    db_user = session.query(User).where(id == User.id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User does not exist")
    session.delete(db_user)
    session.commit()
    return db_user
