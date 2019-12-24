from pydantic import BaseModel, EmailStr, UrlStr
from typing import Optional

from app.model.dbmodel import DBModelMixin


class UserBase(BaseModel):
    username: str
    email: EmailStr
    bio: Optional[str] = ""
    image: Optional[UrlStr] = None


class User(UserBase):
    token: str


class UserInDB(DBModelMixin, UserBase):
    salt: str = ""
    hashed_password: str = ""

    def check_password(self, password: str):
        return verify_password(self.salt + password, self.hashed_password)

    def change_password(self, password: str):
        self.salt = generate_salt()
        self.hashed_password = get_password_hash(self.salt + password)
