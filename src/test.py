import whisper

# Load the base model (or 'small', 'medium', 'large' for better accuracy)
model = whisper.load_model("large")

# Load audio file with Indian accent
result = model.transcribe("C:/Users/admin/Desktop/FYP/implementation/finalYearProject/src/test3.mp3", language="en")

# Print the text
print("Transcription:", result["text"])
# import whisper
# import os
# import time
# import pyaudioop as audioop
# import pydub
# from pydub import AudioSegment
# model = whisper.load_model("base")

# def transcribe_in_chunks(file_path, chunk_duration=5):
    
#     audio = AudioSegment.from_file(file_path)
#     total_ms = len(audio)

#     for i in range(0, total_ms, chunk_duration * 1000):
#         chunk = audio[i:i + chunk_duration * 1000]
#         chunk_path = f"chunk_{i}.mp3"
#         chunk.export(chunk_path, format="mp3")
#         result = model.transcribe(chunk_path, language="en")
#         print(f"[{i//1000}-{(i + chunk_duration * 1000)//1000}s]:", result["text"])
#         os.remove(chunk_path)
#         time.sleep(1)  # simulate delay

# # Example use
# transcribe_in_chunks("C:/Users/admin/Desktop/FYP/implementation/finalYearProject/src/test2.mp3")
