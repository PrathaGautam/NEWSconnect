import pytest
from fastapi.testclient import TestClient
from main import app


@pytest.fixture
def client():
    return TestClient(app)


def test_index(client):
    responses = [client.get("/"), client.get("/search"), client.get("/showallheadings")]
    for response in responses:
        assert response.status_code == 200


def test_show_all_headings(client):
    response = client.get("/showallheadings")
    # assert response.status_code == 200
    print("Response content : ", response.text)
    assert "text/html" in response.headers["content-type"]
    assert "request" in response.context
    assert "headings" in response.context
    assert "number_of_news" in response.context


def test_search(client):
    query = "example"
    response = client.get("/search", params={"query": query})
    # assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "request" in response.context
    assert "headings" in response.context
    assert "query" in response.context
    assert "number_of_filtered_headings" in response.context


# test for invalid endpoint
def test_invalid_endpoint(client):
    response = client.get("/invalid!!")
    assert response.status_code == 404


