from app import app
from flask import render_template, request, jsonify, make_response
from s2translation import SpeechToTranslate
import requests
from pydub import AudioSegment
from pydub.playback import play
import os


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
    
    s2t.start_recording()
    return jsonify({"transcript": "started"})

@app.route("/stop", methods=["POST"])
def stop_process():
    s2t.stop_recording()
    return "stopped recording"

@app.route("/transcript", methods=["POST"])
def transcription():
    isRecording = request.get_json().get("isRecording")
    if (not s2t.transcribed_text.empty() or not s2t.recordings.empty() or isRecording):
        a = s2t.transcribed_text_copy.get()
        return jsonify({"transcript": a})
    return jsonify({"transcript": False})


@app.route("/translate", methods=["POST"])
def translation():
    isRecording = request.get_json().get("isRecording")
    if (not s2t.translated_text.empty() or not s2t.transcribed_text.empty() or isRecording):
        a = s2t.translated_text.get()
        return jsonify({"translation": a})
    return jsonify({"translation": False})


@app.route('/tts', methods=['POST'])
def generate_tts():
    input_text = request.get_json().get('translatedData')
    try:
        response = requests.post("http://127.0.0.1:8000/tts", json={"input": input_text})
        print(f"TTS API response: {response.status_code}, {response.text}")
        if response.status_code == 200:
            audio = AudioSegment.from_wav("text_to_speech/output.wav")
            play(audio)
            os.remove(f"saved_audio_files/audio.wav")
            return jsonify({"message": "TTS generation complete"}), 200
        else:
            return jsonify({"error": "TTS generation failed", "details": response.text}), 500
    except Exception as e:
        print(f"Error in generate_tts: {e}")
        return jsonify({"error": "Internal server error"}), 500
