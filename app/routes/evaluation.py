from surrealdb import RecordID
from typing import List, Optional
from fastapi import APIRouter

from app.db import db
from app.models import Record, Response
from app.models.account import Auth
from app.models.evaluation import Evaluation, EvaluationModel
from app.utils.auth import get_account, verify_auth


router = APIRouter()


@router.post("/create")
async def create_evaluation(auth: Auth, data: Evaluation) -> Response[Optional[Record]]:
    if not await verify_auth(db, auth):
        return Response("Unauthorized.", data=None, success=False)
    account = await get_account(db, auth)
    if account is None:
        return Response("Account not found.", data=None, success=False)
    if account.type == "teacher":
        return Response(
            "Only student can create an evaluation.", data=None, success=False
        )
    evaluation: Optional[EvaluationModel] = await db.create(
        "evaluation", data.to_model().model_dump()
    )  # type: ignore

    if evaluation is None or evaluation.id is None:
        return Response("Failed to create evaluation.", data=None, success=False)

    return Response(
        "Evaluation created successfully.",
        data=Record(id=evaluation.id.id),
    )


@router.get("/get/{id}")
async def get_evaluation_by_id(id: str) -> Response[Optional[Evaluation]]:
    evaluation: Optional[EvaluationModel] = await db.query(  # type: ignore
        "SELECT * FROM evaluation WHERE id = $id",
        {"id": id},
    )
    if evaluation is None:
        return Response("Evaluation not found.", data=None, success=False)
    return Response("Evaluation found.", data=evaluation.to_raw())


@router.post("/delete/{id}")
async def delete_evaluation_by_id(auth: Auth, id: str) -> Response[None]:
    if not await verify_auth(db, auth):
        return Response("Unauthorized.", data=None, success=False)
    account = await get_account(db, auth)
    if account is None:
        return Response("Account not found.", data=None, success=False)
    if account.type == "teacher":
        return Response(
            "Only student can delete an evaluation.", data=None, success=False
        )
    if account.id != id and account.type != "admin":
        return Response(
            "You are not allowed to delete this evaluation.", data=None, success=False
        )
    await db.delete(RecordID("evaluation", id))
    return Response("Evaluation deleted successfully.")


@router.get("/get/{userid}")
async def get_evaluations_by_userid(userid: str) -> Response[List[Evaluation]]:
    evaluation: List[EvaluationModel] = await db.query(  # type: ignore
        "SELECT * FROM evaluation WHERE student = $student",
        {"student": RecordID("account", userid)},
    )
    evaluations = [evaluation.to_raw() for evaluation in evaluation]
    return Response("Evaluation found.", data=evaluations)


@router.get("/get/class/{class_id}")
async def get_evaluations_by_teacher(class_id: str) -> Response[List[Evaluation]]:
    evaluation: List[EvaluationModel] = await db.query(  # type: ignore
        "SELECT * FROM evaluation WHERE cls = $class_id",
        {"class_id": RecordID("class", class_id)},
    )
    evaluations = [evaluation.to_raw() for evaluation in evaluation]
    return Response("Evaluation found.", data=evaluations)
