from typing import Optional, List

from surrealdb import AsyncWsSurrealConnection, RecordID
from app.models.account import Auth, AccountModel, Account

class AccountRepository:
    @staticmethod
    async def verify_auth(db: AsyncWsSurrealConnection, username: str, auth_token: str) -> bool:
        token = await db.query(
            "SELECT * FROM auth WHERE username = $username AND token = $auth_token",
            {
                "username": username,
                "auth_token": auth_token,
            },
        )
        return bool(token)

    @staticmethod
    async def account_exists(db: AsyncWsSurrealConnection, account: Account) -> bool:
        accounts: List[dict] = await db.query(  # type: ignore
            "SELECT * FROM account WHERE username = $username OR email = $email OR phone = $phone",
            {
                "username": account.username,
                "email": account.email,
                "phone": account.phone,
            },
        )
        return len(accounts) > 0

    @staticmethod
    async def get_non_admin_accounts(db: AsyncWsSurrealConnection) -> List[AccountModel]:
        accounts: List[dict] = await db.query(  # type: ignore
            "SELECT * FROM account where type != 'admin'",
        )

        if not accounts or len(accounts) == 0:
            return []
        return [Account(**account).to_model() for account in accounts]

    @staticmethod
    async def get_account_by_name(
        db: AsyncWsSurrealConnection, username: str
    ) -> Optional[AccountModel]:
        accounts: List[dict] = await db.query(  # type: ignore
            "SELECT * FROM account WHERE username = $username",
            {
                "username": username,
            },
        )
        if not accounts or len(accounts) == 0:
            return None
        return Account(**accounts[0]).to_model()

    @staticmethod
    async def get_account_by_id(db: AsyncWsSurrealConnection, id: str) -> Optional[AccountModel]:
        account: Optional[dict] = await db.select(RecordID("account", id))  # type: ignore
        if account is None:
            return None
        return Account(**account).to_model()

    @staticmethod
    async def delete_token(db: AsyncWsSurrealConnection, username: str) -> None:
        await db.query(  # type: ignore
            "DELETE FROM auth WHERE username = $username",
            {
                "username": username,
            },
        )

    @staticmethod
    async def delete_account(db: AsyncWsSurrealConnection, username: str) -> bool:
        target_account = await AccountRepository.get_account_by_name(db, username)
        if target_account is None or target_account.id is None:
            return False
        
        await db.query(
            "DELETE FROM class WHERE teacher = $teacher",
            {
                "teacher": RecordID("account", username),
            },
        )

        await db.query(
            "DELETE FROM auth WHERE username = $username",
            {
                "username": username,
            },
        )

        await db.delete(target_account.id)
        return True

