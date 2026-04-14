from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import IntegrityError
from db import Media, init_db
from models import MediaCreateModel

router = APIRouter(prefix="/media", tags=["media"])
session = init_db()


# TODO: TEMP, to be replaced by seerr webhooks
@router.post("/create")
def create_media(media: MediaCreateModel):
    if session.query(Media).where(Media.id == media.id).first():
        raise HTTPException(status_code=409, detail="Media already exists")

    media_db = Media(**media.model_dump())
    session.add(media_db)
    try:
        session.commit()
    except IntegrityError as exc:
        session.rollback()
        raise HTTPException(status_code=409, detail="Request violates database constraints") from exc
    return 'Success'
