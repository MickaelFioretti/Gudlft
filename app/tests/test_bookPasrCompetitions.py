import pytest
from server import app, loadClubs, loadCompetitions
from utils import run_around_tests  # noqa: F401


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_booking_past_competition(client):
    club = loadClubs()[0]  # Utilisez un club de test
    competition = loadCompetitions()[0]  # Utilisez une compétition de test
    response = client.post(
        "/purchasePlaces",
        data={"club": club["name"], "competition": competition["name"], "places": "12"},
    )
    assert response.status_code == 200
    assert "Cannot book places for past competitions." in response.data.decode()


def test_booking_future_competition(client):
    club = loadClubs()[0]  # Utilisez un club de test
    competition = loadCompetitions()[2]  # Utilisez une compétition de test
    response = client.post(
        "/purchasePlaces",
        data={"club": club["name"], "competition": competition["name"], "places": "12"},
    )
    assert response.status_code == 200
    assert "Great-booking complete!" in response.data.decode()
