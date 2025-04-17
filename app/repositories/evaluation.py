from app.models.evaluation import EvaluationModel, Evaluation
from surrealdb import AsyncWsSurrealConnection, RecordID
from typing import Optional, List
from app.repositories.account import AccountRepository
from app.repositories.cls import ClassRepository


class EvaluationRepository:
    @staticmethod
    async def create_evaluation(db: AsyncWsSurrealConnection, evaluation: EvaluationModel) -> Optional[EvaluationModel]:
        evaluation_model = await db.create(
            "evaluation", evaluation.model_dump(exclude={"id"})
        )

        if evaluation_model is None:
            return None

        if type(evaluation_model) == dict:
            return EvaluationModel(**evaluation_model)
        
        return None
    
    @staticmethod
    async def delete_evaluation(db: AsyncWsSurrealConnection, id: str) -> bool:
        result = await db.delete(RecordID("evaluation", id))
        return result is not None
    
    @staticmethod
    async def get_evaluations(db: AsyncWsSurrealConnection) -> Optional[List[EvaluationModel]]:
        result: Optional[List[dict]] = await db.query(  # type: ignore
            "SELECT * FROM evaluation",
        )
        
        if result is None:
            return None
        elif type(result) == list:
            return [EvaluationModel(**item) for item in result]
        
        return None

    @staticmethod
    async def delete_evaluations_by_cls_id(db: AsyncWsSurrealConnection, cls: RecordID) -> bool:
        result = await db.query(
            "DELETE FROM evaluation WHERE cls = $cls",
            {"cls": cls}
        )
        return result is not None
    
    @staticmethod
    async def get_evaluations_by_user_id_and_cls_id(db: AsyncWsSurrealConnection, user: RecordID, cls: RecordID) -> Optional[EvaluationModel]:
        result = await db.query(
            "SELECT * FROM evaluation WHERE user = $user AND cls = $cls",
            {"user": user, "cls": cls}
        )

        if result is None:
            return None
        
        if type(result) == dict:
            return EvaluationModel(**result)
        elif type(result) == list and len(result) > 0:
            return EvaluationModel(**result[0])
        return None
    
    @staticmethod
    async def get_evaluations_by_user_id(db: AsyncWsSurrealConnection, user: RecordID) -> Optional[List[EvaluationModel]]:
        result: Optional[List[dict]] = await db.query(  # type: ignore
            "SELECT * FROM evaluation WHERE user = $user",
            {"user": user}
        )

        if result is None:
            return None
        elif type(result) == dict:
            return [EvaluationModel(**result)]
        elif type(result) == list:
            return [EvaluationModel(**item) for item in result]
        
        return None
    
    @staticmethod
    async def to_display(db: AsyncWsSurrealConnection, evaluation_model: EvaluationModel) -> Evaluation:
        evaluation = evaluation_model.to_raw()
        
        account = await AccountRepository.get_account_by_id(db, evaluation.user)
        if account is not None:
            evaluation.user = account.username
            
        cls = await ClassRepository.get_class_by_id(db, evaluation.cls)
        if cls is not None:
            evaluation.cls = cls.name

        return evaluation

    @staticmethod
    async def get_evaluations_by_cls_id(db: AsyncWsSurrealConnection, cls: RecordID) -> Optional[List[EvaluationModel]]:
        result: Optional[List[dict]] = await db.query(  # type: ignore
            "SELECT * FROM evaluation WHERE cls = $cls",
            {"cls": cls}
        )

        if result is None:
            return None
        elif type(result) == dict:
            return [EvaluationModel(**result)]
        elif type(result) == list:
            return [EvaluationModel(**item) for item in result]
        
        return None
    
    @staticmethod
    async def evaluation_exists(db: AsyncWsSurrealConnection, user: RecordID, cls: RecordID) -> bool:
        result = await db.query(
            "SELECT * FROM evaluation WHERE user = $user AND cls = $cls",
            {"user": user, "cls": cls}
        )
        return result is not None and len(result) > 0
    
    @staticmethod
    async def get_evaluation_by_id(db: AsyncWsSurrealConnection, id: str) -> Optional[EvaluationModel]:
        evaluation_model = await db.select(
            RecordID("evaluation", id)
        )
        if evaluation_model is None:
            return None
        
        if type(evaluation_model) == dict:
            return EvaluationModel(**evaluation_model)
        
        return None