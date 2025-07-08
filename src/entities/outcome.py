from dataclasses import dataclass

from enum import Enum


class EntityName(str, Enum):
    author = 'author'
    post = 'post'


class EntityAct(str, Enum):
    update = 'update'
    delete = 'delete'
    add = 'add'
    cancel = 'cancel'


@dataclass
class OutcomeMsgInfo:
    entity_id: str
    msg: str = 'completed successfully'
    entity_name: str | None = None
    entity_act: str | None = None
