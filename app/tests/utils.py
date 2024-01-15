import json
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
    with open("clubs.json", mode="w", encoding="utf-8") as c:
        json.dump(original_data, c)


# Fonction pour réinitialiser les données des compétitions
def reset_competitions_data():
    original_data = {
        "competitions": [
            {
                "name": "Spring Festival",
                "date": "2020-03-27 10:00:00",
                "numberOfPlaces": "25",
            },
            {
                "name": "Fall Classic",
                "date": "2020-10-22 13:30:00",
                "numberOfPlaces": "13",
            },
        ]
    }
    with open("competitions.json", mode="w", encoding="utf-8") as c:
        json.dump(original_data, c)


# Hook de pytest pour réinitialiser les données après chaque test
@pytest.fixture(autouse=True)
def run_around_tests():
    # Avant chaque test
    reset_clubs_data()
    reset_competitions_data()
    yield
    # Après chaque test
    reset_clubs_data()
    reset_competitions_data()
