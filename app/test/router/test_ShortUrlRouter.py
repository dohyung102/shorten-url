from fastapi.testclient import TestClient
from sqlmodel import SQLModel

from main import app
from database import get_session
from test.database_test import get_test_session, engine


app.dependency_overrides[get_session] = get_test_session
SQLModel.metadata.drop_all(engine)
SQLModel.metadata.create_all(engine)

client = TestClient(app)

class ShortUrl():
    def __init__(self):
        self.exist_short_url = ''
    
    def set_exist_short_url(self, url):
        self.exist_short_url = url

    def get_exist_short_url(self):
        return self.exist_short_url

short_url = ShortUrl()


def test_create_short_url():
    data = {
        'url': 'https://fastapi.tiangolo.com/ko/'
    }
    response = client.post(
        '/shorten',
        json=data
    )
    assert response.status_code == 200
    content = response.json()
    assert 'short_url' in content
    short_url.set_exist_short_url(content['short_url'])

def test_redirect_short_url():
    short_key = short_url.get_exist_short_url().split('/')[-1]
    response = client.get(
        f'/{short_key}'
    )

def test_non_exist_short_url():
    response = client.get(
        '/adaaaadaddaaadaada'
    )
    assert response.status_code == 404

def test_get_exist_short_url_views():
    short_key = short_url.get_exist_short_url().split('/')[-1]
    response = client.get(
        f'/stat/{short_key}'
    )
    assert response.status_code == 200

def test_get_non_exist_short_url_view():
    response = client.get(
        '/stat/adaaaadaddaaadaada'
    )
    assert response.status_code == 404