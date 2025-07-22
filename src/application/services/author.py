import uuid
import logging

from src.entities.author import FullAuthorInfo, AuthorInfo
from src.entities.outcome import OutcomeMsgInfo
from src.application.interfaces.repository.author import IAuthorRepository
from src.application.interfaces.repository.tm import ITransactionManager
from src.application.interfaces.services.author import IAuthorService
from src.application.exceptions.exc_service import AuthorServiceError

logger = logging.getLogger(__name__)


class AuthorService(IAuthorService):
    """Сервис для работы с постами."""

    def __init__(self, author_repository: IAuthorRepository, tm: ITransactionManager):
        self.author_repo = author_repository
        self.tm = tm

    async def get_author_by_id(self, author_id: str) -> FullAuthorInfo | None:
        try:
            result = await self.author_repo.get_author_by_id(author_id=author_id)
            return result
        except AuthorServiceError as e:
            logger.error("Ошибка при получении автора по id: %s", e)

    async def get_author_by_email(self, email: str) -> FullAuthorInfo | None:
        try:
            result = await self.author_repo.get_author_by_email(email=email)
            return result
        except AuthorServiceError as e:
            logger.error("Ошибка при получении автора по email: %s", e)

    async def get_author_list_by_limit(self, skip: int, limit: int) -> list[AuthorInfo]:
        try:
            result = await self.author_repo.get_author_list_by_limit(skip=skip, limit=limit)
            return result
        except AuthorServiceError as e:
            logger.error("Ошибка при получении всех авторов: %s", e)

    async def create_author(self, name: str, email: str, hashed_password: str) -> FullAuthorInfo | None:
        try:
            new_user_id = uuid.uuid4().hex
            result = await self.author_repo.create_author(
                author_id=new_user_id,
                name=name,
                hashed_password=hashed_password,
            )
            await self.tm.commit()
            return result
        except AuthorServiceError as e:
            await self.tm.rollback()
            logger.error("Ошибка при создании автора: %s", e)

    async def delete_author(self, author_id: str) -> OutcomeMsgInfo | None:
        try:
            result = await self.author_repo.delete_author(author_id=author_id)
            await self.tm.commit()
            return result
        except AuthorServiceError as e:
             await self.tm.rollback()
             logger.error("Ошибка при удалении автора: %s", e)

    async def change_password(self, author_id: str, hashed_password: str) -> OutcomeMsgInfo | None:
        try:
            result = await self.author_repo.change_password(author_id=author_id, hashed_password=hashed_password)
            await self.tm.commit()
            return result
        except AuthorServiceError as e:
             await self.tm.rollback()
             logger.error("Ошибка при изменении пароля автора: %s", e)


