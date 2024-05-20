from datetime import datetime

from sqlmodel import Field, SQLModel


class ShortUrlBase(SQLModel):
    url: str = Field(unique=True)
    expiration_date: datetime

class ShortUrl(ShortUrlBase, table=True):
    short_key: str = Field(primary_key=True)
    views: int = 0

class UrlInput(SQLModel):
    url: str
    expiration_hour: int = 24 * 14

class ShortUrlOnly(SQLModel):
    short_url: str