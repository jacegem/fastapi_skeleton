from typing import Optional, List

from bson import ObjectId
from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from starlette.status import HTTP_404_NOT_FOUND

from app.core.config import database_name, article_collection_name, favorites_collection_name, users_collection_name
from app.crud.tag import get_tags_for_article
from app.crud.user import get_user
from app.model.article import ArticleFilterParams, ArticleInDB
from app.model.profile import Profile


async def get_articles_with_filters(
        conn: AsyncIOMotorClient, filters: ArticleFilterParams, username: Optional[str] = None
) -> List[ArticleInDB]:
    articles: List[ArticleInDB] = []
    base_query = {}

    if filters.tag:
        base_query["tag_list"] = f"$all: [\"{filters.tag}\"]"

    if filters.favorited:
        base_query["slug"] = f"$in: [\"{filters.favorited}\"]"

    if filters.author:
        base_query["author"] = f"$in: [\"{filters.author}]\""

    rows = conn[database_name][article_collection_name].find({"author_id": username},
                                                             limit=filters.limit,
                                                             skip=filters.offset)

    async for row in rows:
        slug = row["slug"]
        author = await get_profile_for_user(conn, row["author_id"], username)
        tags = await get_tags_for_article(conn, slug)
        favorites_count = await get_favorites_count_for_article(conn, slug)
        favorited_by_user = await is_article_favorited_by_user(conn, slug, username)
        articles.append(
            ArticleInDB(
                **row,
                author=author,
                created_at=ObjectId(row["_id"]).generation_time,
                favorites_count=favorites_count,
                favorited=favorited_by_user,
            )
        )
    return articles


async def is_article_favorited_by_user(
        conn: AsyncIOMotorClient, slug: str, username: str
) -> bool:
    user_doc = await conn[database_name][users_collection_name].find_one({"username": username},
                                                                         projection={"id": True})
    article_doc = await conn[database_name][article_collection_name].find_one({"slug": slug}, projection={"id": True})
    if article_doc and user_doc:
        count = await conn[database_name][favorites_collection_name].count_documents({"user_id": user_doc['_id'],
                                                                                      "article_id": article_doc['_id']})
        return count > 0
    else:
        raise RuntimeError(f"没有找到对应的user_id或article_id,"
                           f" 用户名={username} user={user_doc},slug={slug} article={article_doc}")


async def get_favorites_count_for_article(conn: AsyncIOMotorClient, slug: str) -> int:
    article_doc = await conn[database_name][article_collection_name].find_one({"slug": slug}, projection={"id": True})
    if article_doc:
        return await conn[database_name][favorites_collection_name].count_documents({"article_id": article_doc['_id']})
    else:
        raise RuntimeError(f"没有找到对应的article_id,"
                           f" slug={slug} article_id={article_doc}")


async def get_profile_for_user(
        conn: AsyncIOMotorClient, target_username: str, current_username: Optional[str] = None
) -> Profile:
    user = await get_user(conn, target_username)
    if not user:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, detail=f"User {target_username} not found"
        )

    profile = Profile(**user.dict())
    profile.following = await is_following_for_user(
        conn, current_username, target_username
    )

    return profile
