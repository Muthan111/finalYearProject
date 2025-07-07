from fastapi import HTTPException
import asyncio
import traceback
from src.utils.logger import logger
import librosa
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
class RepeatedSyllablesDetectionService:
    def __init__(self):
        self.similarity_threshold = 0.98
        self.min_repetitions = 4
        self.min_time = 0.3

    def detect_repetitions (self,sr, mfcc):
        """
        Detects repetitions in the MFCC features of an audio signal.
        Args:
            sr (int): Sample rate of the audio signal.
            mfcc (np.ndarray): MFCC features of the audio signal.
        Returns:
            list: A list of times (in seconds) where repetitions occur.
        """
        logger.info(f"[detect_repetitions] Detecting repetitions in MFCC features")
        try:
            repeat_indices = []
            for i in range(mfcc.shape[1] - 1):
                sim = cosine_similarity(mfcc[:, i].reshape(1, -1), mfcc[:, i+1].reshape(1, -1))[0][0]
                if sim > self.similarity_threshold:
                    repeat_indices.append(i)
            clustered = []
            cluster = []
            for idx in repeat_indices:
                if not cluster or idx == cluster[-1] + 1:
                    cluster.append(idx)
            else:
                if len(cluster) >= self.min_repetitions:
                    clustered.append(cluster)
                cluster = [idx]
            if len(cluster) >= self.min_repetitions:
                clustered.append(cluster)

            times = [librosa.frames_to_time(c[0], sr=sr, hop_length=512).item() for c in clustered]
            filtered_times = [t for t in times if t >= self.min_time]
            logger.info(f"[DetectorService] detection of repetitions completed")
            return filtered_times
        except Exception as e:
            logger.error(f"[DetectorService] Error in detect_repetitions: {e}")
            logger.error(traceback.format_exc())
            raise HTTPException(status_code=500, detail="Error in detecting repetitions")