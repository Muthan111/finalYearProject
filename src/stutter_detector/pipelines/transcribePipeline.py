from src.stutter_detector.component_services.whisper_service import WhisperService
from src.utils.logger import logger
import traceback
class TranscribePipeline:
    def __init__(self):
        logger.info(f"[TranscribePipeline] Transcription Pipeline initialized.")
        self.whisper_service = WhisperService(use_gradio= False)

    async def run_pipeline(self, file):
        """
        Runs the transcription pipeline:
        1. Transcribes the audio file using the Whisper service.
        2. Returns the text transcription and word alignment.
        """
        logger.info("Running transcription pipeline")
        try:
            # transcription =  self.whisper_service.transcribe_gradio(file)
            transcription = await self.whisper_service.transcribe(file)
            if "error" in transcription:
                logger.error(f"Transcription error: {transcription['error']}")
                return {"error": transcription["error"]}
            text_transcription = transcription['text']
            alignment = transcription["words"]
            

            
            logger.info("Transcription completed successfully.")
            return {
                "text_transcription": text_transcription,
                "alignment": alignment
            }
        
        except Exception as e:
            logger.error(f"Error in TranscribePipeline: {e}")
            logger.error(traceback.format_exc())
            return {"error": "Transcription failed"}
        

    # def run_pipelineV2(self, file):
    #     """
    #     Runs the transcription pipeline:
    #     1. Transcribes the audio file using the Whisper service.
    #     2. Returns the text transcription and word alignment.
    #     """
    #     logger.info("Running transcription pipeline")
    #     try:
    #         transcription =  self.whisper_service.transcribe_gradio(file)
    #         # transcription = await self.whisper_service.transcribe(file)
    #         if "error" in transcription:
    #             logger.error(f"Transcription error: {transcription['error']}")
    #             return {"error": transcription["error"]}
    #         text_transcription = transcription['transcription']
    #         alignment = transcription["word_timestamps"]
            

            
    #         logger.info("Transcription completed successfully.")
    #         return {
    #             "text_transcription": text_transcription,
    #             "alignment": alignment
    #         }
        
    #     except Exception as e:
    #         logger.error(f"Error in TranscribePipeline: {e}")
    #         logger.error(traceback.format_exc())
    #         return {"error": "Transcription failed"}