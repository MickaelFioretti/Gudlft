from server import app, loadClubs, loadCompetitions
import pytest
from utils import run_around_tests  # noqa: F401


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_purchase_places_with_sufficient_points(client):
    clubs = loadClubs()
    competitions = loadCompetitions()
    sufficient_points_club = clubs[0]  # "Simply Lift" avec 13 points
    competition = competitions[0]  # "Spring Festival" avec 25 places disponibles

    response = client.post(
        "/purchasePlaces",
        data={
            "club": sufficient_points_club["name"],
            "competition": competition["name"],
            "places": "5",
        },
    )
    assert response.status_code == 200  # OK
    assert "Great-booking complete!" in response.data.decode()


def test_purchase_places_with_insufficient_points(client):
    clubs = loadClubs()
    competitions = loadCompetitions()
    insufficient_points_club = clubs[1]  # "Iron Temple" avec 4 points
    competition = competitions[0]  # "Spring Festival"

    response = client.post(
        "/purchasePlaces",
        data={
            "club": insufficient_points_club["name"],
            "competition": competition["name"],
            "places": "5",  # Plus que les points disponibles
        },
    )
    assert response.status_code == 200  # OK, mais avec message d'erreur
    assert (
        "You don&#39;t have enough points for this booking." in response.data.decode()
    )
