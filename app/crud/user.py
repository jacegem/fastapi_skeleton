from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import database_name, users_collection_name
from app.model.user import UserInDB


async def get_user(conn: AsyncIOMotorClient, username: str) -> UserInDB:
    row = await conn[database_name][users_collection_name].find_one({"username": username})
    if row:
        return UserInDB(**row)