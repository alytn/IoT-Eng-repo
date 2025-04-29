from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session, flash
from datetime import timedelta
from webApp.database import users, db
import requests

views = Blueprint("views", __name__, static_folder="static", template_folder="templates")

@views.route("/")
def home():
    return render_template("home.html", name="Test Name")

@views.route("/profile")
def profile():
    return render_template("profile.html")

@views.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form["nm"]
        session["user"] = user
        found_user = users.query.filter_by(username=user).first()
        ### found_user = users.query.filter_by(username=user).first() to delete one
        ### for user in found_user:
            ### user.delete() to delete all
        if found_user:
            session["email"] = found_user.email
        else:
            usr = users(user, "")
            db.session.add(usr)
            db.session.commit()
        flash("Logged in successfully :D")
        return redirect(url_for("views.user", user=user))
    else:
        if "user" in session:
            flash("Dawg, you're already logged in...")
            return redirect(url_for("views.user", user=session["user"]))

        return render_template("login.html")

@views.route("/<user>", methods=["POST", "GET"])
def user(user):
    email = None
    if "user" in session:
        user = session["user"]
        if request.method == "POST":
            email = request.form["email"]
            session["email"] = email
            found_user = users.query.filter_by(username=user).first()
            found_user.email = email
            db.session.commit()
            flash("Your email was saved. Prepare for spam.")
        else:
            if "email" in session:
                email = session["email"]
        return render_template("user.html", email=email)
    else:
        flash("Bye lol, you're not logged in.")
        return redirect(url_for("views.login", user=user))

@views.route("/logout")
def logout():
    flash(f"You have been logged out.", "info")
    if "user" in session:
        user = session["user"]
    session.pop("user", None)
    session.pop("email", None)
    return redirect(url_for("views.login"))

NGROK = "https://a560-2601-140-8d00-6bb0-caf9-4147-b9be-47df.ngrok-free.app"

@views.route("/turnon", methods=["POST"])
def turnon():
    try:
        requests.get(f"{NGROK}/led/on")
        flash("LED has been on!", "success")
    except Exception as e:
        flash(f"Error for LED: {e}")
    return redirect(url_for("views.home"))

@views.route("/turnoff", methods=["POST"])
def turnoff():
    try:
        requests.get(f"{NGROK}/led/off")
        flash("LED has been turned off!", "success")
    except Exception as e:
        flash(f"Error for LED: {e}")
    return redirect(url_for("views.home"))

@views.route("/turnblink", methods=["POST"])
def turnblink():
    try:
        requests.get(f"{NGROK}/led/blink")
        flash("LED now blinking!", "success")
    except Exception as e:
        flash(f"Error for LED: {e}")
    return redirect(url_for("views.home"))

@views.route("/surprise")
def surprise():
	return render_template("surprise.html")

@views.route("/gashapon", methods=["POST"])
def gashapon():
    try:
        requests.get(f"{NGROK}/surprise")
        flash("Surprise!", "success")
    except Exception as e:
        flash(f"Failed to activate servo: {e}", "danger")
    return redirect(url_for("views.home"))

@views.route("/players")
def players():
    players_all = users.query.all()
    usernames = [player.username for player in players_all]

    try:
        response = requests.post(f"{NGROK}/sort_players", json={"usernames": usernames})
        if response.status_code == 200:
            alphabetized_usernames = response.json().get('alphabetized_usernames', [])
        else:
            alphabetized_usernames = usernames
    except Exception as e:
        print(f"Yeah this alphabet thing still isn't working :(: {e}")
        sorted_usernames = usernames 
    return render_template("players.html", players=alphabetized_usernames)
