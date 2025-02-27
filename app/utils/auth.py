from surrealdb.connections.async_ws import AsyncWsSurrealConnection

from app.models.account import Auth


async def verify_auth(db: AsyncWsSurrealConnection, auth: Auth) -> bool:
    token = await db.query(
        "SELECT * FROM auth WHERE username = $username AND token = $token",
        {
            "username": auth.username,
            "token": auth.token,
        },
    )
    return bool(token)
