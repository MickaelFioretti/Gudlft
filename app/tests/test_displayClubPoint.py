from server import app, loadClubs
import pytest
from utils import run_around_tests  # noqa: F401


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_club_list_display_after_login(client):
    response = client.post(
        "/showSummary", data={"email": "john@simplylift.co"}, follow_redirects=True
    )

    assert response.status_code == 200

    # Regarde si le nom des clubs est présent dans la page
    clubs = loadClubs()
    for club in clubs:
        assert club["name"] in response.data.decode()
        assert club["points"] in response.data.decode()
