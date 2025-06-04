import librosa
import librosa.display
import noisereduce as nr
import numpy as np
import os
import soundfile as sf
import asyncio
class AudioCleanService:
    def __init__(self):
        pass
    
    async def preprocess_audio(self, file):
        def sync_preprocess(file):
            audio, sr = librosa.load(file, sr=16000)
            pre_emphasis = 0.97
            pre_emp_audio = np.append(audio[0], audio[1:] - pre_emphasis * audio[:-1])
            reduced_noise = nr.reduce_noise(y=pre_emp_audio, sr=sr)
            return {
            "duration_seconds": len(reduced_noise) / sr,
            "sr": sr,
            "cleanedAudio": reduced_noise  # Preview only
            }
        print("Audio processing module loaded successfully.")
        result = await asyncio.to_thread(sync_preprocess, file)
        print("Audio processing module loaded successfully.")
        return result
    
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