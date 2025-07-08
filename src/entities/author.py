from dataclasses import dataclass


@dataclass(frozen=True)
class FullAuthorInfo:
    uuid: str
    name: str
    email: str


@dataclass(frozen=True)
class AuthorInfo:
    name: str
    email: str
