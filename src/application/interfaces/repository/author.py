from typing import Protocol


class IAuthorRepository(Protocol):
    """Интерфейс для работы с авторами."""

    async def get_author_by_id(self, author_id: str):
        pass

    async def get_author_by_email(self, email: str):
        pass

    async def get_author_list_by_limit(self, skip: int, limit: int):
        pass

    async def create_author(self, author_id: str, name: str, email: str, hashed_password: str):
        pass

    async def delete_author(self, author_id: str):
        pass

    async def change_password(self, author_id: str, hashed_password: str):
        pass

    async def change_name(self, author_id: str, email: str):
        pass
