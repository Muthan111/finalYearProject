from fastapi import HTTPException
import asyncio
import traceback
from src.utils.logger import logger
import librosa
import numpy as np
class ProlongationDetectionService:
    def __init__(self):
        pass

    def detect_prolongation(self,audio, sr):
        """
        Detects prolonged segments in the audio signal based on RMS energy.
        Args:
            audio (np.ndarray): Audio signal.
            sr (int): Sample rate of the audio signal.
        Returns:
            list: A list of times (in seconds) where prolongations occur.
        """
        logger.info(f"[detect_prolongation] Detecting prolongations in audio...")
        try:
            hop_length = 512
            energy_floor = 0.01
            rms = librosa.feature.rms(y=audio, frame_length=2048, hop_length=hop_length).flatten()
            rms_diff = np.abs(np.diff(rms))
            rms_masked = (rms[1:] > energy_floor)
            logger.debug(f"[detect_prolongation] RMS shape: {rms.shape}, RMS diff shape: {rms_diff.shape}")

            threshold = 0.005
            min_frames = int((0.3 * sr) / hop_length)

            prolonged = (rms_diff < threshold) & rms_masked
            logger.debug(f"[detect_prolongation] Any prolonged frames: {np.any(prolonged)}")
            logger.debug(f"[detect_prolongation] Prolonged frame indices: {np.where(prolonged)[0]}")

            count = 0
            starts = []
            for i, val in enumerate(prolonged):
                if val:
                    count += 1
                else:
                    if count >= min_frames:
                        starts.append(i - count)
                        logger.debug(f"[detect_prolongation] Prolongation detected from frame {i - count} to {i}")
                    count = 0
            if count >= min_frames:
                starts.append(len(prolonged) - count)
                logger.debug(f"[detect_prolongation] Prolongation detected at end from frame {len(prolonged) - count}")

            return [librosa.frames_to_time(s, sr=sr, hop_length=hop_length).item() for s in starts]
        except Exception as e:
            logger.error(f"Error in detect_prolongation: {e}")
            logger.error(traceback.format_exc())
            return None