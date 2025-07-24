from src.stutter_detector.component_services.audio_analysis_service import AudioAnalysisService
from src.utils.logger import logger
import traceback
class MfccPipeline:
    def __init__(self):
        
        self.audio_analysis_service = AudioAnalysisService()

    async def run_pipeline(self, audio_path, sr):
        """
        Runs the MFCC feature extraction pipeline:
        1. Extracts MFCC features from the audio file.
        2. Returns the MFCC features and sample rate.
        """
        
        try:
            mfcc_features = await self.audio_analysis_service.extractMFCC(audio_path, sr)
            if "error" in mfcc_features:
                return {"error": mfcc_features["error"]}

            
            return {
                "mfcc_features": mfcc_features["mfcc"],
                "sr": sr
            }
        except Exception as e:
            logger.error(f"[MfccPipeline] Error in MFCC Pipeline: {e}")
            logger.error(traceback.format_exc())
            return {"error": "MFCC feature extraction failed"}