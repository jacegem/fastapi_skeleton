from starlette.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/api/article")
    assert response.status_code == 200
    assert response.json() == {'msg': 'article'}


def test_read_items():
    with TestClient(app) as client_with:
        response = client_with.get("/api/articles")
        assert response.status_code == 200
        assert response.json() == {'articles': [], 'articlesCount': 0}

