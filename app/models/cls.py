from typing import Optional
from surrealdb import RecordID
from pydantic import BaseModel


class Class(BaseModel):
    id: Optional[str]
    name: str
    teacher: str
    description: str
    category: str

    def to_model(self) -> "ClassModel":
        return ClassModel(
            id=None if self.id is None else RecordID("class", self.id),
            name=self.name,
            teacher=RecordID("teacher", self.teacher),
            description=self.description,
            category=self.category,
        )


class ClassModel(BaseModel, arbitrary_types_allowed=True):
    id: Optional[RecordID]
    name: str
    teacher: RecordID
    description: str
    category: str

    def to_raw(self) -> Class:
        return Class(
            id=self.id and self.id.id,
            name=self.name,
            teacher=self.teacher.id,
            description=self.description,
            category=self.category,
        )
