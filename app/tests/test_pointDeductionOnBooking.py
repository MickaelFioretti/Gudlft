import json
from server import app, loadClubs, loadCompetitions
import pytest


# Fonction pour réinitialiser les données des clubs
def reset_clubs_data():
    original_data = {
        "clubs": [
            {"name": "Simply Lift", "email": "john@simplylift.co", "points": "13"},
            {"name": "Iron Temple", "email": "admin@irontemple.com", "points": "4"},
            {"name": "She Lifts", "email": "kate@shelifts.co.uk", "points": "12"},
        ]
    }
    with open("clubs.json", "w") as c:
        json.dump(original_data, c)


# Hook de pytest pour réinitialiser les données après chaque test
@pytest.fixture(autouse=True)
def run_around_tests():
    # Avant chaque test
    yield
    # Après chaque test
    reset_clubs_data()


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_booking_deducts_points(client):
    club = loadClubs()[0]  # Prendre un club de test
    competition = loadCompetitions()[0]  # Prendre une compétition de test
    initial_points = int(club["points"])
    places_required = 3

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

    updated_club = [c for c in loadClubs() if c["name"] == club["name"]][0]
    assert int(updated_club["points"]) == initial_points - places_required
