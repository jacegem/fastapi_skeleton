from datetime import datetime, timedelta
from typing import Optional

import jwt
from fastapi import Depends, HTTPException, Header
from jwt import PyJWTError

from motor.motor_asyncio import AsyncIOMotorClient
from starlette.status import HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND

from app.core.config import SECRET_KEY, JWT_TOKEN_PREFIX
from app.crud.user import get_user
from app.db.mongodb import get_database
from app.model.token import TokenPayload
from app.model.user import User

ALGORITHM = "HS256"
access_token_jwt_subject = "access"


def _get_authorization_token(authorization: str = Header(...)):
    token_prefix, token = authorization.split(" ")
    if token_prefix != JWT_TOKEN_PREFIX:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Invalid authorization type"
        )

    return token


async def _get_current_user(
        db: AsyncIOMotorClient = Depends(get_database), token: str = Depends(_get_authorization_token)
) -> User:
    try:
        payload = jwt.decode(token, str(SECRET_KEY), algorithms=[ALGORITHM])
        token_data = TokenPayload(**payload)
    except PyJWTError:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )

    db_user = await get_user(db, token_data.username)
    if not db_user:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="User not found")

    user = User(**db_user.dict(), token=token)
    return user


def _get_authorization_token_optional(authorization: str = Header(None)):
    if authorization:
        return _get_authorization_token(authorization)
    return ""


async def _get_current_user_optional(
        db: AsyncIOMotorClient = Depends(get_database),
        token: str = Depends(_get_authorization_token_optional),
) -> Optional[User]:
    if token:
        return await _get_current_user(db, token)

    return None


def get_current_user_authorizer(*, required: bool = True):
    if required:
        return _get_current_user
    else:
        return _get_current_user_optional


def create_access_token(*, data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire, "sub": access_token_jwt_subject})
    encoded_jwt = jwt.encode(to_encode, str(SECRET_KEY), algorithm=ALGORITHM)
    return encoded_jwt
