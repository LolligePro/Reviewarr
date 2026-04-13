from fastapi import FastAPI, HTTPException
from sqlalchemy import func
from db import init_db, Review, User, Media
from models import ReviewModel, ReviewCreateModel, ReviewUpdateModel

api = FastAPI()  # init FastAPI
session = init_db()  # init SQLite database


@api.post("/user/create")
def create_user(id: int, username: str):
    if session.query(User).where(User.id == id).first():
        raise HTTPException(status_code=400, detail="User already exists")
    session.add(User(
        id=id,
        username=username,
    ))
    session.commit()
    return 'Success'


@api.post("/media/create")
def create_media(id: int, title: str):
    if session.query(Media).where(Media.id == id).first():
        raise HTTPException(status_code=400, detail="Media already exists")
    session.add(Media(
        id=id,
        title=title,
        release_date=func.now(),
    ))
    session.commit()
    return 'Success'


@api.post("/review/create", response_model=ReviewModel)
def create_review(review: ReviewCreateModel):
    if not session.query(User).where(User.id == review.reviewer_id).first():
        raise HTTPException(status_code=404, detail="User does not exist")
    if not session.query(Media).where(Media.id == review.media_id).first():
        raise HTTPException(status_code=404, detail="Media does not exist")
    max_id = session.query(func.max(Review.id)).scalar() or 0
    new_id = max_id + 1
    db_review = Review(id=new_id, **review.model_dump())
    session.add(db_review)
    session.commit()
    return db_review


@api.post("/review/update", response_model=ReviewModel)
def update_review(review: ReviewUpdateModel):
    db_review = session.query(Review).where(review.id == Review.id).first()
    if not db_review:
        raise HTTPException(status_code=404, detail="Review does not exist")

    if review.reviewer_id is not None and not session.query(User).where(User.id == review.reviewer_id).first():
        raise HTTPException(status_code=404, detail="User does not exist")

    if review.media_id is not None and not session.query(Media).where(Media.id == review.media_id).first():
        raise HTTPException(status_code=404, detail="Media does not exist")

    for field, value in review.model_dump(exclude_unset=True).items():
        setattr(db_review, field, value)

    session.commit()
    return db_review

@api.get("/review/get/{id}", response_model=ReviewModel)
def get_review(id: int):
    db_review = session.query(Review).where(id == Review.id).first()
    if not db_review:
        raise HTTPException(status_code=404, detail="Review does not exist")
    return db_review

@api.delete("/review/delete/{id}", response_model=ReviewModel)
def delete_review(id: int):
    db_review = session.query(Review).where(id == Review.id).first()
    if not db_review:
        raise HTTPException(status_code=404, detail="Review does not exist")
    session.delete(db_review)
    session.commit()
    return db_review
