from typing import List, Dict, Optional

from app.models.cls import DisplayClass, Class
from surrealdb import AsyncWsSurrealConnection, RecordID
from app.repositories.account import AccountRepository

class ClassRepository:
    @staticmethod
    async def class_exists(db: AsyncWsSurrealConnection, name: str) -> bool:
        classes: List[dict] = await db.query(  # type: ignore
            "SELECT * FROM class WHERE name = $name",
            {"name": name},
        )
        return len(classes) > 0

    @staticmethod
    async def delete_class_by_name(db: AsyncWsSurrealConnection, name: str) -> None:
        await db.query(
            "DELETE FROM class WHERE name = $name",
            {"name": name},
        )
    
    @staticmethod
    async def delete_class_by_id(db: AsyncWsSurrealConnection, id: str) -> None:
        await db.delete(RecordID("class", id))

    @staticmethod
    async def get_class_by_id(db: AsyncWsSurrealConnection, id: str) -> Optional[Class]:
        cls: Optional[dict] = await db.select(RecordID("class", id))  # type: ignore
        if cls is None:
            return None
        return Class(**cls)

    @staticmethod
    async def get_class_by_name(db: AsyncWsSurrealConnection, name: str) -> Optional[Class]:
        classes: List[dict] = await db.query(  # type: ignore
            "SELECT * FROM class WHERE name = $name",
            {
                "name": name,
            },
        )
        if not classes or len(classes) == 0:
            return None
        return Class(**classes[0])
    
    @staticmethod
    async def get_classes(db: AsyncWsSurrealConnection) -> List[Class]:
        classes: List[dict] = await db.query(  # type: ignore
            "SELECT * FROM class",
        )
        return [Class(**cls) for cls in classes]
    
    @staticmethod
    async def to_display(db: AsyncWsSurrealConnection, classes: List[Class]) -> List[DisplayClass]:
        result = []
        for c in classes:
            teacher_account = await AccountRepository.get_account_by_id(db, c.teacher)
            if teacher_account:
                c.teacher = teacher_account.username
            result.append(c.to_list())
        return result