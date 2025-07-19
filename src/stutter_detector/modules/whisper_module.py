import asyncio
# import whisper
import re
from faster_whisper import WhisperModel
from src.utils.logger import logger
import traceback
from fastapi import HTTPException
from gradio_client import Client, file
import sys
import os

# Add the absolute path of the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../..")))
class WhisperService:

    def __init__(self):
        self.gradio_url = "https://e17585dab19812bc55.gradio.live"
        self.client = Client(self.gradio_url)
        self.result = None
        self.model = WhisperModel("medium.en", device="cpu", compute_type="int8")
        self.language = "en"
        self.initial_prompt = "uh um like you know so"
        self.beam_size = 5
        self.temperature = [0.0, 0.2, 0.4]
    # def transcribe_gradio(self,audio_path):
    #     try:
    #         audio = file(audio_path)
    #         segments = self.client.predict(audio, api_name="/predict")  # Expecting list of segments from Colab
    #         logger.info(f"[transcribe_gradio function] Received segments: {segments}")
    #         print("type of segments:", type(segments))
    #         print (type(segments))
    #         full_text = ""
    #         word_timestamps = []

    #         for segment in segments:
    #             full_text += segment.get("text", "") + " "
                
    #             if "words" in segment and segment["words"]:
    #                 for word in segment["words"]:
    #                     word_timestamps.append({
    #                         "word": word.get("word", "").strip(),
    #                         "start": float(word.get("start", 0)),
    #                         "end": float(word.get("end", 0))
    #                     })

    #         print(f"Full Transcription: {full_text.strip()}")
    #         print(f"Word Timestamps: {word_timestamps}")
    #         return {
    #             "transcription": full_text.strip(),
    #             "word_timestamps": word_timestamps
    #         }

    #     except Exception as e:
    #         logger.error(f"[transcribe_gradio function] Transcription failed: {e}")
    #         logger.error(traceback.format_exc())
    #         return {"error": f"Transcription failed: {str(e)}"}

    
    async def transcribe(self, audio_file):
        logger.info(f"[transcribe function] Transcribing audio file")
        await asyncio.sleep(0)
        max_retries = 2
        for attempt in range(max_retries):
            try: 
                segments, info =  self.model.transcribe(
                audio_file,
                language=self.language,
                initial_prompt=self.initial_prompt,
                word_timestamps=True,
                beam_size=self.beam_size,
                temperature=self.temperature
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

                
                
                return {
                        "text": full_text.strip(),
                        "words": word_timestamps
                    }
                
                
            
            except Exception as e:
                logger.error(f"[transcribe function] Transcription failed: {e}")
                logger.error(traceback.format_exc())
                if attempt < max_retries - 1:
                    logger.info(f"[transcribe function] Retrying transcription in 5 seconds...")
                    await asyncio.sleep(5)  # Wait for 5 seconds before retrying
                else:
                    logger.error(f"[transcribe function] Transcription failed after multiple attempts.")
                    logger.error(traceback.format_exc())
                    segments = None
                    raise HTTPException(status_code=500, detail="Transcription failed")


        
        
        
        
    
    