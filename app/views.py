from app import app

from flask import render_template

@app.route("/")
def hello():
    a = "ronak"
    return render_template("home.html")