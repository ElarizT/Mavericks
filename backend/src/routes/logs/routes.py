from typing import Optional, Union, Annotated
from uuid import UUID
from fastapi import APIRouter, Query, HTTPException
from src.auth.dependencies import CurrentUserDependency
from src.schemas.ws.log import LogEntryDTO
from src.db.session import AsyncDBSession
from src.repositories.log import log_repo

log_router = APIRouter(tags=["Logs"], prefix="/logs")


@log_router.get("/list")
async def get_logs_by_session_id(
    db: AsyncDBSession,
    user: CurrentUserDependency,
    request_id: Annotated[Union[UUID, None], Query] = None,
    session_id: Annotated[Union[UUID, None], Query] = None,
) -> list[Optional[LogEntryDTO]]:
    params = (request_id, session_id)
    if all(params):
        raise HTTPException(
            status_code=400,
            detail="Only 'request_id' or 'session_id' could be provided but not both",
        )
    if not any(params):
        raise HTTPException(
            status_code=400,
            detail="Either 'request_id' or 'session_id' must be provided",
        )

    if session_id:
        session_id = str(session_id)
        # TODO: lookup by user
        return await log_repo.list_by_session_id(db=db, id_=session_id)

    if request_id:
        request_id = str(request_id)
        # TODO: lookup by user
        return await log_repo.list_by_request_id(db=db, id_=request_id)
