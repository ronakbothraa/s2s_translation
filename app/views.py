from app import app

from flask import render_template

@app.route("/")
def hello():
    # a = SpeechToTranslate(input_lang="en", output_lang="hin_Deva")
    return render_template("home.html")