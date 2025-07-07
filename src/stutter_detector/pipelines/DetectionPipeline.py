
from src.stutter_detector.modules.detector_service import DetectorService
from src.utils.logger import logger
import traceback
class DetectionPipeline:
    def __init__(self):
        logger.info(f"[DetectionPipeline] Detection Pipeline initialized.")
        self.detector_service = DetectorService()

    async def run_pipeline(self, audio_path, sr,transcription,alignment,mfcc):
        """
        Runs the detection pipeline:
        1. Detects stutters in the audio file using the provided transcription, alignment,  
        and MFCC features.
        2. Returns the detection results.
        
        """
        logger.info(f"[DetectionPipeline] Running detection pipeline")
        try:
            detection= await self.detector_service.detect_stutters(
                audio=audio_path,
                transcription=transcription,
                sr=sr,
                alignment=alignment,
                mfcc=mfcc
            )
            return detection
        except Exception as e:
            logger.error(f"[DetectionPipeline] Error in DetectionPipeline: {e}")
            logger.error(traceback.format_exc())
            return {"error": "Stutter detection failed"}