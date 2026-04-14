import ast
from datetime import date, datetime
from typing import Any

from fastapi import APIRouter, Body, HTTPException
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError
from db import Media, Review, User, init_db
from models import JellyfinWebhookPayload


router = APIRouter(prefix="/webhook", tags=["webhook"])
session = init_db()


def _as_bool(value) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() == "true"
    return False


def _parse_release_date(year_value, timestamp_value) -> date:
    if year_value is not None:
        year = str(year_value).strip()
        if year.isdigit() and len(year) == 4:
            return date(int(year), 1, 1)

    if isinstance(timestamp_value, datetime):
        return timestamp_value.date()

    if timestamp_value:
        timestamp = str(timestamp_value).strip()
        try:
            return datetime.fromisoformat(timestamp.replace("Z", "+00:00")).date()
        except ValueError:
            pass

    return date(1970, 1, 1)


def _coerce_payload(
    payload: JellyfinWebhookPayload | dict[str, Any] | str | bytes,
) -> JellyfinWebhookPayload:
    """Converts the received payload into a JellyfinWebhookPayload"""
    if isinstance(payload, JellyfinWebhookPayload):
        return payload

    if isinstance(payload, dict):
        try:
            return JellyfinWebhookPayload.model_validate(payload)
        except ValidationError as exc:
            raise HTTPException(status_code=422, detail="Invalid webhook payload") from exc

    if isinstance(payload, bytes):
        raw_text = payload.decode("utf-8", errors="replace")
    else:
        raw_text = payload

    try:
        return JellyfinWebhookPayload.model_validate_json(raw_text)
    except ValidationError:
        # Some senders post Python-literal booleans (True/False) instead of strict JSON.
        try:
            parsed_payload = ast.literal_eval(raw_text)
            return JellyfinWebhookPayload.model_validate(parsed_payload)
        except (ValueError, SyntaxError, ValidationError) as exc:
            raise HTTPException(status_code=422, detail="Invalid webhook payload") from exc


@router.post("/jellyfin")
def process_jellyfin_webhook(
    payload: JellyfinWebhookPayload | dict[str, Any] | str | bytes = Body(...),
):
    payload = _coerce_payload(payload)
    session_payload = payload.Session
    if not _as_bool(session_payload.PlayedToCompletion):
        return {"status": "ignored", "reason": "Playback was not completed"}

    user_id = str(session_payload.UserId or "").strip()
    if not user_id:
        raise HTTPException(status_code=422, detail="Missing Session.UserId")

    username = str(session_payload.User or "").strip() or f"user-{user_id}"

    media_payload = payload.Media
    media_id = str(media_payload.ExternalIds.IMDB or "").strip()
    if not media_id:
        raise HTTPException(status_code=422, detail="Missing Media.ExternalIds.IMDB")

    title = (
        str(media_payload.Title or "").strip()
        or str(media_payload.EpisodeTitle or "").strip()
        or "Unknown Title"
    )
    release_date = _parse_release_date(media_payload.Year, payload.Timestamp)

    if not session.query(User).where(User.id == user_id).first():
        session.add(User(id=user_id, username=username))

    if not session.query(Media).where(Media.id == media_id).first():
        session.add(Media(id=media_id, title=title, release_date=release_date))

    if not session.query(Review).where(
        Review.media_id == media_id,
        Review.reviewer_id == user_id,
    ).first():
        session.add(
            Review(
                reviewer_id=user_id,
                media_id=media_id,
                title="Untitled",
                description="",
                rating=None,
            )
        )

    try:
        session.commit()
    except IntegrityError as exc:
        session.rollback()
        raise HTTPException(status_code=409, detail="Request violates database constraints") from exc

    return {
        "status": "processed",
        "user_id": user_id,
        "media_id": media_id,
    }
