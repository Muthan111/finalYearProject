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
        
        self.pre_emphasis = 0.97


    def save_processed_audio(self, audio, input_name, file_path):
        """
        Saves the processed audio to a specified directory with a unique filename.
        Args:
            audio (np.ndarray): The processed audio data.
            input_name (str): The base name for the audio file.
            file_path (str): The directory where the audio file will be saved.
        Returns:
            dict: A dictionary containing the audio ID, filename, and full path of the saved audio
        """
        os.makedirs(file_path, exist_ok=True)  
        audio_Id = 0
        while True:
            file_name = f"{input_name}_{audio_Id}.wav"
            if not os.path.exists(os.path.join(file_path, file_name)):
                break
            audio_Id += 1
        full_path = os.path.join(file_path, file_name)
        sr = 16000  
        sf.write(full_path, audio, sr)
        return {
            "audioId": audio_Id,
            "filename": file_name,
            "filepath": full_path
        }
    async def preprocess_audio(self, file):
        """
        Cleans the audio file by applying pre-emphasis and noise reduction.
        Args:
            file (str): Path to the audio file.
        Returns:
            dict: A dictionary containing the duration in seconds, sample rate, cleaned audio, and processed
            audio file information.
        """
        def sync_preprocess(file):
            try: 
                logger.info(f"[preprocess_audio] Processing audio file: {file}")
                  # 1️⃣  Basic file‑level sanity check (empty or unreadable file)
                if not os.path.exists(file) or os.path.getsize(file) == 0:
                    logger.warning(f"[preprocess_audio] File {file} is empty or missing.")
                    return {
                        "error": "Audio file is empty or missing.",
                        "cleanedAudio": None,
                        "processedAudio": None,
                    }
                else:
                    audio, sr = librosa.load(file, sr=16000)
                    pre_emphasis = self.pre_emphasis
                    pre_emp_audio = np.append(audio[0], audio[1:] - pre_emphasis * audio[:-1])
                    reduced_noise = nr.reduce_noise(y=pre_emp_audio, sr=sr)
                    processed_audio = self.save_processed_audio(reduced_noise, "processedAudio", "processed_audio_directory")
                    logger.info(f"[preprocess_audio] Audio cleaning completed successfully.")
                    return {
                    "duration_seconds": len(reduced_noise) / sr,
                    "sr": sr,
                    "cleanedAudio": reduced_noise,
                    "processedAudio": processed_audio 

                    }
                
            except Exception as e:
                logger.error(f"[preprocess_audio] Audio cleaning failed. preprocess_audio function has error: {e}")
                logger.error(traceback.format_exc())
                raise HTTPException(status_code=500, detail="Audio cleaning failed")
        result = await asyncio.to_thread(sync_preprocess, file)
        return result
    
    