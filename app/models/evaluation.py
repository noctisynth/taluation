from surrealdb import RecordID
from typing import Optional
from pydantic import BaseModel, field_validator
from typing import Any


class Evaluation(BaseModel):
    id: Optional[str]
    user: str
    cls: str
    score: int
    comment: str
    

    @field_validator('id', mode='before')
    @classmethod
    def validate_id(cls, v: Any) -> Optional[str]:
        if v is None:
            return None
        if hasattr(v, 'id'):
            return v.id
        
    def to_model(self) -> "EvaluationModel":
        return EvaluationModel(
            id=None if self.id is None else RecordID("evaluation", self.id),
            user=RecordID("user", self.user),
            cls=RecordID("class", self.cls),
            score=self.score,
            comment=self.comment,
        )


class EvaluationModel(BaseModel, arbitrary_types_allowed=True):
    id: Optional[RecordID]
    user: RecordID
    cls: RecordID
    score: int
    comment: str

    def to_raw(self) -> Evaluation:
        return Evaluation(
            id=self.id and self.id.id,
            user=self.user.id,
            cls=self.cls.id,
            score=self.score,
            comment=self.comment,
        )


class CreateEvaluation(BaseModel):
    cls: str
    score: int
    comment: str
