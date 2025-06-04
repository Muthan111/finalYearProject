# ===================
# Machine Learning Pipeline for Audio Processing
# ===================


# ===================
# Import Libraries
# ===================
import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import seaborn as sns
from glob import glob
import noisereduce as nr
import librosa
import librosa.display
import IPython.display as ipd
import pyaudio
import wave
import os
import soundfile as sf
from sklearn.metrics.pairwise import cosine_similarity
import re
import whisper
# ===================
# Helper function to generate a unique filename for the audio recording
# ===================



    
def save_audio(frames, inputename, filepath):
    os.makedirs(filepath, exist_ok=True)  # Ensure the directory exists
    audioId = 0
    while True:
        filename = f"{inputename}_{audioId}.wav"
        if not os.path.exists(os.path.join(filepath, filename)):
            break
        audioId += 1
    full_path = os.path.join(filepath, filename)
    with wave.open(full_path, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(pyaudio.PyAudio().get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
    return {
        "audioId": audioId,
        "filename": filename,
        "filepath": full_path
    }

def save_processed_audio(audio, inputename, filepath):
    os.makedirs(filepath, exist_ok=True)  # Ensure the directory exists
    audioId = 0
    while True:
        filename = f"{inputename}_{audioId}.wav"
        if not os.path.exists(os.path.join(filepath, filename)):
            break
        audioId += 1
    full_path = os.path.join(filepath, filename)
    # librosa.output.write_wav(full_path, audio, sr=16000)
    sr = 16000  # Define the sample rate
    sf.write(full_path, audio, sr)
    return {
        "audioId": audioId,
        "filename": filename,
        "filepath": full_path
    }

def save_transcription(text, filepath="../transcriptions"):
    os.makedirs(filepath, exist_ok=True)  # Ensure the directory exists
    counter = 0
    while True:
        filename = f"transcription_{counter}.txt"
        if not os.path.exists(os.path.join(filepath, filename)):
            break
        counter += 1
    fullpath = os.path.join(filepath, filename)
    with open(fullpath, "w", encoding="utf-8") as f:
        f.write(text)
# ===================
# Configurable parameters
# ===================
CHUNK= 1024  # Number of audio samples per frame
FORMAT = pyaudio.paInt16  # Audio format (16-bit PCM)
RATE = 44100  # Sample rate (samples per second)
CHANNELS = 2  # Number of audio channels (1 for mono, 2 for stereo)

# ===================
# Function to record audio from the microphone
# ===================
def microphone():
    recording = pyaudio.PyAudio()
    stream = recording.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    print("🎙️ Recording started...")
    frames = []
    seconds = 10  # Duration of the recording in seconds

    for i in range(0, int(RATE / CHUNK * seconds)):
        data = stream.read(CHUNK)
        frames.append(data)
    print("🎙️ Recording finished.")
    stream.stop_stream()
    stream.close()
    recording.terminate()
    
    filepath = "../recordings"
    audioSaved = save_audio(frames,"audiofile" ,filepath)
    audiofilename = audioSaved["filename"]
    audiofilepath = audioSaved["filepath"]
    return {
        "audiofile": audiofilename,
        "audiofilepath": audiofilepath,
    }
  # Return the filename of the saved audio


# ===================
# Audio Preprocessing
# ===================
def displayAudioGraph(audio):
  plt.figure(figsize=(12, 4))
  librosa.display.waveshow(audio, sr=16000)
  plt.show()



def preprocess_audio(file):
    # Load audio
  audio, sr = librosa.load(file, sr=16000)

  
  # Pre-emphasis
  pre_emphasis = 0.97
  pre_emp_audio = np.append(audio[0], audio[1:] - pre_emphasis * audio[:-1])

  # Reduce noise
  frames = []
  reduced_noise = nr.reduce_noise(y=pre_emp_audio, sr=sr)
  save_processed_audio(reduced_noise, "processed_audio", "../processed_recordings")

  # display reduced audio
  # displayAudioGraph(reduced_noise)
  print("Audio processing module loaded successfully.")
  return{
       "audio": reduced_noise,
       "sr": sr
   }

# ===================
# Audio processing
# ===================    
def extractMFCC(audio,sr, n_mfcc=13):
  # Compute MFCC
  mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=n_mfcc)

  # Normalize and log-scale carefully
  mfcc_db = (mfcc - np.mean(mfcc)) / (np.std(mfcc) + 1e-6) 
#   # Plot
#   plt.figure(figsize=(10, 4))
#   librosa.display.specshow(mfcc_db, x_axis='time')
#   plt.colorbar(format='%+2.0f dB')
#   plt.title("MFCC (Log Scaled, Pre-emphasized)")
#   plt.tight_layout()
#   plt.show()

  return {
    "mfcc": mfcc,
    "mfcc_db": mfcc_db,
    "sr": sr
  }


# ===================
# detect stutters
# =================== 
def transcribe(file_path):
  model = whisper.load_model("medium")
  result = model.transcribe(file_path,initial_prompt="uh um like you know so", language="en",word_timestamps=True)
  text = result['text']
  save_transcription(text, "../transcriptions")
  print("📝 Transcription completed.")

  print(text)
  return text

def repeatedWords(transcript):
  repeated_words = re.findall(r'\b(\w+)(?:[ -]+\1\b)+', transcript.lower())
  return repeated_words

def fillers(transcript):
  fillers = re.findall(r'\b(um+|uh+|er+|ah+)\b', transcript.lower())
  return fillers

def detect_repetition(audio, sr, mfcc, sim_thresh=0.98, min_repeats=4, min_time=0.3):
    """
    Detect repetition in audio based on cosine similarity of MFCC frames.
    
    Parameters:
    - audio: np.array of audio signal
    - sr: sample rate
    - mfcc: MFCC features (n_mfcc x time_frames)
    - sim_thresh: similarity threshold to consider as repetition
    - min_repeats: minimum number of consecutive similar frames to consider repetition
    - min_time: ignore detections before this time (in seconds)

    Returns:
    - list of repetition start times (in seconds)
    """
    print("🔍 Running repetition detection...")
    
    # Calculate frame-wise cosine similarity
    repeat_indices = []
    for i in range(mfcc.shape[1] - 1):
        sim = cosine_similarity(mfcc[:, i].reshape(1, -1), mfcc[:, i+1].reshape(1, -1))[0][0]
        if sim > sim_thresh:
            repeat_indices.append(i)

    print(f"🧠 Similar frame pairs: {repeat_indices}")
    
    # Cluster repeated frames
    clustered = []
    cluster = []
    for idx in repeat_indices:
        if not cluster or idx == cluster[-1] + 1:
            cluster.append(idx)
        else:
            if len(cluster) >= min_repeats:
                clustered.append(cluster)
            cluster = [idx]
    if len(cluster) >= min_repeats:
        clustered.append(cluster)

    print(f"🗂️ Clustered repeats: {clustered}")
    
    # Convert to timestamps and filter out too-early detections
    times = [librosa.frames_to_time(c[0], sr=sr, hop_length=512).item() for c in clustered]
    filtered_times = [t for t in times if t >= min_time]

    print(f"⏱️ Repetition timestamps (filtered): {filtered_times}")
    return filtered_times

def detect_prolongation(audio, sr, energy_thresh=2.0, min_duration=0.5):
    spec = librosa.feature.melspectrogram(y=audio, sr=sr)
    db_spec = librosa.power_to_db(spec, ref=np.max)

    energy_diff = np.abs(np.diff(db_spec, axis=1)).mean(axis=0)
    prolonged_frames = energy_diff < energy_thresh

    # Find contiguous frame sequences
    count = 0
    starts = []
    for i, val in enumerate(prolonged_frames):
        if val:
            count += 1
        else:
            if count >= (min_duration * sr / 512):
                starts.append(i - count)
            count = 0
    return [librosa.frames_to_time(s, sr=sr).item() for s in starts]

def detect_block(audio, sr, silence_thresh=0.01, block_thresh=1.0):
    energy = librosa.feature.rms(y=audio)[0]
    smoothed_energy = np.convolve(energy, np.ones(5)/5, mode='same')
    silent = smoothed_energy < silence_thresh

    first_speech = np.argmax(~silent)
    start_time = librosa.frames_to_time(first_speech, sr=sr)

    if start_time > block_thresh:
        return [start_time]
    return []

# ===================
# Execution function
# =================== 

def execute_pipeline():
    # start recording
    recording = microphone()
    print(f"Audio recorded and saved as {recording['audiofilepath']}")
    raw_audio = recording["audiofilepath"]
    cleaned_audio = preprocess_audio(raw_audio)
    mfcc_features = extractMFCC(cleaned_audio["audio"], cleaned_audio["sr"])
    reptitions = detect_repetition(cleaned_audio["audio"],cleaned_audio["sr"],mfcc_features["mfcc_db"])
    text = transcribe(raw_audio)
    repeated_words = repeatedWords(text)
    # fillers = fillers(text)
    fillerwords = fillers(text)
    prolongnations = detect_prolongation(cleaned_audio["audio"], cleaned_audio["sr"])
    blocks = detect_block(cleaned_audio["audio"], cleaned_audio["sr"])
    return {
        
        "repetitions": reptitions,
        "Repeated Words" : repeated_words,
        "Fillers" : fillerwords,
        "Transcription": text,
        "Prolongations": prolongnations,
        "Blocks": blocks
        # "Fillers": fillers
    }

test1 = execute_pipeline()
print("Detected repetitions at times (in seconds):", test1["repetitions"])
print("Repeated words detected:", test1["Repeated Words"])
print("Fillers detected:", test1["Fillers"])
print("Transcription:", test1["Transcription"])
print("Prolongations detected at times (in seconds):", test1["Prolongations"])
print("Blocks detected at times (in seconds):", test1["Blocks"])
