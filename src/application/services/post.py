from src.application.interfaces.repository.post import IPostRepository
from src.application.interfaces.repository.tm import ITransactionManager

from src.application.interfaces.services.post import IPostService


class PostService(IPostService):
    """Сервис для работы с постами."""

    def __init__(self, post_repository: IPostRepository, tm: ITransactionManager):
        self.post_repository = post_repository
        self.tm = tm
