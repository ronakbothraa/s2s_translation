from app import app
from flask import render_template, request, jsonify, make_response
from s2translation import SpeechToTranslate
from threading import Thread, active_count

s2t = SpeechToTranslate(input_lang="en", output_lang="hin_Deva")
@app.route("/")
def index():
    return render_template("public/home.html", 
                           output_languages=s2t.output_languages, 
                           input_languages=s2t.input_languages)

@app.route("/start", methods=["POST"])
def start_process():
    data = request.get_json()
    s2t.input_lang = data.get('inputLanguage')
    s2t.output_lang = data.get('outputLanguage')
    

    s2t.transcribed_text.queue.clear()
    s2t.translated_text.queue.clear()
    s2t.full_transcribed_text = []


    s2t.messages.put(True)

    recording = Thread(target=s2t.record_microphone)
    recording.start()
    
    transcribing = Thread(target=s2t.transcript)
    transcribing.start()
    
    return "started recording"

@app.route("/stop", methods=["POST"])
def stop_process():
    s2t.stop_recording()
    return "stopped recording"

@app.route("/transcript", methods=["POST"])
def transcription():

    a = s2t.transcribed_text.get()
    translation = Thread(target=s2t.translate, args=(" ".join(s2t.full_transcribed_text), ))
    translation.start()
    
    return jsonify({"transcript": a})


@app.route("/translate", methods=["POST"])
def translation():
    a = s2t.translated_text.get()
    return jsonify({"translation": a})



