import pytest
from server import app, loadClubs, loadCompetitions
from utils import run_around_tests  # noqa: F401


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_booking_limit_exceeded(client):
    club = loadClubs()[0]  # Utilisez un club de test
    competition = loadCompetitions()[2]  # Utilisez une compétition de test
    response = client.post(
        "/purchasePlaces",
        data={"club": club["name"], "competition": competition["name"], "places": "13"},
    )
    assert response.status_code == 200
    assert (
        "Cannot book more than 12 places for a competition." in response.data.decode()
    )


def test_booking_not_exceeding_12_places(client):
    club = loadClubs()[0]  # Utilisez un club de test
    competition = loadCompetitions()[2]  # Utilisez une compétition de test
    response = client.post(
        "/purchasePlaces",
        data={"club": club["name"], "competition": competition["name"], "places": "12"},
    )
    assert response.status_code == 200
    assert "Great-booking complete!" in response.data.decode()
