import logging

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select, update, delete, insert

from src.application.interfaces.repository.author import IAuthorRepository
from src.application.exceptions.exc_repository import (
    NotFoundInfoException,
    NotPerformedActionException,
)

from src.entities.author import FullAuthorInfo, AuthorInfo
from src.entities.outcome import OutcomeMsgInfo, EntityName, EntityAct
from src.infrastructure.models import Author

logger = logging.getLogger(__name__)


class AuthorRepository(IAuthorRepository):
    """Репозиторий для работы с авторами."""

    def __init__(self, session: AsyncSession):
        self._session = session


    async def get_author_by_id(self, author_id: str) -> FullAuthorInfo | None:
        query = select(
            Author.uuid,
            Author.name,
            Author.email,
        ).where(Author.uuid==author_id)

        try:
            result = await self._session.execute(query)
            author_id, author_name, author_email = result.fetchone()

            if not result:
                raise NotFoundInfoException("Автор с id {} не найден".format(author_id))

            return FullAuthorInfo(
                uuid=f"{author_id}",
                name=author_name,
                email=author_email,
            )
        except SQLAlchemyError as e:
            logger.error("Ошибка при совершении запроса на получение автора по id: {}".format(e))


    async def get_author_list_by_limit(self, skip: int = 0, limit: int = 100) -> list[AuthorInfo]:
        query = select(Author.name, Author.email).offset(skip).limit(limit)
        result = await self._session.execute(query)
        results = result.mappings().all()

        return [
            AuthorInfo(
                name=result.name,
                email=result.email,
            ) for result in results
        ]

    async def get_author_by_email(self, email: str) -> FullAuthorInfo | None:
        query = select(
            Author.uuid,
            Author.name,
            Author.email,
        ).where(Author.email==email)

        try:
            result = await self._session.execute(query)
            author_id, author_name, author_email = result.one()

            if not result:
                raise NotFoundInfoException("Автор с email: {} не найден".format(author_email))

            return FullAuthorInfo(
                uuid=f"{author_id}",
                name=author_name,
                email=author_email,
            )
        except SQLAlchemyError as e:
            logger.error("Ошибка при совершении запроса на получение автора по email: {}".format(e))

    async def create_author(self, author_id: str, name: str, email: str, hashed_password: str) -> FullAuthorInfo | None:
        try:
            stmt = insert(Author).values(
                id=author_id,
                name=name,
                email=email,
                password=hashed_password,
            ).returning(
                Author.uuid,
                Author.name,
                Author.email,
            )

            result = await self._session.execute(stmt)
            new_author_data = result.fetchone()

            if new_author_data:
                return FullAuthorInfo(
                    uuid=f"{new_author_data.uuid}",
                    name=new_author_data.name,
                    email=new_author_data.email,
                )
        except SQLAlchemyError as e:
            logger.error("Ошибка при совершении запроса на создание автора: {}".format(e))

    async def delete_author(self, author_id: str) -> OutcomeMsgInfo | None:
        try:
            stmt = delete(Author).where(Author.uuid == author_id).returning(Author.uuid)
            result = await self._session.execute(stmt)
            delete_author_id = result.scalar()

            if delete_author_id is None:
                raise NotPerformedActionException("Автор не был удален: {}".format(author_id))

            return OutcomeMsgInfo(
                entity_id=f'{delete_author_id}',
                entity_name=EntityName.author.value,
                entity_act=EntityAct.delete.value,
            )
        except SQLAlchemyError as e:
            logger.error("Ошибка при совершении запроса на удаление автора: {}".format(e))

    async def change_password(self, author_id: str, hashed_password: str) -> OutcomeMsgInfo | None:
        try:
            stmt = update(Author).where(Author.uuid == author_id).values(password=hashed_password).returning(Author.uuid)
            result = await self._session.execute(stmt)
            update_author_id = result.scalar()

            if update_author_id is None:
                raise NotPerformedActionException("Пароль автора не был изменен: {}".format(author_id))

            return OutcomeMsgInfo(
                entity_id=f'{author_id}',
                entity_name=EntityName.author.value,
                entity_act=EntityAct.update.value,
            )
        except SQLAlchemyError as e:
            logger.error("Ошибка при совершении запроса на изменение пароля автора: {}".format(e))
