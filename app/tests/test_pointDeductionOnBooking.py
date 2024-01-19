from server import app, loadClubs, loadCompetitions
import pytest
from utils import run_around_tests  # noqa: F401


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_booking_deducts_points(client):
    club = loadClubs()[0]  # Prendre un club de test
    competition = loadCompetitions()[2]  # Prendre une compétition de test
    initial_points = int(club["points"])
    places_required = 2

    response = client.post(
        "/purchasePlaces",
        data={
            "club": club["name"],
            "competition": competition["name"],
            "places": str(places_required),
        },
    )

    assert response.status_code == 200
    assert "Great-booking complete!" in response.data.decode()

    updated_club = loadClubs()[0]
    assert int(updated_club["points"]) == initial_points - places_required
