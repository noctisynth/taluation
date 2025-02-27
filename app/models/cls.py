from typing import Optional
from surrealdb import RecordID
from pydantic import BaseModel


class Class(BaseModel):
    name: str
    teacher: str
    description: str
    category: str

    def to_model(self) -> "ClassModel":
        return ClassModel(
            id=None,
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
            name=self.name,
            teacher=self.teacher.id,
            description=self.description,
            category=self.category,
        )
