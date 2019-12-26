from typing import Optional

from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import EmailStr
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from app.crud.user import get_user, get_user_by_email


async def check_free_username_and_email(
        conn: AsyncIOMotorClient,
        username: Optional[str] = None,
        email: Optional[EmailStr] = None,
):
    if username:
        user_by_username = await get_user(conn, username)
        if user_by_username:
            raise HTTPException(
                status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                detail="user with this username already exists"
            )
    if email:
        user_by_email = await get_user_by_email(conn, email)
        if user_by_email:
            raise HTTPException(
                status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                detail="User with this email already exists"
            )
