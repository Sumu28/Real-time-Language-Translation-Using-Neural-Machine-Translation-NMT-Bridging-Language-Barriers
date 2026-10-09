# Speak Once, Translate Everywhere

**A small Flask web app that listens to you speak and gives you the translation in several languages at once.**

Say a sentence in English (or another supported language) and the app writes down what you said, then translates it into Spanish, French, Hindi, Kannada, Tamil and Telugu by default. You can also turn any translation into an audio file to download.

It started from a simple idea: language should not get in the way of a conversation, so what would it take to go from *spoken words* to *translated text and speech* in one step?

> Built as my own personal project during my IBM internship on *Real-Time Language Translation Using Neural Machine Translation* (February–April 2025), as a hands-on demo of speech-to-translation.

---

## How it works

1. **Listen.** The app opens the microphone, adjusts for background noise, and records until you stop talking.
2. **Transcribe.** The audio is sent to Google's speech recognition (through the `SpeechRecognition` library) and comes back as text.
3. **Translate.** The text is translated into each target language using Google Translate (through the `deep-translator` library).
4. **Speak.** If you ask for audio, the translated text is turned into speech with `pyttsx3` and sent back as a file.

**The translation itself comes from Google's services. This project is the app that connects them together.** It does not train or host its own translation model.

## The API

| Route | Method | What it does |
|---|---|---|
| `/` | GET | Serves the web page |
| `/translate` | POST | Listens, transcribes and translates |
| `/download-audio` | POST | Returns spoken audio for a piece of text |

**Example request to `/translate`:**

```json
{
  "source_lang": "en",
  "target_langs": ["es", "fr", "hi"]
}
```

If you leave out the languages, it uses English as the source and translates into `es`, `fr`, `hi`, `kn`, `ta` and `te`.

**Example response:**

```json
{
  "original": "Good morning",
  "translations": {
    "es": "Buenos días",
    "fr": "Bonjour",
    "hi": "सुप्रभात"
  }
}
```

*(Replace this with a real response from your own run.)*

**Request to `/download-audio`:** send `{"text": "...", "lang": "es"}` and you get an audio file back. If `text` is empty, it returns a 400 error.

*(Add screenshots of the page here.)*

---

## Tech stack

Python · Flask · SpeechRecognition · PyAudio · pyttsx3 · deep-translator · HTML (`templates/index.html`)

## Run it yourself

You will need Python 3, a working microphone and an internet connection.

```bash
git clone https://github.com/Sumu28/<your-repo-name>.git
cd <your-repo-name>
python -m venv venv
source venv/bin/activate        # on Windows: venv\Scripts\activate
pip install flask SpeechRecognition pyttsx3 deep-translator pyaudio
python app.py
```

Then open `http://127.0.0.1:5000` in your browser.

**If PyAudio won't install:** on macOS run `brew install portaudio` first. On Linux install `portaudio19-dev`. On Windows, use a pre-built wheel. *(Add a `requirements.txt` to the repo.)*

---

## Things to know

- **It only works when run on your own computer.** The app records from the microphone of the machine running Flask, not from the visitor's browser. If you host it online, it will try to find a microphone on the server. A deployable version needs to capture audio in the browser and upload it.
- **It waits for you indefinitely.** There is no time limit on listening, so a request can hang if nobody speaks.
- **Errors get translated.** If speech isn't understood, the message "Could not understand the audio." is returned as if it were your speech and gets translated into every language.
- **The audio ignores the language.** The text-to-speech part uses whatever voice is installed on your system. The `lang` value is accepted but not used, so Hindi, Kannada, Tamil or Telugu text may be read in an English voice or not at all.
- **The file is called `.mp3`, but it may not be one.** `pyttsx3` often saves WAV audio, whichever extension you give it. The server also speaks the text aloud as it saves.
- **It depends on online services.** Speech recognition and translation both go through Google's free services, so you need internet, your audio leaves your machine, and the free endpoints can be rate-limited or change without warning.
- **Language codes must work for both services.** The same code is used for speech recognition and translation, so some codes (such as `zh-CN` or regional forms) may need separate handling.
- **Debug mode is on.** Fine for development, but turn off `debug=True` before putting it anywhere public.

## What I would improve next

- Record audio in the browser and send it to the server, so it works for anyone
- Add a timeout and return proper error codes instead of error text
- Use a text-to-speech service that supports Indian languages properly
- Add a language picker to the page, and show results as they arrive
- Add tests and a `requirements.txt`

## Author

Sumukha Sagar
Built alongside my IBM project internship, Bengaluru, 2025.
