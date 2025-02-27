from surrealdb import RecordID
from typing import Optional
from fastapi import APIRouter

from app.db import db
from app.models import Response
from app.models.account import Auth
from app.models.evaluation import Evaluation, EvaluationModel
from app.utils.auth import get_account, verify_auth


router = APIRouter()


@router.post("/create")
async def create_evaluation(auth: Auth, data: Evaluation):
    if not await verify_auth(db, auth):
        return Response("Unauthorized.", data=None, success=False)
    account = await get_account(db, auth)
    if account is None:
        return Response("Account not found.", data=None, success=False)
    if account.type == "teacher":
        return Response(
            "Only student can create an evaluation.", data=None, success=False
        )
    evaluation: EvaluationModel = await db.create(
        "evaluation", data.to_model().model_dump()
    )  # type: ignore
    return Response(
        "Evaluation created successfully.",
        data={"id": evaluation.id},
    )


@router.get("/get/{id}")
async def get_evaluation_by_id(id: str):
    evaluation: Optional[EvaluationModel] = await db.query(  # type: ignore
        "SELECT * FROM evaluation WHERE id = $id",
        {"id": id},
    )
    if evaluation is None:
        return Response("Evaluation not found.", data=None, success=False)
    return Response("Evaluation found.", data=evaluation.to_raw())


@router.post("/delete/{id}")
async def delete_evaluation_by_id(auth: Auth, id: str):
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
