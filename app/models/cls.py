from typing import Optional, Any
from surrealdb import RecordID
from pydantic import BaseModel, field_validator


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
            teacher=RecordID("account", self.teacher),
            description=self.description,
            category=self.category,
        )
    
    def to_list(self) -> "DisplayClass":
        return DisplayClass(
            name=self.name,
            teacher=self.teacher,
            category=self.category,
            description=self.description,
        )
    
    @field_validator('teacher', mode='before')
    @classmethod
    def validate_teacher(cls, v: Any) -> str:
        if hasattr(v, 'id'):
            return v.id
        return v
    
    @field_validator('id', mode='before')
    @classmethod
    def validate_id(cls, v: Any) -> Optional[str]:
        if v is None:
            return None
        if hasattr(v, 'id'):
            return v.id


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


class CreateClass(BaseModel):
    name: str
    teacher: Optional[str] = None
    description: str
    category: str

    def to_model(self, teacher_id: Optional[str] = None) -> "ClassModel":
        return ClassModel(
            id=None,
            name=self.name,
            teacher=RecordID("account", teacher_id or self.teacher),
            description=self.description,
            category=self.category,
        )


class DeleteClass(BaseModel):
    name: Optional[str] = None
    id: Optional[str] = None


class UpdateClass(BaseModel):
    name: str
    newname: Optional[str] = None
    teacher: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None


class GetClass(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    

class DisplayClass(BaseModel):
    name: str
    teacher: str
    category: str
    description: str