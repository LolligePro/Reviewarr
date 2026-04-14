from pydantic import BaseModel, Field, field_validator
from datetime import date

class MediaCreateModel(BaseModel):
    id: str = Field(..., min_length=1, description='ID of the media item')
    title: str = Field(..., min_length=1, description='Title of the media item')
    release_date: date = Field(..., description='Date of release of the media item')

    @field_validator('title')
    @classmethod
    def validate_title(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError('Title cannot be blank')
        return normalized