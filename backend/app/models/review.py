from typing import Optional
from pydantic import BaseModel, Field

class ReviewBaseModel(BaseModel):
    title: Optional[str] = Field("Untitled", description='Title of the review')
    description: Optional[str] = Field("", description='Description of the review')
    rating: Optional[float] = Field(None, ge=0.0, le=1.0, description='Rating of the review')
    media_id: int = Field(..., description='ID of the media the review is about')
    reviewer_id: int = Field(..., description='ID of the user who made the review')

    class Config:
        from_attributes = True


class ReviewCreateModel(ReviewBaseModel):
    # no required id yet
    pass


class ReviewModel(ReviewBaseModel):
    pass


class ReviewUpdateModel(BaseModel):
    # composite identifier for the review to update
    media_id: int = Field(..., description='ID of the media the review is about')
    reviewer_id: int = Field(..., description='ID of the user who made the review')
    title: Optional[str] = Field(None, description='Title of the review')
    description: Optional[str] = Field(None, description='Description of the review')
    rating: Optional[float] = Field(None, ge=0.0, le=1.0, description='Rating of the review')

    class Config:
        from_attributes = True