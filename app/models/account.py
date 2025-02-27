from surrealdb import RecordID
from typing import Literal, Optional
from pydantic import BaseModel


class Account(BaseModel):
    id: Optional[str]
    username: str
    password: str
    email: str
    phone: str
    type: Literal["student", "teacher", "admin"]

    def to_model(self):
        return AccountModel(
            id=None if self.id is None else RecordID("account", self.id),
            username=self.username,
            password=self.password,
            email=self.email,
            phone=self.phone,
            type=self.type,
        )


class AccountModel(BaseModel, arbitrary_types_allowed=True):
    id: Optional[RecordID]
    username: str
    password: str
    email: str
    phone: str
    type: Literal["student", "teacher", "admin"]

    def to_raw(self):
        return Account(
            id=self.id and self.id.id,
            username=self.username,
            password=self.password,
            email=self.email,
            phone=self.phone,
            type=self.type,
        )


class Auth(BaseModel):
    username: str
    token: str


class Credentials(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    token: str
