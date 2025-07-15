from typing import Protocol


class ITransactionManager(Protocol):
    """Интерфейс для менеджера транзакций"""

    async def commit(self) -> None:
        pass

    async def rollback(self) -> None:
        pass
