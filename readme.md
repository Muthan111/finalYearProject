# setting up venv
py -3.10 -m venv myenv
# Activate the Scripts
myenv/Scripts/Activate  

# Install the required packages
pip install -r requirements.txt

# Start the server
uvicorn src.main:app --reload

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

## 🚀 **API Endpoint**

**POST** `/stutter_detection`

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