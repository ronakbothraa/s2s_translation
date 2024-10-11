from app import app
from flask import render_template, request
from s2translation import SpeechToTranslate
from threading import Thread


s2t = SpeechToTranslate(input_lang="en", output_lang="hin_Deva")
@app.route("/")
def index():
    return render_template("public/home.html")

@app.route("/process", methods=["POST"])
def transcription():
    s2t.messages.put(True)

    recording = Thread(target=s2t.record_microphone)
    recording.start()
    
    transcribing = Thread(target=s2t.transcription)
    transcribing.start()