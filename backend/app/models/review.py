from typing import Optional
from pydantic import BaseModel, Field, field_validator

class ReviewBaseModel(BaseModel):
    title: Optional[str] = Field("Untitled", min_length=1, description='Title of the review')
    description: Optional[str] = Field("", description='Description of the review')
    rating: Optional[float] = Field(None, ge=0.0, le=1.0, description='Rating of the review')
    media_id: str = Field(..., min_length=1, description='ID of the media the review is about')
    reviewer_id: str = Field(..., min_length=1, description='ID of the user who made the review')

    @field_validator('title')
    @classmethod
    def validate_title(cls, value: str) -> str:
        return value.strip()

    @field_validator('description')
    @classmethod
    def normalize_description(cls, value: str) -> str:
        return value.strip()

    class Config:
        from_attributes = True


class ReviewCreateModel(ReviewBaseModel):
    pass


class ReviewModel(ReviewBaseModel):
    pass


class ReviewUpdateModel(BaseModel):
    # composite identifier for the review to update
    media_id: str = Field(..., min_length=1, description='ID of the media the review is about')
    reviewer_id: str = Field(..., min_length=1, description='ID of the user who made the review')
    title: Optional[str] = Field(None, description='Title of the review')
    description: Optional[str] = Field(None, description='Description of the review')
    rating: Optional[float] = Field(None, ge=0.0, le=1.0, description='Rating of the review')

    @field_validator('title')
    @classmethod
    def validate_optional_title(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        normalized = value.strip()
        if not normalized:
            raise ValueError('Title cannot be blank')
        return normalized

    @field_validator('description')
    @classmethod
    def normalize_optional_description(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        return value.strip()

    class Config:
        from_attributes = True