import re
import asyncio
import traceback
from src.utils.logger import logger


class FillerDetectionService:
    def __init__(self):
        pass

    def fillers(self, transcript):
        """
        Detects fillers in the transcript.
        Args:
            transcript (str): The transcript text.
        Returns:
            list: A list of fillers found in the transcript.
        """
        logger.info("[fillers] Detecting fillers in transcript...")
        max_retries = 2
        for attempt in range(max_retries):
            try:
                fillers = re.findall(
                    r"\b(um+|uh+|er+|ah+)\b", transcript.lower()
                )
                break
            except Exception as e:
                if attempt < max_retries - 1:
                    logger.info("[fillers] Retrying recording in 5 seconds...")
                    asyncio.sleep(5)
                else:
                    logger.error(f"[fillers] Fillers detection failed: {e}")
                    logger.error(traceback.format_exc())
                    fillers = None
        logger.info("[fillers] Fillers detection completed")
        return fillers
