from surrealdb import RecordID
from typing import Literal, Optional
from pydantic import BaseModel


class Account(BaseModel):
    username: str
    password: str
    email: str
    phone: str
    type: Literal["student", "teacher", "admin"]


class AccountModel(BaseModel, arbitrary_types_allowed=True):
    id: Optional[RecordID]
    username: str
    password: str
    email: str
    phone: str
    type: Literal["student", "teacher", "admin"]


class Auth(BaseModel):
    username: str
    token: str
