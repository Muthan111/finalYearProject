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

    # def detect_repetitions (self,sr, mfcc):
    #     """
    #     Detects repetitions in the MFCC features of an audio signal.
    #     Args:
    #         sr (int): Sample rate of the audio signal.
    #         mfcc (np.ndarray): MFCC features of the audio signal.
    #     Returns:
    #         list: A list of times (in seconds) where repetitions occur.
    #     """
    #     logger.info(f"[detect_repetitions] Detecting repetitions in MFCC features")
    #     try:
    #         repeat_indices = []
    #         for i in range(mfcc.shape[1] - 1):
    #             sim = cosine_similarity(mfcc[:, i].reshape(1, -1), mfcc[:, i+1].reshape(1, -1))[0][0]
    #             if sim > self.similarity_threshold:
    #                 repeat_indices.append(i)
    #         clustered = []
    #         cluster = []
    #         for idx in repeat_indices:
    #             if not cluster or idx == cluster[-1] + 1:
    #                 cluster.append(idx)
    #         else:
    #             if len(cluster) >= self.min_repetitions:
    #                 clustered.append(cluster)
    #             cluster = [idx]
    #         if len(cluster) >= self.min_repetitions:
    #             clustered.append(cluster)

    #         times = [librosa.frames_to_time(c[0], sr=sr, hop_length=512).item() for c in clustered]
    #         filtered_times = [t for t in times if t >= self.min_time]
    #         logger.info(f"[DetectorService] detection of repetitions completed")
    #         return filtered_times
    #     except Exception as e:
    #         logger.error(f"[DetectorService] Error in detect_repetitions: {e}")
    #         logger.error(traceback.format_exc())
    #         raise HTTPException(status_code=500, detail="Error in detecting repetitions")
    def detect_repetitions(self, sr, mfcc, frame_hop=512):
        """
        Detects repetitions in the MFCC features by comparing non-adjacent frames.
        Args:
            sr (int): Sample rate.
            mfcc (np.ndarray): MFCC array (shape: [n_mfcc, n_frames])
        Returns:
            list of timestamps (float) where repetition likely occurs.
        """
        

        logger.info("[detect_repetitions] Running improved MFCC repetition detection")

        try:
            frame_delay = 10  # compare frame i with i+10 (~230ms at 512 hop)
            threshold = self.similarity_threshold  # e.g., 0.95
            min_repeats = self.min_repetitions      # e.g., 3

            repeated_times = []
            similarity_scores = []

            for i in range(mfcc.shape[1] - frame_delay):
                f1 = mfcc[:, i].reshape(1, -1)
                f2 = mfcc[:, i + frame_delay].reshape(1, -1)
                sim = cosine_similarity(f1, f2)[0][0]
                similarity_scores.append(sim)
                if sim > threshold:
                    repeated_times.append(librosa.frames_to_time(i, sr=sr, hop_length=frame_hop))

            # Cluster close detections
            clustered_times = []
            if repeated_times:
                cluster = [repeated_times[0]]
                for t in repeated_times[1:]:
                    if t - cluster[-1] <= 0.3:  # within 300ms
                        cluster.append(t)
                    else:
                        if len(cluster) >= min_repeats:
                            clustered_times.append(round(cluster[0], 2))
                        cluster = [t]
                if len(cluster) >= min_repeats:
                    clustered_times.append(round(cluster[0], 2))

            logger.info(f"[detect_repetitions] Found {len(clustered_times)} repetition(s)")
            return clustered_times

        except Exception as e:
            logger.error(f"[detect_repetitions] Error: {e}")
            raise HTTPException(status_code=500, detail="Error detecting repetitions")
