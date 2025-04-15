from typing import Optional
from fastapi import APIRouter, Request
from argon2.exceptions import VerifyMismatchError
from app.db import db
from app.models import Response
from app.models.account import Account, Credentials, LoginResponse, UpdateAccount, AccountResponse
from app.repositories.account import AccountRepository

import argon2

router = APIRouter()


@router.post("/register")
async def register(account: Account) -> Response[None]:
    if await AccountRepository.account_exists(db, account):
        return Response("Account already exists.", data=None, success=False)
    else:
        account.password = argon2.hash_password(
            account.password.encode(), salt=account.username.encode()
        ).decode()
        account_data = account.model_dump(exclude={"id"})
        await db.create("account", account_data)

    return Response("Account created successfully.")


@router.post("/login")
async def login(credentials: Credentials) -> Response[Optional[LoginResponse]]:
    account = await AccountRepository.get_account_by_name(db, credentials.username)

    if account is None:
        return Response("Account not found.", data=None, success=False)

    try:
        if argon2.verify_password(
            account.password.encode(), credentials.password.encode()
        ):
            await AccountRepository.delete_token(db, account.username)
            token = argon2.hash_password(account.username.encode()).decode()
            await db.create(
                "auth",
                {
                    "username": account.username,
                    "token": token,
                },
            )
            return Response("Login successful.", data=LoginResponse(token=token))
        else:
            return Response("Invalid password.", data=None, success=False)
    except VerifyMismatchError:
        return Response("Invalid password.", data=None, success=False)



@router.get("/logout")
async def logout(request: Request) -> Response[None]:
    auth = request.state.auth
    await AccountRepository.delete_token(db, auth.username)
    return Response("Logout successful.")

@router.patch("")
async def update_account(update_data: UpdateAccount, request: Request) -> Response[None]:
    auth = request.state.auth

    current_user = await AccountRepository.get_account_by_name(db, auth.username)
    if current_user is None:
        return Response("Current user account not found.", data=None, success=False)
    
    target_account = await AccountRepository.get_account_by_name(db, update_data.username)

    if target_account is None or target_account.id is None:
        return Response("Target account not found.", data=None, success=False)

    if update_data.type is not None and current_user.type != "admin":
        return Response("Permission denied. Only admin can modify account type.", data=None, success=False)

    if auth.username != update_data.username and current_user.type != "admin":
        return Response(
            "Permission denied. Only admin can update other accounts.", data=None, success=False
        )
    
    old_name = target_account.username

    if update_data.newname is not None:
        target_account.username = update_data.newname
    if update_data.email is not None:
        target_account.email = update_data.email
    if update_data.phone is not None:
        target_account.phone = update_data.phone
    if update_data.type is not None:
        target_account.type = update_data.type
    
    await db.update(target_account.id, target_account.model_dump())
    await AccountRepository.delete_token(db, old_name)
    return Response("Account updated successfully.")


@router.delete("")
async def delete_account_by_username(username: str, request: Request) -> Response[None]:
    auth = request.state.auth

    current_user = await AccountRepository.get_account_by_name(db, auth.username)
    if current_user is None:
        return Response("Current user account not found.", data=None, success=False)
    
    if auth.username != username and current_user.type != "admin":
        return Response(
            "Permission denied. Only admin can delete other accounts.", data=None, success=False
        )

    if not await AccountRepository.delete_account(db, username):
        return Response("Failed to delete account.", data=None, success=False)

    return Response("Account deleted successfully.")


@router.get("")
async def get_account_by_name(name: str, request: Request) -> Response[Optional[AccountResponse]]:
    auth = request.state.auth
    
    current_user = await AccountRepository.get_account_by_name(db, auth.username)
    if current_user is None:
        return Response("Current user not found.", data=None, success=False)
    
    if current_user.type != "admin" and auth.username != name:
        return Response("Permission denied. You can only access your own account.", data=None, success=False)
    
    account = await AccountRepository.get_account_by_name(db, name)
    
    if account is None:
        return Response("Account not found.", data=None, success=False)
    else:
        return Response("Account found.", data=account.to_response())
