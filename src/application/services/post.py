import uuid
import logging


from src.entities.post import FullPostInfo, PostInfo
from src.entities.outcome import OutcomeMsgInfo
from src.application.interfaces.repository.post import IPostRepository
from src.application.interfaces.repository.tm import ITransactionManager
from src.application.interfaces.services.post import IPostService
from src.application.exceptions.exc_service import PostServiceError

logger = logging.getLogger(__name__)


class PostService(IPostService):
    """Сервис для работы с постами."""

    def __init__(self, post_repository: IPostRepository, tm: ITransactionManager):
        self.post_repo = post_repository
        self.tm = tm

    async def get_post_by_id(self, post_id: str) -> FullPostInfo | None:
        try:
            result = await self.post_repo.get_post_by_id(post_id=post_id)
            return result
        except PostServiceError as e:
            logger.error("Ошибка при получении поста по id: %s", e)

    async def get_post_list_by_limit(self, skip: int, limit: int):
        try:
            result = await self.post_repo.get_post_list_by_limit(skip=skip, limit=limit)
            return result
        except PostServiceError as e:
            logger.error("Ошибка при получении постов: %s", e)

    async def get_posts_by_author(self, author_id: str, skip: int, limit: int) -> list[PostInfo]:
        try:
            result = await self.post_repo.get_posts_by_author(author_id=author_id, skip=skip, limit=limit)
            return result
        except PostServiceError as e:
            logger.error("Ошибка при получении постов автора: %s", e)

    async def create_post(self, title: str, text: str, user_id: str) -> FullPostInfo | None:
        try:
            new_post_id = uuid.uuid4().hex
            result = await self.post_repo.create_post(post_id=new_post_id, title=title, text=text, user_id=user_id)
            await self.tm.commit()
            return result
        except PostServiceError as e:
            await self.tm.rollback()
            logger.error("Ошибка при создании поста: %s", e)

    async def delete_post(self, post_id: str, author_id: str) -> PostInfo | None:
        try:
            result = await self.post_repo.delete_post(post_id=post_id, author_id=author_id)
            await self.tm.commit()
            return result
        except PostServiceError as e:
            await self.tm.rollback()
            logger.error("Ошибка при удалении поста: %s", e)

    async def update_post(self, post_id: str, author_id: str, text: str) -> OutcomeMsgInfo | None:
        try:
            result = await self.post_repo.update_post(post_id=post_id, author_id=author_id, text=text)
            await self.tm.commit()
            return result
        except PostServiceError as e:
            await self.tm.rollback()
            logger.error("Ошибка при обновлении поста: %s", e)
