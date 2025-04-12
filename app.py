
from flask import Flask, render_template, request, redirect, session
app = Flask(__name__)
app.secret_key = "geheim"

@app.route("/")
def home():
    return "Willkommen im Geschwader-Logbuch!"

if __name__ == "__main__":
    app.run(debug=True)
