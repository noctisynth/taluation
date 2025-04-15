from surrealdb import RecordID
from typing import List, Optional
from fastapi import APIRouter, Request, Depends

from app.db import db
from app.models import Record, Response
from app.models.account import Auth
from app.models.evaluation import Evaluation, EvaluationModel, CreateEvaluation
from app.repositories.account import AccountRepository
from app.repositories.cls import ClassRepository
from app.repositories.evaluation import EvaluationRepository
router = APIRouter()


@router.put("")
async def create_evaluation(evaluation: CreateEvaluation, request: Request) -> Response[Optional[Record]]:
    auth = request.state.auth
    
    account = await AccountRepository.get_account_by_name(db, auth.username)

    if account is None or account.id is None:
        return Response("Account not found.", data=None, success=False)
    if account.type == "teacher":
        return Response(
            "Only student can create an evaluation.", data=None, success=False
        )
    
    cls = await ClassRepository.get_class_by_name(db, evaluation.cls)
    if cls is None or cls.id is None:
        return Response("Class not found.", data=None, success=False)

    cls_model = cls.to_model()
    if cls_model.id is None:
        return Response("Class ID not found.", data=None, success=False)
    
    old_evaluation_model = await EvaluationRepository.get_evaluations_by_user_id_and_cls_id(db, account.id, cls_model.id)
    print(old_evaluation_model)
    if old_evaluation_model is not None and old_evaluation_model.id is not None:
        return Response("Evaluation already exists.", data=Record(id=old_evaluation_model.id.id), success=False)
    elif old_evaluation_model is not None:
        return Response("Evaluation already exists.", data=None, success=False)
    
    if evaluation.score > 10:
        evaluation.score = 10
    elif evaluation.score < 1:
        evaluation.score = 1
    
    evaluation.score = int(evaluation.score)

    evaluation_model = EvaluationModel(
        id=None,
        user=account.id,
        cls=cls_model.id,
        score=evaluation.score,
        comment=evaluation.comment,
    )
    
    evaluation_model = await EvaluationRepository.create_evaluation(db, evaluation_model)

    if evaluation_model is None:
        return Response("Failed to create evaluation.", data=None, success=False)

    if evaluation_model.id is None:
        return Response("Failed to get evaluation ID.", data=None, success=False)
        
    return Response(
        "Evaluation created successfully.",
        data= Record(id=evaluation_model.id.id),
    )

@router.delete("")
async def delete_evaluation_by_id(id: str, request: Request) -> Response[None]:
    auth = request.state.auth
    
    account = await AccountRepository.get_account_by_name(db, auth.username)
    if account is None or account.id is None:
        return Response("Account not found.", data=None, success=False)
    if account.type == "teacher":
        return Response(
            "Only student can delete an evaluation.", data=None, success=False
        )
    evaluation = await EvaluationRepository.get_evaluation_by_id(db, id)
    if evaluation is None or evaluation.id is None:
        return Response("Evaluation not found.", data=None, success=False)
    
    if account.id.id != evaluation.user.id and account.type != "admin":
        return Response(
            "You are not allowed to delete this evaluation.", data=None, success=False
        )
    
    await db.delete(RecordID("evaluation", id))
    return Response("Evaluation deleted successfully.")


@router.get("")
async def get_evaluations(
    id: Optional[str] = None, 
    user_id: Optional[str] = None, 
    class_id: Optional[str] = None
) -> Response[List[Evaluation]]:
    if user_id is not None and class_id is not None:
        evaluation_model = await EvaluationRepository.get_evaluations_by_user_id_and_cls_id(
            db, 
            RecordID("account", user_id),
            RecordID("class", class_id)
        )
        if evaluation_model is None:
            return Response("Evaluation not found.", data=[], success=False)
        return Response("Evaluation found.", data=[await EvaluationRepository.to_display(db, evaluation_model)])
    
    param_count = sum(1 for param in [id, user_id, class_id] if param is not None)
    
    if param_count == 0:
        return Response("Please provide id, user_id or class_id parameter", data=[], success=False)
    
    if id is not None:
        evaluation = await EvaluationRepository.get_evaluation_by_id(db, id)
        if evaluation is None:
            return Response("Evaluation not found.", data=[], success=False)
        return Response("Evaluation found.", data=[await EvaluationRepository.to_display(db, evaluation)])
    
    if user_id is not None:
        evaluation_models = await EvaluationRepository.get_evaluations_by_user_id(db, RecordID("account", user_id))
        if evaluation_models is None:
            return Response("Evaluation not found.", data=[], success=False)
        evaluations = [await EvaluationRepository.to_display(db, e) for e in evaluation_models]
        return Response("Evaluation found.", data=evaluations)
    
    if class_id is not None:
        evaluation_models = await EvaluationRepository.get_evaluations_by_cls_id(db, RecordID("class", class_id))
        if evaluation_models is None:
            return Response("Evaluation not found.", data=[], success=False)
        evaluations = [await EvaluationRepository.to_display(db, e) for e in evaluation_models]
        return Response("Evaluation found.", data=evaluations)
    
    return Response("Invalid request.", data=[], success=False)
