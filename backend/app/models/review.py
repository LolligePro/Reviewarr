from typing import Optional
from pydantic import BaseModel, Field

class ReviewBaseModel(BaseModel):
    title: Optional[str] = Field("Untitled", description='Title of the review')
    description: Optional[str] = Field("", description='Description of the review')
    rating: Optional[float] = Field(None, ge=0.0, le=1.0, description='Rating of the review')
    media_id: int = Field(..., description='ID of the media that is being reviewed')
    reviewer_id: int = Field(..., description='ID of the user that is creating the review')

    class Config:
        from_attributes = True


class ReviewCreateModel(ReviewBaseModel):
    pass


class ReviewUpdateModel(ReviewBaseModel):
    pass


class ReviewModel(ReviewBaseModel):
    id: int = Field(..., description='ID of the review')

