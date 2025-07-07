from src.stutter_detector.modules.whisper_module import WhisperService
from src.utils.logger import logger
import traceback
class TranscribePipeline:
    def __init__(self):
        logger.info(f"[TranscribePipeline] Transcription Pipeline initialized.")
        self.whisper_service = WhisperService()

    async def run_pipeline(self, file):
        """
        Runs the transcription pipeline:
        1. Transcribes the audio file using the Whisper service.
        2. Returns the text transcription and word alignment.
        """
        logger.info("Running transcription pipeline")
        try:
            transcription = await self.whisper_service.transcribe(file)
            text_transcription = transcription['text']
            alignment = transcription["words"]
            if "error" in transcription:
                return {"error": transcription["error"]}

            
            logger.info("Transcription completed successfully.")
            return {
                "text_transcription": text_transcription,
                "alignment": alignment
            }
        
        except Exception as e:
            logger.error(f"Error in TranscribePipeline: {e}")
            logger.error(traceback.format_exc())
            return {"error": "Transcription failed"}