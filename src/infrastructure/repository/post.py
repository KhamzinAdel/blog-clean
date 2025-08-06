import logging

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select, update, delete, insert, func
from sqlalchemy.orm import joinedload

from src.application.exceptions.exp_repository import NotPerformedActionException
from src.entities.outcome import OutcomeMsgInfo, EntityName, EntityAct
from src.entities.author import AuthorInfo
from src.application.interfaces.repository.post import IPostRepository
from src.entities.post import FullPostInfo, PostInfoAuthor, PostInfo
from src.infrastructure.models import Post

logger = logging.getLogger(__name__)


class PostRepository(IPostRepository):
    """Репозиторий для работы с постами."""

    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_post_by_id(self, post_id: str) -> FullPostInfo | None:
        query = (
            select(Post)
            .where(
                Post.uuid == post_id,
                Post.is_deleted == False
            )
        )

        try:
            result = await self._session.execute(query)
            post = result.scalar_one_or_none()

            if not post:
                return None

            return FullPostInfo(
                uuid=str(post.uuid),
                title=post.title,
                text=post.text,
                is_published=post.is_published,
                is_deleted=post.is_deleted,
                created_at=post.created_at,
                author_id=str(post.author_id),
            )
        except SQLAlchemyError as e:
            logger.error("Ошибка при получении поста: %s", e)

    async def get_post_list_by_limit(self, skip: int, limit: int) -> list[PostInfoAuthor]:
        query = select(
            Post
        ).options(
            joinedload(Post.author)
        ).where(
            Post.is_published == True,
            Post.is_deleted == False,
        ).order_by(
            Post.created_at.desc()
        ).offset(skip).limit(limit)

        try:
            result = await self._session.execute(query)
            posts = result.scalars().unique().all()

            return [
                PostInfoAuthor(
                    title=post.title,
                    text=post.text,
                    is_published=post.is_published,
                    created_at=post.created_at,
                    author=AuthorInfo(
                        name=post.author.name,
                        email=post.author.email,
                    )
                )
                for post in posts
            ] if posts else []
        except SQLAlchemyError as e:
            logger.error("Ошибка при получении опубликованных постов: %s", e)

    async def get_posts_by_author(self, author_id: str, skip: int = 0, limit: int = 100) -> list[PostInfo]:
        query = select(
               Post.title,
               Post.text,
               Post.is_published,
               Post.created_at,
               Post.author_id,
        ).where(Post.author_id == author_id).offset(skip).limit(limit)

        try:
            result = await self._session.execute(query)
            posts = result.scalars().all()
            return [
                PostInfo(
                    title=post.title,
                    text=post.text,
                    is_published=post.is_published,
                    created_at=post.created_at,
                    author_id=post.author_id,
                )
                for post in posts
            ] if posts else []

        except SQLAlchemyError as e:
            logger.error("Ошибка при получении постов автора: %s", e)

    async def create_post(self, post_id: str, title: str, text: str, author_id: str) -> FullPostInfo | None:
        try:
            stmt = insert(Post).values(author_id=author_id, text=text, id=post_id).returning(
                Post.uuid,
                Post.title,
                Post.text,
                Post.created_at,
                Post.is_published,
                Post.is_deleted,
                Post.author_id,
            )

            result = await self._session.execute(stmt)
            new_post_data = result.fetchone()

            if new_post_data is None:
                raise NotPerformedActionException("Пост не был создан.")

            return FullPostInfo(
                uuid=f"{new_post_data.uuid}",
                title=new_post_data.title,
                text=new_post_data.text,
                created_at=new_post_data.created_at.strftime("%Y.%m.%d"),
                is_published=new_post_data.is_published,
                is_deleted=new_post_data.is_deleted,
                author_id='%s' % new_post_data.author_id,
            )
        except SQLAlchemyError as e:
            logger.error("Ошибка при создании поста: %s", e)

    async def delete_post(self, post_id: str, author_id: str) -> OutcomeMsgInfo | None:
        try:
            stmt = delete(Post).where((Post.uuid == post_id) & (Post.author_id == author_id)).returning(Post.uuid)
            result = await self._session.execute(stmt)
            del_post_id = result.scalar()

            if del_post_id is None:
                raise NotPerformedActionException("Пост не был удален: %s" % author_id)

            return OutcomeMsgInfo(
                entity_id=f"{del_post_id}",
                entity_name=EntityName.post.value,
                entity_act=EntityAct.delete.value,
            )
        except SQLAlchemyError as e:
            logger.error("Ошибка при совершении запроса на удаление поста: %s", e)

    async def update_post(self, post_id: str, author_id: str, text: str) -> PostInfo | None:
        try:
            stmt = (
                update(Post)
                .where(
                    (Post.uuid == post_id) &
                    (Post.author_id == author_id) &
                    (Post.is_deleted == False)
                )
                .values(
                    text=text,
                    updated_at=func.now()
                )
                .returning(
                    Post.uuid,
                    Post.title,
                    Post.text,
                    Post.is_published,
                    Post.created_at,
                    Post.author_id,
                )
            )

            result = await self._session.execute(stmt)
            updated_post = result.fetchone()

            if not updated_post:
                raise NotPerformedActionException("Пост не был обновлен: %s" % author_id)

            return PostInfo(
                title=updated_post.title,
                text=updated_post.text,
                is_published=updated_post.is_published,
                created_at=updated_post.created_at,
                author_id=f"{updated_post.author_id}",
            )

        except SQLAlchemyError as e:
            logger.error(
                "Ошибка при обновлении поста %s автором %s: %s",
                post_id,
                author_id,
                e,
            )
