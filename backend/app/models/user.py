from typing import Optional
from pydantic import BaseModel, Field

class UserBaseModel(BaseModel):
    username: str = Field(..., description='Username of the user')

    class Config:
        from_attributes = True


class UserCreateModel(UserBaseModel):
    # no required id yet
    pass


class UserModel(UserBaseModel):
    id: int = Field(..., description='ID of the user')


class UserUpdateModel(BaseModel):
    # all optional except id
    id: int = Field(..., description='ID of the user')
    username: Optional[str] = Field(None, description='Username of the user')

    class Config:
        from_attributes = True