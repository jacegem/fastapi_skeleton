from typing import List

from pydantic import Schema

from app.model.dbmodel import DateTimeModelMixin, DBModelMixin
from app.model.profile import Profile
from app.model.rwmodel import RWModel


class ArticleBase(RWModel):
    title: str
    description: str
    body: str
    tag_list: List[str] = Schema([], alias="tagList")


class Article(DateTimeModelMixin, ArticleBase):
    slug: str
    author: Profile
    favorited: bool
    favorites_count: int = Schema(..., alias="favoritesCount")


class ArticleInDB(DBModelMixin, Article):
    pass


class ArticleFilterParams(RWModel):
    tag: str = ""
    author: str = ""
    favorited: str = ""
    limit: int = 20
    offset: int = 0


class ManyArticlesInResponse(RWModel):
    articles: List[Article]
    articles_count: int = Schema(..., alias="articlesCount")
