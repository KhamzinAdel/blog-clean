from dataclasses import dataclass
from datetime import datetime

from .author import AuthorInfo


@dataclass(frozen=True)
class FullPostInfo:
    uuid: str
    title: str
    text: str
    is_published: bool
    is_deleted: bool
    created_at: datetime
    author_id: str


@dataclass(frozen=True)
class PostInfoAuthor:
    title: str
    text: str
    is_published: bool
    created_at: datetime
    author: AuthorInfo


@dataclass(frozen=True)
class PostInfo:
    title: str
    text: str
    is_published: bool
    created_at: datetime
    author_id: str
