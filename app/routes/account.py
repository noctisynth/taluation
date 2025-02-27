from typing import List, Optional
from fastapi import APIRouter
from surrealdb import RecordID

from app.db import db
from app.models import Response
from app.models.account import Account, AccountModel, Auth
from app.utils.auth import verify_auth

import argon2

router = APIRouter()


@router.post("/register")
async def register(account: Account):
    result: List[AccountModel] = await db.query(  # type: ignore
        "SELECT * FROM account WHERE username = $username \
            OR email = $email OR phone = $phone",
        {
            "username": account.username,
            "email": account.email,
            "phone": account.phone,
        },
    )

    if len(result) > 0:
        return Response("Account already exists.", data=None, success=False)
    else:
        account.password = argon2.hash_password(
            account.password.encode(), salt=account.username.encode()
        ).decode()
        await db.create("account", account.model_dump())

    return Response("Account created successfully.")


@router.get("/login")
async def login():
    account: Optional[Account] = await db.query(  # type: ignore
        "SELECT * FROM account WHERE username = $username",
    )

    if account is None:
        return Response("Account not found.", data=None, success=False)
    elif argon2.verify_password(account.password.encode(), account.username.encode()):
        token = argon2.hash_password(account.username.encode()).decode()
        await db.create(
            "auth",
            {
                "username": account.username,
                "token": token,
            },
        )
        return Response("Login successful.", data={"token": token})
    else:
        return Response("Invalid password.", data=None, success=False)


@router.post("/update")
async def update_account(auth: Auth, data: Account):
    if not await verify_auth(db, auth):
        return Response("Invalid token.", data=None, success=False)

    account: AccountModel = await db.query(  # type: ignore
        "SELECT * FROM account WHERE username = $username",
        {
            "username": auth.username,
        },
    )
    if not account.id:
        return Response("Account not found.", data=None, success=False)

    await db.update(account.id, data.model_dump())
    return Response("Account updated successfully.")


@router.post("/delete/{username}")
async def delete_account_by_username(auth: Auth, username: str):
    if not await verify_auth(db, auth):
        return Response("Invalid token.", data=None, success=False)

    account: Optional[AccountModel] = await db.query(  # type: ignore
        "SELECT * FROM account WHERE username = $username",
        {
            "username": auth.username,
        },
    )
    if account is None:
        return Response("Account not found.", data=None, success=False)
    if auth.username != username and account.type != "admin":
        return Response(
            "You are not allowed to delete this account.", data=None, success=False
        )

    await db.query(
        "DELETE * FROM class WHERE teacher = $teacher",
        {
            "teacher": RecordID("teacher", auth.username),
        },
    )
    await db.query(
        "DELETE * FROM auth WHERE username = $username",
        {
            "username": auth.username,
        },
    )
    await db.delete(RecordID("account", auth.username))

    return Response("Account deleted successfully.")


@router.get("/get/{username}")
async def get_account_by_username(username: str):
    account: Optional[AccountModel] = await db.query(  # type: ignore
        "SELECT * FROM account WHERE username = $username",
        {
            "username": username,
        },
    )
    if account is None:
        return Response("Account not found.", data=None, success=False)
    else:
        return Response("Account found.", data=account)
