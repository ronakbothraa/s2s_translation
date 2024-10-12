from app import app
from flask import render_template, request, jsonify
from s2translation import SpeechToTranslate
from threading import Thread


s2t = SpeechToTranslate(input_lang="en", output_lang="hin_Deva")
@app.route("/")
def index():
    return render_template("public/home.html")

@app.route("/start", methods=["POST"])
def start_process():
    s2t.messages.put(True)

    recording = Thread(target=s2t.record_microphone)
    recording.start()
    
    transcribing = Thread(target=s2t.transcription)
    transcribing.start()
    return "something"

@app.route("/stop", methods=["POST"])
def stop_process():
    s2t.stop_recording()
    return "something"

@app.route("/process", methods=["POST"])
def transcription():
    a = s2t.transcribed_text.get()
    return jsonify({"transcript": a})