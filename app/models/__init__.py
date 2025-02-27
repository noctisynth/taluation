from typing import Generic, Optional, TypeVar
from pydantic import BaseModel
from .account import Account as Account


T = TypeVar("T")


class Response(BaseModel, Generic[T]):
    message: str
    data: Optional[T] = None
    success: bool

    def __init__(self, message: str, data: Optional[T] = None, success: bool = True):
        super().__init__(message=message, data=data, success=success)


class Record(BaseModel):
    id: str
