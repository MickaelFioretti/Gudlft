from server import app
from flask import url_for
import pytest
from utils import run_around_tests  # noqa: F401


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


# Test quand l'email n'est pas présent
def test_show_summary_without_email(client):
    response = client.post(
        "/showSummary", data={"email": "email_not_present@example.com"}
    )
    assert response.status_code == 302  # Redirection
    assert response.location.endswith(url_for("index"))


# Test quand l'email est présent
def test_show_summary_with_email(client):
    response = client.post("/showSummary", data={"email": "john@simplylift.co"})
    assert response.status_code == 200  # OK
