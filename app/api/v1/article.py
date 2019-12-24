from fastapi import APIRouter, Query, Depends
from motor.motor_asyncio import AsyncIOMotorClient

from app.core.jwt import get_current_user_authorizer
from app.core.util import create_aliased_response
from app.crud.article import get_articles_with_filters
from app.db.mongodb import get_database
from app.model.article import ManyArticlesInResponse, ArticleFilterParams
from app.model.user import User

router = APIRouter()


@router.get("/articles", response_model=ManyArticlesInResponse, tags=["articles"])
async def get_articles(
        tag: str = "",
        author: str = "",
        favorited: str = "",
        limit: int = Query(20, gt=0),
        offset: int = Query(0, ge=0),
        user: User = Depends(get_current_user_authorizer(required=False)),
        db: AsyncIOMotorClient = Depends(get_database),
):
    filters = ArticleFilterParams(
        tag=tag, author=author, favorited=favorited, limit=limit, offset=offset
    )

    db_articles = await get_articles_with_filters(
        db, filters, user.username if user else None
    )

    return create_aliased_response(
        ManyArticlesInResponse(articles=db_articles, articles_count=len(db_articles))
    )
