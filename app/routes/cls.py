from typing import Optional
from surrealdb import RecordID
from fastapi import APIRouter

from app.db import db
from app.models import Response
from app.models.account import Auth
from app.models.cls import Class, ClassModel
from app.utils.auth import get_account, verify_auth

router = APIRouter()


@router.post("/create")
async def create_class(auth: Auth, data: Class):
    if not await verify_auth(db, auth):
        return Response("Unauthorized.", data=None, success=False)

    account = await get_account(db, auth)
    if account is None:
        return Response("Account not found.", data=None, success=False)
    if account.type != "teacher":
        return Response(
            "Only teacher can create a new class.", data=None, success=False
        )

    cls: ClassModel = await db.create("class", data.to_model().model_dump())  # type: ignore

    return Response(
        "Class created successfully.",
        data={"id": cls.id},
    )


@router.post("/update")
async def update_class(auth: Auth, data: Class):
    if not await verify_auth(db, auth):
        return Response("Unauthorized.", data=None, success=False)
    account = await get_account(db, auth)
    if account is None:
        return Response("Account not found.", data=None, success=False)
    if account.type != "teacher":
        return Response("Only teacher can update a class.", data=None, success=False)

    cls: ClassModel = await db.select(RecordID("class", data.id))  # type: ignore
    if cls is None:
        return Response("Class not found.", data=None, success=False)

    await db.update(
        RecordID("class", cls.id),
        data.to_model().model_dump(),
    )
    return Response("Class updated successfully.")


@router.post("/delete/{id}")
async def delete_class(auth: Auth, id: str):
    if not await verify_auth(db, auth):
        return Response("Unauthorized.", data=None, success=False)
    account = await get_account(db, auth)
    if account is None:
        return Response("Account not found.", data=None, success=False)
    if account.type != "teacher":
        return Response("Only teacher can delete a class.", data=None, success=False)
    await db.delete(RecordID("class", id))
    return Response("Class deleted successfully.")


@router.get("/get/{name}")
async def get_class_by_name(name: str):
    cls: Optional[ClassModel] = await db.query(
        "SELECT * FROM class WHERE name = $name",
        {"name": name},
    )  # type: ignore
    if cls is None:
        return Response("Class not found.", data=None, success=False)
    return Response("Class retrieved successfully.", data=cls.to_raw())
