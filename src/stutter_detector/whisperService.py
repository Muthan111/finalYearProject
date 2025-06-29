import asyncio
# import whisper
import re
from faster_whisper import WhisperModel
from src.utils.logger import logger
import traceback
from fastapi import HTTPException
class WhisperService:

    def __init__(self):
        logger.info("Whisper Service initialized.")
        self.result = None
        self.model = WhisperModel("medium.en", device="cpu", compute_type="int8")
        self.language = "en"
        self.initial_prompt = "uh um like you know so"

    
    async def transcribe(self, audio_file):
        logger.info(f"Transcribing audio file")
        await asyncio.sleep(0)
        max_retries = 2
        for attempt in range(max_retries):
            try: 
                segments, info = self.model.transcribe(
                audio_file,
                language=self.language,
                initial_prompt=self.initial_prompt,
                word_timestamps=True
            )

                full_text = ""
                word_timestamps = []

                for segment in segments:
                    full_text += segment.text + " "
                    if segment.words:  # only if words are available
                        for word in segment.words:
                            word_timestamps.append({
                                "word": word.word.strip(),
                                "start": float(word.start),
                                "end": float(word.end)
                            })

                logger.info("Transcription completed successfully.")
                
                return {
                        "text": full_text.strip(),
                        "words": word_timestamps
                    }
                
                
            
            except Exception as e:
                logger.error(f"Transcription failed: {e}")
                logger.error(traceback.format_exc())
                if attempt < max_retries - 1:
                    logger.info(f"Retrying transcription in 5 seconds...")
                    await asyncio.sleep(5)  # Wait for 5 seconds before retrying
                else:
                    logger.error("Transcription failed after multiple attempts.")
                    logger.error(traceback.format_exc())
                    transcription = None
                    raise HTTPException(status_code=500, detail="Transcription failed")
            
                    
        
        
        
        
    
    