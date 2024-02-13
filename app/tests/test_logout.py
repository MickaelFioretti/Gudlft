from server import app
from flask import url_for
import pytest
from utils import run_around_tests  # noqa: F401


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


# Test for logout route
def test_logout(client):
    response = client.get("/logout")
    assert response.status_code == 302  # Expecting redirection
    assert response.location.endswith(url_for("index"))  # Ensure redirection to index
