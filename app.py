from flask import Flask, render_template, request, jsonify, send_file
import speech_recognition as sr
import pyttsx3
from deep_translator import GoogleTranslator
import os

app = Flask(__name__)

def recognize_speech(source_lang="en"):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print(f"Listening for {source_lang}...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio, language=source_lang)
            return text
        except sr.UnknownValueError:
            return "Could not understand the audio."
        except sr.RequestError:
            return "Error connecting to speech recognition service."

def text_to_speech(text, lang_code, filename="output.mp3"):
    tts = pyttsx3.init()
    tts.setProperty('rate', 150)  # Speed of speech
    tts.say(text)
    tts.save_to_file(text, filename)
    tts.runAndWait()
    return filename

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    data = request.json
    source_lang = data.get("source_lang", "en")
    target_langs = data.get("target_langs", ["es", "fr", "hi", "kn", "ta", "te"])
    
    text = recognize_speech(source_lang)
    translations = {}

    for target_lang in target_langs:
        translated_text = GoogleTranslator(source=source_lang, target=target_lang).translate(text)
        translations[target_lang] = translated_text
    
    return jsonify({"original": text, "translations": translations})

@app.route('/download-audio', methods=['POST'])
def download_audio():
    data = request.json
    text = data.get("text", "")
    lang_code = data.get("lang", "en")

    if not text:
        return jsonify({"error": "No text provided"}), 400

    filename = "translation.mp3"
    text_to_speech(text, lang_code, filename)
    
    return send_file(filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)

