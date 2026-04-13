from fastapi import APIRouter, HTTPException
from datetime import date
from db import Media, init_db

router = APIRouter(prefix="/media", tags=["media"])
session = init_db()


# TODO: TEMP, to be replaced by seerr webhooks
@router.post("/create")
def create_media(id: int, title: str):
    if session.query(Media).where(Media.id == id).first():
        raise HTTPException(status_code=400, detail="Media already exists")
    session.add(Media(
        id=id,
        title=title,
        release_date=date.today(),
    ))
    session.commit()
    return 'Success'
