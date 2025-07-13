from typing import Optional
from src.schemas.ws.log import LogCreate, LogUpdate, LogEntryDTO
from src.repositories.base import CRUDBase
from src.models import Log
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


class LogRepository(CRUDBase[Log, LogCreate, LogUpdate]):
    async def list_by_session_id(
        self, db: AsyncSession, id_: str
    ) -> list[Optional[Log]]:
        q = await db.execute(select(self.model).where(self.model.session_id == id_))
        return [LogEntryDTO(**log.__dict__) for log in q.scalars().all()]

    async def list_by_request_id(
        self, db: AsyncSession, id_: str
    ) -> list[Optional[Log]]:
        q = await db.execute(select(self.model).where(self.model.request_id == id_))
        return [LogEntryDTO(**log.__dict__) for log in q.scalars().all()]


log_repo = LogRepository(Log)
