from fastapi import APIRouter, HTTPException
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
    if session.query(Review).where(
            Review.media_id == review.media_id,
            Review.reviewer_id == review.reviewer_id,
    ).first():
        raise HTTPException(status_code=409, detail="Review already exists")

    db_review = Review(**review.model_dump())
    session.add(db_review)
    session.commit()
    return db_review


@router.post("/update", response_model=ReviewModel)
def update_review(review: ReviewUpdateModel):
    db_review = session.query(Review).where(
        Review.media_id == review.media_id,
        Review.reviewer_id == review.reviewer_id,
    ).first()
    if not db_review:
        raise HTTPException(status_code=404, detail="Review does not exist")

    for field, value in review.model_dump(exclude_unset=True, exclude={"media_id", "reviewer_id"}).items():
        setattr(db_review, field, value)

    session.commit()
    return db_review


@router.get("/get/{media_id}/{reviewer_id}", response_model=ReviewModel)
def get_review(media_id: int, reviewer_id: int):
    db_review = session.query(Review).where(
        Review.media_id == media_id,
        Review.reviewer_id == reviewer_id,
    ).first()
    if not db_review:
        raise HTTPException(status_code=404, detail="Review does not exist")
    return db_review


@router.delete("/delete/{media_id}/{reviewer_id}", response_model=ReviewModel)
def delete_review(media_id: int, reviewer_id: int):
    db_review = session.query(Review).where(
        Review.media_id == media_id,
        Review.reviewer_id == reviewer_id,
    ).first()
    if not db_review:
        raise HTTPException(status_code=404, detail="Review does not exist")
    session.delete(db_review)
    session.commit()
    return db_review
