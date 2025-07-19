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
            if repeated_syllables is None:
                repeated_syllables = None
            if prolongations is None:
                prolongations = None
            if blocks is None:
                blocks = None

            if repeated_words is None:
                repeated_words = None
            if fillers is None:
                fillers = None
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

