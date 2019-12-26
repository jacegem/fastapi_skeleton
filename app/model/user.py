from pydantic import BaseModel, EmailStr, UrlStr
from typing import Optional

from app.core.security import verify_password, generate_salt, get_password_hash
from app.model.dbmodel import DBModelMixin
from app.model.rwmodel import RWModel


class UserBase(BaseModel):
    username: str
    email: EmailStr
    bio: Optional[str] = ""
    image: Optional[UrlStr] = None


class User(UserBase):
    token: str


class UserInLogin(RWModel):
    email: EmailStr
    password: str


class UserInCreate(UserInLogin):
    username: str


class UserInResponse(RWModel):
    user: User


class UserInDB(DBModelMixin, UserBase):
    salt: str = ""
    hashed_password: str = ""

    def check_password(self, password: str):
        return verify_password(self.salt + password, self.hashed_password)

    def change_password(self, password: str):
        self.salt = generate_salt()
        self.hashed_password = get_password_hash(self.salt + password)
