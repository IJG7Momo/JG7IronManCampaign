
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
app.secret_key = "very_secret_key"

ADMIN_EMAIL = "moritzschmieden@gmail.com"

def get_db():
    conn = sqlite3.connect("users.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as db:
        db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                role TEXT DEFAULT 'user',
                status TEXT DEFAULT 'pending'
            )
        ''')
init_db()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        action = request.form.get("action")
        email = request.form.get("email")
        password = request.form.get("password")

        if action == "login":
            db = get_db()
            user = db.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
            if user and check_password_hash(user["password_hash"], password):
                if user["status"] != "approved":
                    flash("Your account is not approved yet.")
                    return redirect(url_for("index"))
                session["user_id"] = user["id"]
                session["username"] = user["username"]
                session["role"] = user["role"]
                return redirect(url_for("dashboard"))
            flash("Invalid credentials.")

        elif action == "register":
            username = request.form.get("username")
            password_hash = generate_password_hash(password)
            role = "admin" if email == ADMIN_EMAIL else "user"
            status = "approved" if email == ADMIN_EMAIL else "pending"
            try:
                db = get_db()
                db.execute("INSERT INTO users (username, email, password_hash, role, status) VALUES (?, ?, ?, ?, ?)",
                           (username, email, password_hash, role, status))
                db.commit()
                flash("Registration submitted. Wait for approval." if status == "pending" else "Admin registered.")
                return redirect(url_for("index"))
            except sqlite3.IntegrityError:
                flash("Email already registered.")
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("index"))
    return render_template("dashboard.html", username=session.get("username"), role=session.get("role"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))
