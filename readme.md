## Cloning Instructions:

git clone <link goes here>
cd <repo-folder>

## installation Instructions


# Activate the Scripts (This is for windows)
py -3.10 -m venv myenv
myenv\Scripts\activate  

# Activate the Scripts (This is for macOS/Linux )
python3.10 -m venv myenv
source myenv/bin/activate

# Install the required packages
pip install -r requirements.txt
🧠 Note: This project uses faster-whisper for faster, lower-latency transcription.
You must install ffmpeg separately for audio processing.
🧠 Note: This project uses faster-whisper for faster, lower-latency transcription.
It’s a CTranslate2-based implementation of OpenAI Whisper and runs locally, without needing an API key.
📦 GitHub: https://github.com/guillaumekln/faster-whisper

## Install ffmpeg
# Windows (using Chocolatey)
choco install ffmpeg

# macOS (using Homebrew)
brew install ffmpeg

# Ubuntu/Debian
sudo apt install ffmpeg


# Start the server
python run_server.py

# 🎙️ Stutter Detection Pipeline

## 📌 Overview

This project implements an **end-to-end stutter detection pipeline** for speech recordings.  
It combines **audio recording**, **noise cleaning**, **automatic transcription** using OpenAI's Whisper model, and **custom rule-based stutter detection logic** (repetitions, prolongations, blocks, fillers, and repeated words).

This project is built using **FastAPI** for the backend API and can be integrated with any frontend for real-time or batch processing.

---

## ⚙️ Pipeline Steps

The pipeline runs the following steps **in sequence**:

1️⃣ **Audio Recording**  
- Uses the device microphone to record user speech.
- Handles retries in case of microphone failures.

2️⃣ **Audio Cleaning**  
- Pre-processes raw audio to reduce noise and prepare for feature extraction.
- Ensures a clean input for the ASR and feature detectors.

3️⃣ **Audio Transcription**  
- Uses the Whisper AI model to transcribe the spoken content into text.
- Retries transcription once if a transient error occurs.

4️⃣ **Feature Extraction**  
- Extracts MFCC (Mel Frequency Cepstral Coefficients) features for signal analysis.

5️⃣ **Stutter Detection**  
- Detects various disfluencies using custom logic:
  - **Repetitions**
  - **Prolongations**
  - **Blocks**
  - **Fillers**
  - **Repeated Words**

6️⃣ **Partial Results and Fallbacks**  
- If any step fails, the pipeline returns all available data instead of failing completely.
- Full stack traces are logged for debugging.

---
## API docs
http://127.0.0.1:8000/docs
The above link will take you to all the APIs


## 🚀 **API Endpoint**

**POST** `http://127.0.0.1:8000/stutter_detection`

**Description:**  
Triggers the complete stutter detection pipeline:
- Starts recording
- Cleans the audio
- Transcribes it
- Analyzes it
- Returns detected disfluencies and the transcription.

**Response JSON Example:**
```json
{
  "repetitions": [ ... ],
  "blocks": [ ... ],
  "prolongations": [ ... ],
  "transcription": "Your transcribed text here",
  "fillers": [ ... ],
  "repeated_words": [ ... ]
}
```
## Author
Muhammad Muad Thaha
muadthaha@gmail.com

## Output files
# Audio files
Audio files will be saved in uploaded_files
Format: wav
# Logs
logs will be stored under logs

## 📜 License

This project is licensed under the MIT License.

It includes the use of [faster-whisper](https://github.com/guillaumekln/faster-whisper) by Guillaume Klein, which is also licensed under MIT.

---

## 📁 Data Sources

### 📊 SEP‑28k (Stuttering Events in Podcasts)
- **Dataset by:** Colin Lea, Vikramjit Mitra, Aparna Joshi, Sachin Kajarekar, Jeffrey Bigham  
- **License:** Creative Commons Attribution‑NonCommercial 4.0 (CC BY‑NC 4.0)  
- **Source:** [SEP‑28k on Kaggle](https://www.kaggle.com/datasets/ikrbasak/sep-28k)

> ⚠️ Used for **testing and academic evaluation only**. Not for commercial use.
