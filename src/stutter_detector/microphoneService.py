import pyaudio
import wave
import os
import asyncio
import logging
from fastapi import HTTPException
from src.utils.logger import logger
import traceback
class MicrophoneService:
    def __init__(self):
        logger.info("Microphone Service initialized.")
        self.result = None
        self.language = "en"
        self.sample_rate = 16000
        self.chunk_size = 1024
        self.channels  = 1
        self.format = pyaudio.paInt16
        self.frames = []
        self.clip_duration = 20  
    

    async def start_recording(self):
        logger.info("Starting audio recording...")
        audio_displayURL = "http://127.0.0.1:8000/static"
        max_retries = 2
        for attempt in range(max_retries):
            try:
                self.p = pyaudio.PyAudio()
                self.stream = self.p.open(format=self.format,
                                   channels=self.channels,
                                   rate=self.sample_rate,
                                   input=True,
                                   frames_per_buffer=self.chunk_size)
        
                self.frames = []
                for _ in range(0, int(self.sample_rate / self.chunk_size * self.clip_duration)):
                    data = self.stream.read(self.chunk_size)
                    self.frames.append(data)
                self.stream.stop_stream()
                self.stream.close()
                self.p.terminate()
                if len(self.frames) == 0:
                    print("No audio data captured. Please check your microphone settings.")
                else:
                    file_path = "recordings"
                    audio_Saved = self.save_audio(self.frames, "recording", file_path)
                    audio_filename = audio_Saved["filename"]
                    audio_filepath = audio_Saved["filepath"]
                    website_audio = os.path.join(audio_displayURL, audio_filename)
                    logger.info("Audio recording completed successfully.")
                    return {
                    "audiofile": audio_filename,
                    "audiofilepath": audio_filepath,
                    "audioDisplayURL": website_audio,
                    
                
                }
            except Exception as e:
                if attempt < max_retries - 1:
                    logger.info(f"Retrying recording in 5 seconds...")
                    await asyncio.sleep(5) 
                else:
                    logger.error(f"Error in recording audio: {e}")
                    logger.error(traceback.format_exc())
                    raise HTTPException(status_code=500, detail="Error in recording audio function")
                
    
    def save_audio(self,frames, input_name, file_path):
        os.makedirs(file_path, exist_ok=True)  
        audio_Id = 0
        while True:
            file_name = f"{input_name}_{audio_Id}.wav"
            if not os.path.exists(os.path.join(file_path, file_name)):
                break
            audio_Id += 1
        full_path = os.path.join(file_path, file_name)
        with wave.open(full_path, 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.p.get_sample_size(self.format))
            wf.setframerate(self.sample_rate)
            wf.writeframes(b''.join(frames))
        return {
        "audioId": audio_Id,
        "filename": file_name,
        "filepath": full_path
        }