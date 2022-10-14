from pydantic import BaseModel


class UserBase(BaseModel):
    email: str


class UserIn(UserBase):
    password: str


class UserOut(UserBase):
    is_active: bool
    email_validated: bool

    class Config:
        orm_mode = True
