import pytest
from server import app
from utils import run_around_tests  # noqa: F401


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


# Test booking route with valid competition and club
def test_book_route_valid(client):
    response = client.get("/book/Spring%20Festival/Iron%20Temple")
    assert response.status_code == 200
    assert b"How many places?" in response.data


# Test booking route with invalid competition or club
def test_book_route_invalid(client):
    response = client.get("/book/Spring%20Festiva/Iron%20Temple")
    assert response.status_code == 200
    assert b"Something went wrong-please try again" in response.data
