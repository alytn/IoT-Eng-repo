from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session, flash
from datetime import timedelta
from database import users, db

views = Blueprint(__name__,"views", static_folder="static", template_folder="templates")

@views.route("/")
def home():
    return render_template("home.html", name="Test Name")

@views.route("/profile")
def profile():
    return render_template("profile.html")

@views.route("/json")
def get_json():
    return jsonify({'name': 'Aly', 'coolness': 10})

@views.route("/data")
def get_data():
    data = request.json
    return jsonify(data)

@views.route("/go-to-home")
def go_to_home():
    return redirect(url_for("views.home"))

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

@views.route("/players")
def players():
    return render_template("players.html", values=users.query.all())


@views.route("/logout")
def logout():
    flash(f"You have been logged out.", "info")
    if "user" in session:
        user = session["user"]
    session.pop("user", None)
    session.pop("email", None)
    return redirect(url_for("views.login"))


