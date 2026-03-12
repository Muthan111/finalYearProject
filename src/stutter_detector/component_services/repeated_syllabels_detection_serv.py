from src.utils.logger import logger
import librosa
from sklearn.metrics.pairwise import cosine_similarity


class RepeatedSyllablesDetectionService:
    def __init__(self):
        self.similarity_threshold = 0.98
        self.min_repetitions = 4
        self.min_time = 0.3

    def detect_repetitions(self, sr, mfcc, frame_hop=512):
        """
        Detects repetitions in the MFCC
        features by comparing non-adjacent frames.
        Args:
            sr (int): Sample rate.
            mfcc (np.ndarray): MFCC array (shape: [n_mfcc, n_frames])
        Returns:
            list of dicts with 'start_time'
            and 'end_time' where repetition likely occurs.
        """
        logger.info(
            "[detect_repetitions] Running improved MFCC repetition detection"
        )
        try:
            frame_delay = 10
            threshold = self.similarity_threshold
            min_repeats = self.min_repetitions
            repeated_times = []
            for i in range(mfcc.shape[1] - frame_delay):
                f1 = mfcc[:, i].reshape(1, -1)
                f2 = mfcc[:, i + frame_delay].reshape(1, -1)
                sim = cosine_similarity(f1, f2)[0][0]
                if sim > threshold:
                    repeated_times.append(
                        librosa.frames_to_time(i, sr=sr, hop_length=frame_hop)
                    )
            # Cluster close detections
            clustered_times = []
            if repeated_times:
                cluster = [repeated_times[0]]
                for t in repeated_times[1:]:
                    if t - cluster[-1] <= 0.3:  # within 300ms
                        cluster.append(t)
                    else:
                        if len(cluster) >= min_repeats:
                            clustered_times.append(
                                {
                                    "start_time": round(cluster[0], 2),
                                    "end_time": round(cluster[-1], 2),
                                }
                            )
                        cluster = [t]
                if len(cluster) >= min_repeats:
                    clustered_times.append(
                        {
                            "start_time": round(cluster[0], 2),
                            "end_time": round(cluster[-1], 2),
                        }
                    )

            logger.info(f"Found {len(clustered_times)} repetition(s)")
            return clustered_times

        except Exception as e:
            logger.error(f"[detect_repetitions] Error: {e}")
            return []
