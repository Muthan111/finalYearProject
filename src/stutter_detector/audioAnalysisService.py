import librosa
import numpy as np
import asyncio
from src.utils.logger import logger
import traceback
class AudioAnalysisService:
    def __init__(self):
        logger.info("Audio Analysis Service initialized.")
        self.n_mfcc = 13
        

    async def extractMFCC(self, audio_file, sr):
        def compute_mfcc():
            try:
                logger.info("Extracting MFCC features...")
                mfcc = librosa.feature.mfcc(y=audio_file, sr=sr, n_mfcc=self.n_mfcc)
                mfcc_db = (mfcc - np.mean(mfcc)) / (np.std(mfcc) + 1e-6)
                return {
                    "mfcc": mfcc_db,
                    "sr": sr
                }
            except Exception as e:
                logger.error(f"Error in extractMFCC: {e}")
                logger.error(traceback.format_exc())
                raise Exception("Error in extracting MFCC features")
        return await asyncio.to_thread(compute_mfcc)
    
    

   