from typing import Optional

from pydantic import BaseModel


class CastIn(BaseModel):
    name: str
    nationality: Optional[str] = None


class CastOut(CastIn):
    id: int


class CastUpdate(CastIn):
    name: Optional[str] = None
