from src.repositories.agent import agent_repo

from src.db.session import async_session
from logging import getLogger
from src.utils.db_initial_healthcheck import preflight_db_availability_check


logger = getLogger(__name__)


async def run_startup_jobs():
    await preflight_db_availability_check()
    async with async_session() as db:
        await agent_repo.set_all_agents_inactive(db=db)

    logger.debug("Initial startup jobs complete")
    return
