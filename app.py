
from flask import Flask, render_template, session, redirect, request, url_for

app = Flask(__name__)
app.secret_key = 'very_secret_key'

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username and password:
            session["user"] = username
            return redirect(url_for("dashboard"))
    if "user" in session:
        return redirect(url_for("dashboard"))
    return render_template("pages/index.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("index"))

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("index"))
    return render_template("pages/dashboard.html", user=session["user"])
