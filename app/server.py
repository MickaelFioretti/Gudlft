import json
from datetime import datetime
from flask import Flask, render_template, request, redirect, flash, url_for


def loadClubs():
    with open("clubs.json", mode="r", encoding="utf-8") as c:
        listOfClubs = json.load(c)["clubs"]
        return listOfClubs


def loadCompetitions():
    with open("competitions.json", mode="r", encoding="utf-8") as comps:
        listOfCompetitions = json.load(comps)["competitions"]
        return listOfCompetitions


app = Flask(__name__)
app.secret_key = "something_special"

if __name__ == "__main__":
    app.run(debug=True)

competitions = loadCompetitions()
clubs = loadClubs()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/showSummary", methods=["POST"])
def showSummary():
    email = request.form.get("email")
    matched_clubs = [c for c in clubs if c["email"] == email]

    # Vérifier si l'adresse e-mail est dans le fichier JSON
    if not matched_clubs:
        flash("Sorry, we don't have your email address on file!")
        return redirect(url_for("index"))
    else:
        club = matched_clubs[0]
        return render_template(
            "welcome.html", club=club, competitions=competitions, clubs=clubs
        )


@app.route("/book/<competition>/<club>")
def book(competition, club):
    foundClub = [c for c in clubs if c["name"] == club]
    foundCompetition = [c for c in competitions if c["name"] == competition]
    if foundClub and foundCompetition:
        return render_template(
            "booking.html", club=foundClub[0], competition=foundCompetition[0]
        )
    else:
        flash("Something went wrong-please try again")
        return render_template(
            "welcome.html", club=club, competitions=competitions, clubs=clubs
        )


@app.route("/purchasePlaces", methods=["POST"])
def purchasePlaces():
    competitions = loadCompetitions()
    clubs = loadClubs()

    competition = [c for c in competitions if c["name"] == request.form["competition"]][
        0
    ]
    club = [c for c in clubs if c["name"] == request.form["club"]][0]
    placesRequired = int(request.form["places"])

    # Vérifier si la date de la compétition est passée
    if datetime.now() > datetime.strptime(competition["date"], "%Y-%m-%d %H:%M:%S"):
        flash("Cannot book places for past competitions.")
        return render_template(
            "welcome.html", club=club, competitions=competitions, clubs=clubs
        )

    # Vérifier si le nombre de places demandées dépasse 12
    if placesRequired > 12:
        flash("Cannot book more than 12 places for a competition.")
        return render_template(
            "welcome.html", club=club, competitions=competitions, clubs=clubs
        )

    # Vérification des points disponibles
    if placesRequired > int(club["points"]):
        flash("You don't have enough points for this booking.")
        return render_template(
            "welcome.html", club=club, competitions=competitions, clubs=clubs
        )

    # Mise à jour des points du club et des places disponibles dans la compétition
    competition["numberOfPlaces"] = int(competition["numberOfPlaces"]) - placesRequired
    club["points"] = int(club["points"]) - placesRequired

    # Mise à jour du fichier JSON
    with open("clubs.json", mode="w", encoding="utf-8") as c:
        json.dump({"clubs": clubs}, c)

    with open("competitions.json", mode="w", encoding="utf-8") as comps:
        json.dump({"competitions": competitions}, comps)

    flash("Great-booking complete!")
    return render_template(
        "welcome.html", club=club, competitions=competitions, clubs=clubs
    )


# TODO: Add route for points display


@app.route("/logout")
def logout():
    return redirect(url_for("index"))
