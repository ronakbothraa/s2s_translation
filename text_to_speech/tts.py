from TTS.api import TTS
from flask import Flask, request, jsonify

app = Flask(__name__)

tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")
tts.to("cuda")

@app.route("/")
def index():
    return "<h1>Text to Speech</h1>"

@app.route("/tts", methods=['POST'])
def testtospeech():
    input = request.get_json().get('input')
    try :
        tts.tts_to_file(
                    text=input,
                    file_path=f"output.wav",
                    speaker_wav=["../saved_audio_files/audio.wav"],
                    language="hi",
                    split_sentences=True
        )
        return jsonify({"message": "TTS completed"}), 200
    except Exception as e:
        return jsonify({"message": "Error in TTS"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)