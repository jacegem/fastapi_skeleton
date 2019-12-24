from typing import List

from app.model.dbmodel import DBModelMixin
from app.model.rwmodel import RWModel


class Tag(RWModel):
    tag: str


class TagInDB(DBModelMixin, Tag):
    pass


class TagsList(RWModel):
    tags: List[str] = []