from pydantic import BaseModel


class UserEvent(BaseModel):
    source: str = "User"


class UserCreated(UserEvent):
    type: str = "UserCreated"
    id: str
    email: str
    validation_token: str


class UserVerified(UserEvent):
    type: str = "UserVerified"
    id: str
    email: str
