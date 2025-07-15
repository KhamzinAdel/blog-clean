from typing import Protocol


class IPostService(Protocol):
    """Интерфейс сервиса постов"""

    async def get_post_by_id(self, post_id: str):
        pass

    async def get_post_list_by_limit(self, skip: int, limit: int):
        pass

    async def get_posts_by_author(self, author_id: str, skip: int, limit: int):
        pass

    async def create_post(self, title: str, text: str, user_id: str):
        pass

    async def delete_post(self, post_id: str, author_id: str):
        pass

    async def update_post(self, post_id: str, author_id: str, text: str):
        pass