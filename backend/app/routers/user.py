from fastapi import APIRouter, HTTPException, Path
from sqlalchemy.exc import IntegrityError
from uuid import uuid4

from db import User, init_db
from models import UserModel, UserCreateModel, UserUpdateModel

router = APIRouter(prefix="/user", tags=["user"])
session = init_db()


@router.post("/create", response_model=UserModel)
def create_user(user: UserCreateModel):
    db_user = User(id=str(uuid4()), **user.model_dump())
    session.add(db_user)
    try:
        session.commit()
    except IntegrityError as exc:
        session.rollback()
        raise HTTPException(status_code=409, detail="Request violates database constraints") from exc
    return db_user


@router.post("/update", response_model=UserModel)
def update_user(user: UserUpdateModel):
    update_data = user.model_dump(exclude_unset=True, exclude={"id"})
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields provided to update")

    db_user = session.query(User).where(user.id == User.id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User does not exist")

    for field, value in update_data.items():
        setattr(db_user, field, value)

    try:
        session.commit()
    except IntegrityError as exc:
        session.rollback()
        raise HTTPException(status_code=409, detail="Request violates database constraints") from exc
    return db_user


@router.get("/get/{id}", response_model=UserModel)
def get_user(id: str = Path(..., min_length=1)):
    db_user = session.query(User).where(id == User.id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User does not exist")
    return db_user


@router.delete("/delete/{id}", response_model=UserModel)
def delete_user(id: str = Path(..., min_length=1)):
    db_user = session.query(User).where(id == User.id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User does not exist")
    session.delete(db_user)
    try:
        session.commit()
    except IntegrityError as exc:
        session.rollback()
        raise HTTPException(status_code=409, detail="Request violates database constraints") from exc
    return db_user
