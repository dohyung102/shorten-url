from sqlmodel import create_engine, Session


DATABASE_URL = 'sqlite:///./test/test_develop.db'

engine = create_engine(
    DATABASE_URL, pool_size=1
)

def get_test_session():
    with Session(engine) as session:
        yield session