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

        self.translated_text = Queue()
        self.tokenizer = AutoTokenizer.from_pretrained("facebook/nllb-200-distilled-600M")
        self.translation_model = AutoModelForSeq2SeqLM.from_pretrained("facebook/nllb-200-distilled-600M")

        self.languages = {"ace_Arab": "Achinese (Arabic script)","ace_Latn": "Achinese (Latin script)","acm_Arab": "Iraqi Arabic (Arabic script)","acq_Arab": "Ta'izzi-Adeni Arabic (Arabic script)","aeb_Arab": "Tunisian Arabic (Arabic script)","afr_Latn": "Afrikaans","ajp_Arab": "South Levantine Arabic (Arabic script)","aka_Latn": "Akan","amh_Ethi": "Amharic","apc_Arab": "North Levantine Arabic (Arabic script)","arb_Arab": "Standard Arabic (Arabic script)","ars_Arab": "Najdi Arabic (Arabic script)","ary_Arab": "Moroccan Arabic (Arabic script)","arz_Arab": "Egyptian Arabic (Arabic script)","ast_Latn": "Asturian","awa_Deva": "Awadhi (Devanagari script)","ayr_Latn": "Aymara","azb_Arab": "South Azerbaijani (Arabic script)","azj_Latn": "North Azerbaijani (Latin script)","bak_Cyrl": "Bashkir (Cyrillic script)","bam_Latn": "Bambara","ban_Latn": "Balinese","bel_Cyrl": "Belarusian (Cyrillic script)","bem_Latn": "Bemba","ben_Beng": "Bengali","bho_Deva": "Bhojpuri (Devanagari script)","bjn_Arab": "Banjar (Arabic script)","bjn_Latn": "Banjar (Latin script)","bod_Tibt": "Tibetan","bos_Latn": "Bosnian (Latin script)","bug_Latn": "Buginese","bul_Cyrl": "Bulgarian (Cyrillic script)","cat_Latn": "Catalan","ceb_Latn": "Cebuano","cjk_Latn": "Chokwe","ckb_Arab": "Central Kurdish (Arabic script)","crh_Latn": "Crimean Tatar (Latin script)","cym_Latn": "Welsh","dan_Latn": "Danish","deu_Latn": "German","dik_Latn": "Dinka","dyu_Latn": "Dyula","dzo_Tibt": "Dzongkha (Tibetan script)","eng_Latn": "English","epo_Latn": "Esperanto","est_Latn": "Estonian","ewe_Latn": "Ewe","fao_Latn": "Faroese","fij_Latn": "Fijian","fin_Latn": "Finnish","fon_Latn": "Fon","fra_Latn": "French","fur_Latn": "Friulian","fuv_Latn": "Nigerian Fulfulde","gaz_Latn": "West Central Oromo","gla_Latn": "Scottish Gaelic","gle_Latn": "Irish","glg_Latn": "Galician","grn_Latn": "Guarani","guj_Gujr": "Gujarati","hat_Latn": "Haitian Creole","hau_Latn": "Hausa","heb_Hebr": "Hebrew","hin_Deva": "Hindi (Devanagari script)","hne_Deva": "Chhattisgarhi (Devanagari script)","hrv_Latn": "Croatian","hun_Latn": "Hungarian","hye_Armn": "Armenian","ibo_Latn": "Igbo","ilo_Latn": "Ilocano","ind_Latn": "Indonesian","isl_Latn": "Icelandic","ita_Latn": "Italian","jav_Latn": "Javanese","jpn_Jpan": "Japanese (Japanese script)","kab_Latn": "Kabyle","kac_Latn": "Jingpho","kam_Latn": "Kamba","kan_Knda": "Kannada","kas_Arab": "Kashmiri (Arabic script)","kas_Deva": "Kashmiri (Devanagari script)","kat_Geor": "Georgian","knc_Arab": "Central Kanuri (Arabic script)","knc_Latn": "Central Kanuri (Latin script)","kon_Latn": "Kongo","kor_Hang": "Korean (Hangul script)","lao_Laoo": "Lao","lij_Latn": "Ligurian","lim_Latn": "Limburgish","lin_Latn": "Lingala","lit_Latn": "Lithuanian","ltg_Latn": "Latgalian","ltz_Latn": "Luxembourgish","lua_Latn": "Luba-Kasai","lug_Latn": "Ganda","luo_Latn": "Luo","lus_Latn": "Mizo","mag_Deva": "Magahi (Devanagari script)","mai_Deva": "Maithili (Devanagari script)","mal_Mlym": "Malayalam","mar_Deva": "Marathi (Devanagari script)","min_Latn": "Minangkabau","mkd_Cyrl": "Macedonian (Cyrillic script)","mlg_Latn": "Malagasy","mlt_Latn": "Maltese","mni_Beng": "Manipuri (Bengali script)","mos_Latn": "Mossi","mri_Latn": "Maori","mya_Mymr": "Burmese (Myanmar script)","nld_Latn": "Dutch","nno_Latn": "Norwegian Nynorsk","nob_Latn": "Norwegian Bokmål","npi_Deva": "Nepali (Devanagari script)","nso_Latn": "Northern Sotho","nus_Latn": "Nuer","nya_Latn": "Chichewa","oci_Latn": "Occitan","ory_Orya": "Odia","pag_Latn": "Pangasinan","pan_Guru": "Punjabi (Gurmukhi script)","pap_Latn": "Papiamento","pbt_Arab": "Southern Pashto (Arabic script)","plt_Latn": "Plateau Malagasy","pol_Latn": "Polish","por_Latn": "Portuguese","prs_Arab": "Dari (Arabic script)","pus_Arab": "Northern Pashto (Arabic script)","que_Latn": "Quechua","ron_Latn": "Romanian","run_Latn": "Rundi","rus_Cyrl": "Russian (Cyrillic script)","sag_Latn": "Sango","san_Deva": "Sanskrit (Devanagari script)","sat_Beng": "Santali (Bengali script)","scn_Latn": "Sicilian","shn_Mymr": "Shan (Myanmar script)","sin_Sinh": "Sinhala","slk_Latn": "Slovak","slv_Latn": "Slovenian","smo_Latn": "Samoan","sna_Latn": "Shona","snd_Arab": "Sindhi (Arabic script)","som_Latn": "Somali","sot_Latn": "Southern Sotho","spa_Latn": "Spanish","srd_Latn": "Sardinian","srp_Cyrl": "Serbian (Cyrillic script)","ssw_Latn": "Swati","sun_Latn": "Sundanese","swe_Latn": "Swedish","swh_Latn": "Swahili","szl_Latn": "Silesian","tam_Taml": "Tamil","tat_Cyrl": "Tatar (Cyrillic script)","tel_Telu": "Telugu","tgk_Cyrl": "Tajik (Cyrillic script)","tgl_Latn": "Tagalog","tha_Thai": "Thai","tir_Ethi": "Tigrinya (Ethiopic script)","tpi_Latn": "Tok Pisin","tsn_Latn": "Tswana","tso_Latn": "Tsonga","tuk_Latn": "Turkmen","tum_Latn": "Tumbuka","tur_Latn": "Turkish","twi_Latn": "Twi","tzm_Latn": "Central Atlas Tamazight (Latin script)","uig_Arab": "Uyghur (Arabic script)","ukr_Cyrl": "Ukrainian (Cyrillic script)","umb_Latn": "Umbundu","urd_Arab": "Urdu (Arabic script)","uzn_Latn": "Northern Uzbek (Latin script)","vec_Latn": "Venetian","vie_Latn": "Vietnamese","war_Latn": "Waray","wol_Latn": "Wolof","xho_Latn": "Xhosa","ydd_Hebr": "Eastern Yiddish (Hebrew script)","yor_Latn": "Yoruba","yue_Hant": "Cantonese (Traditional Chinese script)","zho_Hans": "Mandarin (Simplified Chinese script)","zho_Hant": "Mandarin (Traditional Chinese script)","zul_Latn": "Zulu"}


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

                # if np.max(np.abs(np.frombuffer(b''.join(frames), dtype=np.int16))) < 1000:
                #     self.stop_recording()

                self.recordings.put(frames.copy())
                frames = []
                i = 0
        
        stream.stop_stream()
        stream.close()
        p.terminate()

    def transcript(self):
        while not self.messages.empty():
            frames = self.recordings.get()

            with wave.open("audio.wav", 'wb') as wf:
                wf.setnchannels(self.CHANNELS)
                wf.setsampwidth(2)
                wf.setframerate(self.FRAME_RATE)
                wf.writeframes(b''.join(frames))

            segments, _ = self.transcription_model.transcribe(f'audio.wav', beam_size=5)
            text = " ".join([segment.text for segment in segments])
            self.full_transcribed_text.append(text)
            self.transcribed_text.put(text)
            print(f"live transcription: ", text)
            os.remove(f"audio.wav")
            
            if keyboard.is_pressed('q'):
                self.stop_recording()

    def translate(self, trnscrpt=""):
        inputs = self.tokenizer(trnscrpt, return_tensors="pt", padding=True, truncation=True).to("cuda")
        inputs = {k: inputs[k].to(self.translation_model.device) for k in inputs}
        outputs = self.translation_model.generate(**inputs, forced_bos_token_id=self.tokenizer.convert_tokens_to_ids(self.output_lang))
        outputs = self.tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]
        self.translated_text.put(outputs)


    def start_recording(self):
        self.messages.put(True)

        print("Start Recording:")
        recording = Thread(target=self.record_microphone)
        recording.start()
        
        transcribing = Thread(target=self.transcript)
        transcribing.start()

        translation = Thread(target=self.translate, args=())
        translation.start()


    def stop_recording(self):
        self.messages.get()
        torch.cuda.empty_cache()
        print("input: ", " ".join(self.full_transcribed_text))
        # print("Translated Text: ", " ".join(self.translated_text))


if __name__ == "__main__":
    a = SpeechToTranslate(input_lang="en", output_lang="hin_Deva")
    a.start_recording()