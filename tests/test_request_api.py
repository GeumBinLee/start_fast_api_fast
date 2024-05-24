import pytest

from app.services.request_api import get, post


def test_get():
    response = get("https://jsonplaceholder.typicode.com/posts", {})
    assert response.status_code == 200


def test_post():
    response = post(
        "https://jsonplaceholder.typicode.com/posts",
        {},
        {"title": "foo", "body": "bar", "userId": 1},
    )
    assert response.status_code == 201
