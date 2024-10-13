from TTS.api import TTS
from flask import Flask, request, jsonify

app = Flask(__name__)
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")
tts.to("cuda")

@app.route("/")
def index():
    return "<h1>Text to Speech</h1>"

@app.route("/tts", methods=['POST'])
def tts():
    input = request.json.get('input')

    tts.tts_to_file(text=input,
                file_path=f"output.wav",
                speaker_wav=["Recording.wav"],
                language="hi",
                split_sentences=True
                )

    return jsonify({"message": "TTS completed"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)