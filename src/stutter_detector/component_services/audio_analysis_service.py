import librosa
import numpy as np
import asyncio
from src.utils.logger import logger
import traceback


class AudioAnalysisService:
    def __init__(self):

        self.n_mfcc = 13

    async def extractMFCC(self, audio_file, sr):
        """
        Extracts MFCC features from the given audio file.
        Args:
            audio_file (str): Path to the audio file.
            sr (int): Sample rate of the audio file.
        Returns:
            dict: A dictionary containing the MFCC features and sample rate.
        """

        def compute_mfcc():
            try:
                logger.info(" [extractMFCC] Extracting MFCC features...")
                mfcc = librosa.feature.mfcc(
                    y=audio_file, sr=sr, n_mfcc=self.n_mfcc
                )
                mfcc_db = (mfcc - np.mean(mfcc)) / (np.std(mfcc) + 1e-6)
                return {"mfcc": mfcc_db, "sr": sr}
            except Exception as e:
                logger.error(
                    f"[extractMFCC] Error in extractMFCC function: {e}"
                )
                logger.error(traceback.format_exc())
                raise Exception("Error in extracting MFCC features")

        return await asyncio.to_thread(compute_mfcc)
