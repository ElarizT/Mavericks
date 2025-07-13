from src.db.session import async_session
from sqlalchemy import text
import socket
from logging import getLogger
from src.core.settings import get_settings

logger = getLogger(__name__)
settings = get_settings()


async def preflight_db_availability_check():
    try:
        async with async_session() as db:
            await db.execute(text("SELECT 1"))
    except socket.gaierror:
        raise Exception(
            f"Backend is unable to reach database at '{settings.SQLALCHEMY_ASYNC_DATABASE_URI}'. Please check env variables."  # noqa: E501
        )
