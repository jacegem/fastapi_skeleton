from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import EmailStr

from app.core.config import database_name, users_collection_name
from app.model.user import UserInDB, UserInCreate


async def get_user(conn: AsyncIOMotorClient, username: str) -> UserInDB:
    row = await conn[database_name][users_collection_name].find_one({"username": username})
    if row:
        return UserInDB(**row)


async def get_user_by_email(conn: AsyncIOMotorClient, email: EmailStr) -> UserInDB:
    row = await conn[database_name][users_collection_name].find_one({"email": email})
    if row:
        return UserInDB(**row)


async def create_user(conn: AsyncIOMotorClient, user: UserInCreate) -> UserInDB:
    db_user = UserInDB(**user.dict())
    db_user.change_password(user.password)

    row = await conn[database_name][users_collection_name].insert_one(db_user.dict())

    db_user.id = row.inserted_id
    db_user.created_at = ObjectId(db_user.id).generation_time
    db_user.updated_at = ObjectId(db_user.id).generation_time

    return db_user
