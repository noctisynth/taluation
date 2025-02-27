from surrealdb.connections.async_ws import AsyncWsSurrealConnection
from surrealdb import AsyncSurreal

db: AsyncWsSurrealConnection = AsyncSurreal("ws://127.0.0.1:5070") # type: ignore we use async ws connection
