from datetime import datetime

from sqlmodel import Session, select

from model import shortUrlModel


def get_short_url_by_url(session: Session, url: str):
    statement = select(shortUrlModel.ShortUrl).where(shortUrlModel.ShortUrl.url == url)
    session_short_url = session.exec(statement).first()
    return session_short_url

def get_short_url_by_short_key(session: Session, key: str):
    statement = select(shortUrlModel.ShortUrl).where(shortUrlModel.ShortUrl.short_key == key)
    session_short_url = session.exec(statement).first()
    return session_short_url

def create_short_url(session: Session, short_url: shortUrlModel.ShortUrl):
    db_short_url = shortUrlModel.ShortUrl.model_validate(short_url)
    session.add(db_short_url)
    session.commit()
    session.refresh(db_short_url)
    return db_short_url

def update_short_url(session: Session, key: str, date: datetime):
    statement = select(shortUrlModel.ShortUrl).where(shortUrlModel.ShortUrl.short_key == key)
    session_short_url = session.exec(statement).first()
    session_short_url.expiration_date = date
    session_short_url.views = 0
    session.add(session_short_url)
    session.commit()
    session.refresh(session_short_url)

def delete_short_url(session: Session, key: str):
    statement = select(shortUrlModel.ShortUrl).where(shortUrlModel.ShortUrl.short_key == key)
    session_short_url = session.exec(statement).first()
    session.delete(session_short_url)
    session.commit()

def update_short_url_views(session: Session, key: str):
    statement = select(shortUrlModel.ShortUrl).where(shortUrlModel.ShortUrl.short_key == key)
    session_short_url = session.exec(statement).first()
    session_short_url.views += 1
    session.add(session_short_url)
    session.commit()
    session.refresh(session_short_url)