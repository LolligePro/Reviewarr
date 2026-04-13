from fastapi import APIRouter, HTTPException
from sqlalchemy import func
from db import Review, User, Media, init_db
from models import ReviewModel, ReviewCreateModel, ReviewUpdateModel

router = APIRouter(prefix="/review", tags=["review"])
session = init_db()

@router.post("/create", response_model=ReviewModel)
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

@router.post("/update", response_model=ReviewModel)
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

@router.get("/get/{id}", response_model=ReviewModel)
def get_review(id: int):
    db_review = session.query(Review).where(id == Review.id).first()
    if not db_review:
        raise HTTPException(status_code=404, detail="Review does not exist")
    return db_review

@router.delete("/delete/{id}", response_model=ReviewModel)
def delete_review(id: int):
    db_review = session.query(Review).where(id == Review.id).first()
    if not db_review:
        raise HTTPException(status_code=404, detail="Review does not exist")
    session.delete(db_review)
    session.commit()
    return db_review

