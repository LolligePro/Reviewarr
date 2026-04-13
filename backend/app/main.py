from fastapi import FastAPI
from sqlalchemy import func
from db import init_db, Review, User, Media
from models import ReviewModel, ReviewCreateModel, ReviewUpdateModel

api = FastAPI()  # init FastAPI
session = init_db()  # init SQLite database

@api.post("/user/")
async def create_user(id: int, username: str):
    session.add(User(
        id=id,
        username=username,
    ))
    session.commit()
    return 'Success'

@api.post("/media/")
async def create_media(id: int, title: str):
    session.add(Media(
        id=id,
        title=title,
        release_date=func.now(),
    ))
    session.commit()
    return 'Success'

@api.post("/reviews/")
async def create_review(review: ReviewCreateModel):
    max_id = session.query(func.max(Review.id)).scalar() or 0
    new_id = max_id + 1 if max_id else 0
    session.add(Review(
        id=new_id,
        title=review.title,
        description=review.description,
        rating=review.rating,
        reviewer_id=review.reviewer_id,
        media_id=review.media_id,
    ))
    await session.commit()
    return 'Success'

@api.get("/reviews/")
async def get_reviews():
    return session.query(Review).all()
