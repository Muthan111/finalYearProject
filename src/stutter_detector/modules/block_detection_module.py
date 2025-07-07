import re
import asyncio
import traceback
from src.utils.logger import logger
from fastapi import HTTPException
class BlockDetectionService:
    def __init__(self):
        pass 

    def detect_blocks_phoneme(self, alignment ):
        """
        Detects blocks of phonemes in the alignment data.
        Args:
            alignment (list): List of words with start and end times.
        Returns:
            list: A list of blocks with start, end, and duration.

        """
        logger.info(f"[detect_blocks_phoneme] Detecting blocks of phonemes...")
        try:
            block_thresh=0.15
            blocks = []
            prev_end = 0
            for word in alignment:
                start = float(word['start'])
                if start - prev_end > block_thresh:
                    blocks.append({
                    "start": prev_end,
                    "end": start,
                    "duration": start - prev_end
                })
                prev_end = float(word['end'])
            logger.info(f"[detect_blocks_phoneme] Block detection completed")
            return blocks
        except Exception as e:
            logger.error(f"[detect_blocks_phoneme] Error in detect_blocks_phoneme: {e}")
            raise HTTPException(status_code=500, detail="Error in detecting blocks of phonemes")