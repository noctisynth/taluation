from typing import Optional, List
from surrealdb import RecordID
from fastapi import APIRouter, Request, Depends

from app.db import db
from app.models import Record, Response
from app.models.cls import CreateClass, GetClass, UpdateClass, DeleteClass, DisplayClass
from app.repositories.account import AccountRepository
from app.repositories.cls import ClassRepository
from app.repositories.evaluation import EvaluationRepository
router = APIRouter()


@router.put("")
async def create_class(cls_dto: CreateClass, request: Request) -> Response[Optional[Record]]:
    auth = request.state.auth

    account = await AccountRepository.get_account_by_name(db, auth.username)
    if account is None:
        return Response("Account not found.", data=None, success=False)
    if account.type != "teacher" and account.type != "admin":
        return Response(
            "Only teacher or admin can create a new class.", data=None, success=False
        )

    teacher_id = None
    if account.type == "admin":
        teacher_id = cls_dto.teacher
    elif account.type == "teacher":
        if account.id is None:
            return Response("Teacher ID not found.", data=None, success=False)
        teacher_id = account.id.id
    else:
        return Response("Teacher must be specified.", data=None, success=False)

    if await ClassRepository.class_exists(db, cls_dto.name):
        return Response("Class name already exists.", data=None, success=False)

    cls_model_data = cls_dto.to_model(teacher_id).model_dump(exclude={"id"})
    await db.create("class", cls_model_data)

    return Response(
        "Class created successfully."
    )


@router.patch("")
async def update_class(update_data: UpdateClass, request: Request) -> Response[None]:
    auth = request.state.auth
    
    account = await AccountRepository.get_account_by_name(db, auth.username)

    if account is None:
        return Response("Account not found.", data=None, success=False)
    if account.type != "teacher" and account.type != "admin":
        return Response("Only teacher or admin can update a class.", data=None, success=False)

    cls = await ClassRepository.get_class_by_name(db, update_data.name)
    if cls is None:
        return Response("Class not found.", data=None, success=False)
    
    cls_model = cls.to_model()

    if cls_model.id is None:
        return Response("Class ID not found.", data=None, success=False)

    if account.type == "teacher":
        if account.id is None:
            return Response("Teacher ID not found.", data=None, success=False)
        if str(cls_model.teacher.id) != str(account.id.id):
            return Response("You can only update your own class.", data=None, success=False)
        if update_data.teacher is not None:
            return Response("Teacher cannot change the class's teacher.", data=None, success=False)

    if update_data.newname is not None:
        other_cls = await ClassRepository.get_class_by_name(db, update_data.newname)
        if other_cls is not None:
            return Response("Class name already exists.", data=None, success=False)
        cls_model.name = update_data.newname
    if update_data.teacher is not None:
        new_teacher = await AccountRepository.get_account_by_name(db, update_data.teacher)
        if new_teacher is None or new_teacher.id is None:
            return Response("Teacher not found.", data=None, success=False)
        cls_model.teacher = new_teacher.id
    if update_data.description is not None:
        cls_model.description = update_data.description
    if update_data.category is not None:
        cls_model.category = update_data.category

    await db.update(
        cls_model.id,
        cls_model.model_dump(),
    )
    return Response("Class updated successfully.")


@router.delete("")
async def delete_class(request: Request, delete_data: DeleteClass = Depends()) -> Response[None]:
    auth = request.state.auth
    
    account = await AccountRepository.get_account_by_name(db, auth.username)

    if account is None:
        return Response("Account not found.", data=None, success=False)
    
    if account.type != "teacher" and account.type != "admin":
        return Response("Only teacher or admin can delete a class.", data=None, success=False)
    
    if delete_data.name is not None:
        cls_model = await ClassRepository.get_class_by_name(db, delete_data.name)
    elif delete_data.id is not None:
        cls_model = await ClassRepository.get_class_by_id(db, delete_data.id)
    else:
        return Response("Class name or ID not found.", data=None, success=False)

    if cls_model is None or cls_model.id is None:
        return Response("Class not found.", data=None, success=False)

    if account.type == "teacher":
        if account.id is None:
            return Response("Teacher ID not found.", data=None, success=False)

        if str(cls_model.teacher) != str(account.id.id):
            return Response("You can only delete your own class.", data=None, success=False)
    
    await EvaluationRepository.delete_evaluations_by_cls_id(db, RecordID("class", cls_model.id))
    await ClassRepository.delete_class_by_id(db, cls_model.id)
    return Response("Class deleted successfully.")


@router.get("")
async def get_classes(get_class: GetClass = Depends()) -> Response[List[DisplayClass]]:
    classes = None
    
    if get_class.id is not None:
        cls = await ClassRepository.get_class_by_id(db, get_class.id)
        classes = [cls] if cls else None
    elif get_class.name is not None:
        cls = await ClassRepository.get_class_by_name(db, get_class.name)
        classes = [cls] if cls else None
    elif get_class.teacher is not None:
        account = await AccountRepository.get_account_by_name(db, get_class.teacher)
        if account is None or account.id is None:
            return Response("Teacher not found.", data=None, success=False)
        classes = await ClassRepository.get_classes_by_teacher(db, account.id)
    else:
        classes = await ClassRepository.get_classes(db)
    
    if not classes:
        return Response("Class not found.", data=None, success=False)
        
    display_classes = await ClassRepository.to_display(db, classes)
    return Response("Class retrieved successfully.", data=display_classes)