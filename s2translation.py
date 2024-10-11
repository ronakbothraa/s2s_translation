import pyaudio, wave, os, torch, keyboard
import numpy as np
from faster_whisper import WhisperModel
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from queue import Queue
from threading import Thread

class SpeechToTranslate:
    def __init__(self, input_lang, output_lang):
        self.input_lang = input_lang
        self.output_lang = output_lang

        self.messages = Queue()
        self.recordings = Queue()
        self.transcribed_text = Queue()
        self.full_transcribed_text = []

        self.CHANNELS = 1
        self.FRAME_RATE = 16000
        self.RECORD_SECONDS = 3
        self.FORMAT = pyaudio.paInt16

        self.transcription_model = WhisperModel("medium", device="cuda" if torch.cuda.is_available() else "cpu", compute_type="float16" if torch.cuda.is_available() else "int8")

        self.translated_text = []
        self.tokenizer = AutoTokenizer.from_pretrained("facebook/nllb-200-distilled-600M")
        self.translation_model = AutoModelForSeq2SeqLM.from_pretrained("facebook/nllb-200-distilled-600M")


    def record_microphone(self, chunk=1024):
        p = pyaudio.PyAudio()
        stream = p.open(format=self.FORMAT,
                    channels=self.CHANNELS,
                    rate=self.FRAME_RATE,
                    input=True,
                    input_device_index=1,
                    frames_per_buffer=chunk)
        
        frames = []
        
        while not self.messages.empty():
            data = stream.read(chunk)
            frames.append(data)
            if len(frames) >= (self.FRAME_RATE * self.RECORD_SECONDS) / chunk:

                if np.max(np.abs(np.frombuffer(b''.join(frames), dtype=np.int16))) < 1000:
                    self.stop_recording()

                self.recordings.put(frames.copy())
                frames = []
                i = 0
        
        stream.stop_stream()
        stream.close()
        p.terminate()

    def transcription(self):
        while not self.messages.empty():
            frames = self.recordings.get()

            with wave.open("audio.wav", 'wb') as wf:
                wf.setnchannels(self.CHANNELS)
                wf.setsampwidth(2)
                wf.setframerate(self.FRAME_RATE)
                wf.writeframes(b''.join(frames))

            segments, _ = self.transcription_model.transcribe(f'audio.wav', beam_size=5)
            text = " ".join([segment.text for segment in segments])
            self.transcribed_text.put(text)
            self.full_transcribed_text.append(text)
            print(f"live transcription: ", text)
            os.remove(f"audio.wav")
            
            if keyboard.is_pressed('q'):
                self.stop_recording()

    def translate(self, trnscrpt=""):
        while not self.messages.empty() or trnscrpt != "":
            if trnscrpt == "":
                text = self.transcribed_text.get()
            else:
                text = trnscrpt
            inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True)
            inputs = {k: inputs[k].to(self.translation_model.device) for k in inputs}
            outputs = self.translation_model.generate(**inputs, forced_bos_token_id=self.tokenizer.convert_tokens_to_ids(self.output_lang))
            outputs = self.tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]
            self.translated_text.append(outputs)
            trnscrpt = ""


    def start_recording(self):
        self.messages.put(True)

        print("Start Recording:")
        recording = Thread(target=self.record_microphone)
        recording.start()
        
        transcribing = Thread(target=self.transcription)
        transcribing.start()

        translation = Thread(target=self.translate, args=())
        translation.start()


    def stop_recording(self):
        self.messages.get()
        torch.cuda.empty_cache()
        print("Translated Text: ", " ".join(self.translated_text))


if __name__ == "__main__":
    a = SpeechToTranslate(input_lang="en", output_lang="hin_Deva")
    a.start_recording()