import librosa
import librosa.display
import noisereduce as nr
import numpy as np
import os
import soundfile as sf
import asyncio
from src.utils.logger import logger
import traceback
from fastapi import HTTPException
class AudioCleanService:
    def __init__(self):
        logger.info("Audio Clean Service initialized.")
        self.pre_emphasis = 0.97
    def save_processed_audio(self, audio, inputename, filepath):
        os.makedirs(filepath, exist_ok=True)  
        audioId = 0
        while True:
            filename = f"{inputename}_{audioId}.wav"
            if not os.path.exists(os.path.join(filepath, filename)):
                break
            audioId += 1
        full_path = os.path.join(filepath, filename)
        sr = 16000  
        sf.write(full_path, audio, sr)
        return {
            "audioId": audioId,
            "filename": filename,
            "filepath": full_path
        }
    async def preprocess_audio(self, file):
        def sync_preprocess(file):
            try: 
                logger.info(f"Processing audio file: {file}")
                audio, sr = librosa.load(file, sr=16000)
                pre_emphasis = self.pre_emphasis
                pre_emp_audio = np.append(audio[0], audio[1:] - pre_emphasis * audio[:-1])
                reduced_noise = nr.reduce_noise(y=pre_emp_audio, sr=sr)
                processedAudio = self.save_processed_audio(reduced_noise, "processedAudio", "processed_audio_directory")
                logger.info("Audio cleaning completed successfully.")
                return {
                "duration_seconds": len(reduced_noise) / sr,
                "sr": sr,
                "cleanedAudio": reduced_noise,
                "processedAudio": processedAudio 

                }
                
            except Exception as e:
                logger.error(f"Audio cleaning failed: {e}")
                logger.error(traceback.format_exc())
                raise HTTPException(status_code=500, detail="Audio cleaning failed")
        result = await asyncio.to_thread(sync_preprocess, file)
        return result
    
    