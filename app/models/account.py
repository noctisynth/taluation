from surrealdb import RecordID
from typing import Optional
from pydantic import BaseModel


class Account(BaseModel):
    username: str
    password: str
    email: str
    phone: str


class AccountModel(BaseModel, arbitrary_types_allowed=True):
    id: Optional[RecordID]
    username: str
    password: str
    email: str
    phone: str


class Auth(BaseModel):
    username: str
    token: str
