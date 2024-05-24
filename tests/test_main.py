import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "테스트 화면"}


def test_read_item():
    item_id = 1
    response = client.get(f"/items/{item_id}")
    assert response.status_code == 200
    assert response.json() == {"message": f"item_id로 {item_id} 받음"}
