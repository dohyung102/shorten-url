from fastapi.testclient import TestClient
from sqlmodel import SQLModel

from main import app
from database import get_session
from test.database_test import get_test_session, engine


app.dependency_overrides[get_session] = get_test_session
SQLModel.metadata.create_all(engine)

client = TestClient(app)


def test_create_short_url():
    data = {
        'url': 'www.naver.com'
    }
    response = client.post(
        "/shorten",
        json=data
    )
    assert response.status_code == 200
    content = response.json()
    assert 'short_url' in content