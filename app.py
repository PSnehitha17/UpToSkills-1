from flask import Flask, render_template, request, jsonify, send_from_directory
from gtts import gTTS
import os
import hashlib
import re

app = Flask(__name__)

CACHE_FOLDER = "cache"

# Create cache folder if not exists
if not os.path.exists(CACHE_FOLDER):
    os.makedirs(CACHE_FOLDER)


# Home Page
@app.route("/")
def home():
    return render_template("index.html")


# Serve Audio Files
@app.route("/cache/<filename>")
def serve_audio(filename):
    return send_from_directory(CACHE_FOLDER, filename)


# Generate Audio
@app.route("/generate", methods=["POST"])
def generate_audio():

    text = request.json["text"]

    # -----------------------------
    # TEXT NORMALIZATION
    # -----------------------------

    # Convert to lowercase
    text = text.lower()

    # Remove leading/trailing spaces
    text = text.strip()

    # Remove extra spaces/new lines
    text = " ".join(text.split())

    # Normalize repeated characters
    # hiiiiii -> hii
    text = re.sub(r'(.)\1{2,}', r'\1\1', text)

    # Remove punctuation
    text = re.sub(r'[^\w\s]', '', text)

    # -----------------------------
    # CREATE HASH
    # -----------------------------

    file_hash = hashlib.md5(text.encode()).hexdigest()

    filename = f"{file_hash}.mp3"

    filepath = os.path.join(CACHE_FOLDER, filename)

    # -----------------------------
    # CACHE CHECK
    # -----------------------------

    if os.path.exists(filepath):

        status = "Loaded from Cache ⚡"

    else:

        tts = gTTS(text=text, lang='en')

        tts.save(filepath)

        status = "Generated New Audio 🎤"

    return jsonify({
        "audio": filename,
        "status": status,
        "normalized_text": text
    })


# -----------------------------
# CLEAR CACHE
# -----------------------------

@app.route("/clear-cache", methods=["POST"])
def clear_cache():

    for file in os.listdir(CACHE_FOLDER):

        file_path = os.path.join(CACHE_FOLDER, file)

        if os.path.isfile(file_path):
            os.remove(file_path)

    return jsonify({
        "message": "Cache Cleared Successfully 🗑️"
    })


if __name__ == "__main__":
    app.run(debug=True)