from sqlalchemy.ext.asyncio import AsyncSession

from src.application.interfaces.repository.tm import ITransactionManager


class TransactionManager(ITransactionManager):
    """Менеджер транзакций"""

    def __init__(self, session: AsyncSession):
        self._session = session

    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.rollback()
