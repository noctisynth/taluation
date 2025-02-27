from typing import Optional
from surrealdb.connections.async_ws import AsyncWsSurrealConnection

from app.models.account import AccountModel, Auth


async def verify_auth(db: AsyncWsSurrealConnection, auth: Auth) -> bool:
    token = await db.query(
        "SELECT * FROM auth WHERE username = $username AND token = $token",
        {
            "username": auth.username,
            "token": auth.token,
        },
    )
    return bool(token)


async def get_account(
    db: AsyncWsSurrealConnection, auth: Auth
) -> Optional[AccountModel]:
    account: Optional[AccountModel] = await db.query(  # type: ignore
        "SELECT * FROM account WHERE username = $username",
        {
            "username": auth.username,
        },
    )
    return account
