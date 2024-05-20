from sqlmodel import create_engine, Session

import os


DATABASE_URL = 'sqlite:///./develop.db'

engine = create_engine(
    DATABASE_URL, pool_size=1
)

def get_session():
    with Session(engine) as session:
        yield session