from typing import List

from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import database_name, article_collection_name
from app.model.tag import TagInDB


async def get_tags_for_article(conn: AsyncIOMotorClient, slug: str) -> List[TagInDB]:
    tags = []
    article_tags = await conn[database_name][article_collection_name].find_one({"slug": slug},
                                                                               projection={"tag_list": True})
    for row in article_tags["tag_list"]:
        tags.append(TagInDB({"tag": row}))

    return tags
