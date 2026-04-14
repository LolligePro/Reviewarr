from typing import Optional
from pydantic import BaseModel, Field, field_validator

class UserBaseModel(BaseModel):
    username: str = Field(..., min_length=1, description='Username of the user')

    @field_validator('username')
    @classmethod
    def validate_username(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError('Username cannot be blank')
        return normalized

    class Config:
        from_attributes = True


class UserCreateModel(UserBaseModel):
    # no required id yet
    pass


class UserModel(UserBaseModel):
    id: int = Field(..., ge=1, description='ID of the user')


class UserUpdateModel(BaseModel):
    # all optional except id
    id: int = Field(..., ge=1, description='ID of the user')
    username: Optional[str] = Field(None, description='Username of the user')

    @field_validator('username')
    @classmethod
    def validate_optional_username(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        normalized = value.strip()
        if not normalized:
            raise ValueError('Username cannot be blank')
        return normalized

    class Config:
        from_attributes = True