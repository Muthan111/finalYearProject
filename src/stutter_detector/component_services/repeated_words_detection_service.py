from src.utils.logger import logger
import re
import asyncio


class RepeatedWordsDetectionService:
    def __init__(self):
        pass

    async def repeatedWords(self, transcript):
        """
        Detects repeated words in the transcript.
        Args:
            transcript (str): The transcript text.
        Returns:
            list: A list of repeated words found in the transcript.
        """
        logger.info(
            "[repeatedWords] Detecting repeated words in transcript..."
        )
        max_retries = 2
        for attempt in range(max_retries):
            try:
                repeated_words = re.findall(
                    r"\b(\w+)(?:[ -]+\1\b)+", transcript.lower()
                )
                break
            except Exception as e:
                if attempt < max_retries - 1:
                    logger.info(
                        f"[repeatedWords] Retrying recording in 5 seconds {e}"
                    )
                    await asyncio.sleep(5)

                else:
                    repeated_words = None
        logger.info("[repeatedWords] Repeated words detection completed")
        return repeated_words
