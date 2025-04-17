from surrealdb import RecordID
from typing import Literal, Optional, Union, Any, List, TypeVar, Dict
from pydantic import BaseModel, field_validator


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
    
    @field_validator('id', mode='before')
    @classmethod
    def validate_id(cls, v: Any) -> Optional[str]:
        if v is None:
            return None
        if isinstance(v, str):
            return v
        if hasattr(v, 'id'):
            return str(v.id)
        return str(v)


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

    def to_response(self):
        return AccountResponse(
            id=self.id and self.id.id,
            username=self.username,
            email=self.email,
            phone=self.phone,
            type=self.type
        )

class Auth(BaseModel):
    username: str
    token: str


class Credentials(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    token: str


class ChangePassword(BaseModel):
    oldpassword: str
    newpassword: str


class UpdateAccount(BaseModel):
    username: str
    newname: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    type: Optional[Literal["student", "teacher", "admin"]] = None


class AccountResponse(BaseModel):
    id: Optional[str] = None
    username: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    type: Optional[Literal["student", "teacher", "admin"]] = None

    def retain_id_only(self):
        return AccountResponse(
            id=self.id,
            username=None,
            email=None,
            phone=None,
            type=None
        )
