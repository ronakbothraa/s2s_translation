from app import app
from flask import render_template, request, jsonify, make_response
from s2translation import SpeechToTranslate
from threading import Thread

s2t = SpeechToTranslate(input_lang="en", output_lang="hin_Deva")
@app.route("/")
def index():
    return render_template("public/home.html", 
                           output_languages=s2t.output_languages, 
                           input_languages=s2t.input_languages)

@app.route("/start", methods=["POST"])
def start():
    data = request.get_json()
    s2t.input_lang = data.get('inputLanguage')
    s2t.output_lang = data.get('outputLanguage')
    
    s2t.recordings.queue.clear()
    s2t.transcribed_text.queue.clear()
    s2t.translated_text.queue.clear()
    s2t.full_transcribed_text.queue.clear()
    s2t.full_translated_text.queue.clear()

    s2t.messages.put(True)

    recording = Thread(target=s2t.record_microphone)
    recording.start()

    transcribing = Thread(target=s2t.transcript)
    transcribing.start()

    translation = Thread(target=s2t.translate)
    translation.start()
    
    print("started")
    return jsonify({"transcript": "started"})

@app.route("/stop", methods=["POST"])
def stop_process():
    s2t.stop_recording()
    return "stopped recording"

@app.route("/transcript", methods=["POST"])
def transcription():
    isRecording = request.get_json().get("isRecording")
    print(isRecording, ": isRecording in transcription function/route")
    if (not s2t.transcribed_text.empty() or not s2t.recordings.empty() or isRecording):
        a = s2t.full_transcribed_text.get()
        return jsonify({"transcript": a})
    return jsonify({"transcript": False})


@app.route("/translate", methods=["POST"])
def translation():
    isRecording = request.get_json().get("isRecording")
    print(isRecording, ": isRecording in translation function/route")
    if (not s2t.translated_text.empty() or not s2t.transcribed_text.empty() or isRecording):
        a = s2t.translated_text.get()
        return jsonify({"translation": a})
    return jsonify({"translation": False})


@app.route('/generate_tts', methods=['POST'])
def generate_tts():
    input_text = request.json.get("input")
    response = request.post("http://127.0.0.1:5001/tts", json={"input": input_text})

    if response.status_code == 200:
        return jsonify({"message": "TTS generation complete"}), 200
    
    return jsonify({"error": "Failed to generate TTS"}), 500
