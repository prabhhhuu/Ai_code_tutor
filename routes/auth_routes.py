from flask import Blueprint, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_db

auth_bp = Blueprint("auth", __name__)


# LOGIN PAGE
@auth_bp.route("/")
@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        db = get_db()

        user = db.execute(
            "SELECT * FROM users WHERE email=?",
            (email,)
        ).fetchone()

        db.close()

        if user and check_password_hash(user["password_hash"], password):

            session["user"] = user["username"]

            return redirect("/editor")

        return "Invalid login"

    return render_template("login.html")


# REGISTER PAGE
@auth_bp.route("/register", methods=["GET","POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        hashed = generate_password_hash(password)

        db = get_db()

        db.execute(
            "INSERT INTO users (username,email,password_hash) VALUES (?,?,?)",
            (username,email,hashed)
        )

        db.commit()
        db.close()

        return redirect("/login")

    return render_template("register.html")


# LOGOUT
@auth_bp.route("/logout")
def logout():

    session.clear()

    return redirect("/login")
