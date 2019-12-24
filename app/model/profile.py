from typing import Optional

from pydantic import UrlStr

from app.model.rwmodel import RWModel


class Profile(RWModel):
    username: str
    bio: Optional[str] = ""
    image: Optional[UrlStr] = None
    following: bool = False

