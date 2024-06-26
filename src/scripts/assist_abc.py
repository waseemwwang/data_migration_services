from abc import ABC, abstractmethod
from models.database import SessionManager
from sqlalchemy.ext.asyncio import AsyncSession
from utils.logger import log


class ScriptABC(ABC):

    def __init__(self, db_name: str) -> None:
        super().__init__()
        self.db_name = db_name

    @abstractmethod
    async def load_data(self, session: AsyncSession):
        pass

    @abstractmethod
    async def process_data(self, session: AsyncSession):
        pass

    @abstractmethod
    async def update_data(self, session: AsyncSession):
        pass

    def as_result(self):
        pass


    async def run(self):
        log.debug("run start")
        async with SessionManager(self.db_name) as session:
            await self.load_data(session)
            log.debug("load_data end")
            await self.process_data(session)
            log.debug("process_data end")
            await self.update_data(session)
            log.debug("update_data end")
        return self.as_result()

