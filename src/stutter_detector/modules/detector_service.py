from fastapi import HTTPException
import asyncio
import traceback
from src.utils.logger import logger
from sklearn.metrics.pairwise import cosine_similarity
import librosa
import numpy as np
import re
from src.stutter_detector.modules.block_detection_module import BlockDetectionService
from src.stutter_detector.modules.prolongation_detection_module import ProlongationDetectionService
from src.stutter_detector.modules.repeated_syllabels_detection_module import RepeatedSyllablesDetectionService
from src.stutter_detector.modules.filller_detection_module import FillerDetectionService
from src.stutter_detector.modules.repeated_words_detection_module import RepeatedWordsDetectionService
class DetectorService:
    def __init__(self):
        pass
        self.block_detection_service = BlockDetectionService()
        self.prolongation_detection_service = ProlongationDetectionService()
        self.repeated_syllables_detection_service = RepeatedSyllablesDetectionService()
        self.filler_detection_service = FillerDetectionService()
        self.repeated_words_detection_service = RepeatedWordsDetectionService()
        # Default parameters for detection
        # self.similarity_threshold = 0.98
        # self.min_repetitions = 4
        # self.min_time = 0.3
        # self.energy_threshold = 0.002
        # self.min_duration = 0.2
        # self.silent_thresh = 0.01
        # self.block_thresh = 1.0
        # self.hop_length = 512  # Default hop length for librosa

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
    
    # def detect_prolongation(self,audio, sr):
    #     """
    #     Detects prolonged segments in the audio signal based on RMS energy.
    #     Args:
    #         audio (np.ndarray): Audio signal.
    #         sr (int): Sample rate of the audio signal.
    #     Returns:
    #         list: A list of times (in seconds) where prolongations occur.
    #     """
    #     logger.info(f"[detect_prolongation] Detecting prolongations in audio...")
    #     try:
    #         hop_length = 512
    #         energy_floor = 0.01
    #         rms = librosa.feature.rms(y=audio, frame_length=2048, hop_length=hop_length).flatten()
    #         rms_diff = np.abs(np.diff(rms))
    #         rms_masked = (rms[1:] > energy_floor)
    #         logger.debug(f"[detect_prolongation] RMS shape: {rms.shape}, RMS diff shape: {rms_diff.shape}")

    #         threshold = 0.005
    #         min_frames = int((0.3 * sr) / hop_length)

    #         prolonged = (rms_diff < threshold) & rms_masked
    #         logger.debug(f"[detect_prolongation] Any prolonged frames: {np.any(prolonged)}")
    #         logger.debug(f"[detect_prolongation] Prolonged frame indices: {np.where(prolonged)[0]}")

    #         count = 0
    #         starts = []
    #         for i, val in enumerate(prolonged):
    #             if val:
    #                 count += 1
    #             else:
    #                 if count >= min_frames:
    #                     starts.append(i - count)
    #                     logger.debug(f"[detect_prolongation] Prolongation detected from frame {i - count} to {i}")
    #                 count = 0
    #         if count >= min_frames:
    #             starts.append(len(prolonged) - count)
    #             logger.debug(f"[detect_prolongation] Prolongation detected at end from frame {len(prolonged) - count}")

    #         return [librosa.frames_to_time(s, sr=sr, hop_length=hop_length).item() for s in starts]
    #     except Exception as e:
    #         logger.error(f"Error in detect_prolongation: {e}")
    #         raise HTTPException(status_code=500, detail="Error in detecting prolongations")
    
    # def detect_blocks_phoneme(self, alignment ):
    #     """
    #     Detects blocks of phonemes in the alignment data.
    #     Args:
    #         alignment (list): List of words with start and end times.
    #     Returns:
    #         list: A list of blocks with start, end, and duration.

    #     """
    #     logger.info(f"[detect_blocks_phoneme] Detecting blocks of phonemes...")
    #     try:
    #         block_thresh=0.15
    #         blocks = []
    #         prev_end = 0
    #         for word in alignment:
    #             start = float(word['start'])
    #             if start - prev_end > block_thresh:
    #                 blocks.append({
    #                 "start": prev_end,
    #                 "end": start,
    #                 "duration": start - prev_end
    #             })
    #             prev_end = float(word['end'])
    #         logger.info(f"[detect_blocks_phoneme] Block detection completed")
    #         return blocks
    #     except Exception as e:
    #         logger.error(f"[detect_blocks_phoneme] Error in detect_blocks_phoneme: {e}")
    #         raise HTTPException(status_code=500, detail="Error in detecting blocks of phonemes")
        
    
    # async def repeatedWords(self,transcript):
    #     """
    #     Detects repeated words in the transcript.
    #     Args:
    #         transcript (str): The transcript text.
    #     Returns:
    #         list: A list of repeated words found in the transcript.
    #     """
    #     logger.info(f"[repeatedWords] Detecting repeated words in transcript...")
    #     max_retries = 2
    #     for attempt in range(max_retries):
    #         try:
    #             repeated_words = re.findall(r'\b(\w+)(?:[ -]+\1\b)+', transcript.lower())
    #             break
    #         except Exception as e:
    #             if attempt < max_retries - 1:
    #                 logger.info(f"[repeatedWords] Retrying recording in 5 seconds...")
    #                 await asyncio.sleep(5)

    #             else:
    #                 repeated_words = None
    #     logger.info(f"[repeatedWords] Repeated words detection completed")
    #     return repeated_words

    # def fillers(self,transcript):
    #     """
    #     Detects fillers in the transcript.
    #     Args:
    #         transcript (str): The transcript text.
    #     Returns:
    #         list: A list of fillers found in the transcript.
    #     """
    #     logger.info(f"[fillers] Detecting fillers in transcript...")
    #     max_retries = 2
    #     for attempt in range(max_retries):
    #         try:
    #             fillers = re.findall(r'\b(um+|uh+|er+|ah+)\b', transcript.lower())
    #             break
    #         except Exception as e:
    #             if attempt < max_retries - 1:
    #                 logger.info(f"[fillers] Retrying recording in 5 seconds...")
    #                 asyncio.sleep(5)
    #             else:
    #                 logger.error(f"[fillers] Fillers detection failed: {e}")
    #                 logger.error(traceback.format_exc())
    #                 fillers = None
    #     logger.info(f"[fillers] Fillers detection completed")
    #     return fillers
    async def detect_stutters(self,audio, transcription, sr, alignment,mfcc):
        """
        Detects stutters in the audio file based on the transcription, alignment, and MFCC features.
        Args:
            audio (str): Path to the audio file.
            transcription (str): The transcription text.
            sr (int): Sample rate of the audio file.
            alignment (list): Word alignment data.
            mfcc (np.ndarray): MFCC features of the audio signal.
        Returns:
            dict: A dictionary containing the results of stutter detection, including repeated words, blocks, fillers, repeated syllables, and prolongations.
        """
        logger.info(f"[detect_stutters] Starting stutter detection...")
        try:
            # Detect repeated words
            repeated_words = await self.repeated_words_detection_service.repeatedWords(transcription)
            blocks = self.block_detection_service.detect_energy_blocks(audio,alignment,sr)
            fillers = self.filler_detection_service.fillers(transcription)
            repeated_syllables = self.repeated_syllables_detection_service.detect_repetitions(sr, mfcc)
            prolongations = self.prolongation_detection_service.detect_prolongation(audio, sr)
            result = {
                "repeated_words": repeated_words,
                "blocks": blocks,
                "fillers": fillers,
                "repeated_syllables": repeated_syllables,
                "prolongations": prolongations
            }
            logger.info(f"[detect_stutters] Stutter detection completed successfully.")
            return result
        except Exception as e:
            logger.error(f"[detect_stutters] Stutter detection failed: {e}")
            logger.error(traceback.format_exc())
            raise HTTPException(status_code=500, detail="Stutter detection failed")

