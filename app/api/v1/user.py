from datetime import timedelta

from fastapi import APIRouter, Depends, Body, HTTPException
from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorClient
from starlette.responses import JSONResponse
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.core.jwt import get_current_user_authorizer, create_access_token
from app.crud.shortcuts import check_free_username_and_email
from app.crud.user import create_user, get_user_by_email
from app.db.mongodb import get_database
from app.model.user import UserInResponse, User, UserInCreate, UserInLogin

router = APIRouter()


@router.get("/user", response_model=UserInResponse, tags=["users"])
async def retrieve_current_user(user: User = Depends(get_current_user_authorizer())):
    return UserInResponse(user=user)


@router.get("/user2")
async def retrieve_current_user2():
    user_data = {
        "username": 'username',
        "email": 'user email',
        "token": 'user token'
    }
    user = User(
        username='username',
        email='user@email.com',
        token='user token'
    )

    return JSONResponse(content=jsonable_encoder(user))


@router.post(
    '/users',
    response_model=UserInResponse,
    tags=['authentication'],
    status_code=HTTP_201_CREATED
)
async def register(
        # user: UserInCreate = Body(..., embed=True),
        user: UserInCreate = Body(..., embed=True),
        db: AsyncIOMotorClient = Depends(get_database)
):
    await check_free_username_and_email(db, user.username, user.email)

    async with await db.start_session() as s:
        async with s.start_transaction():
            db_user = await create_user(db, user)
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            token = create_access_token(
                data={"username": db_user.username},
                expires_delta=access_token_expires,
            )

            return UserInResponse(user=User(**db_user.dict(), token=token))


@router.post('/users/login', response_model=UserInResponse, tags=['authentication'])
async def login(
        user: UserInLogin = Body(..., embed=True),
        db: AsyncIOMotorClient = Depends(get_database)
):
    db_user = await get_user_by_email(db, user.email)
    if not db_user or not db_user.check_password(user.password):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token(data={"username": db_user.username}, expires_delta=access_token_expires)

    return UserInResponse(user=User(**db_user.dict(), token=token))
