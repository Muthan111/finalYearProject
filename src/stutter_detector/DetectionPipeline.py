
from src.stutter_detector.detector_service import DetectorService

class DetectionPipeline:
    def __init__(self):
       
        self.detector_service = DetectorService()

    async def run_pipeline(self, audio_path, sr,transcription,alignment,mfcc):

        # Step 1: Analyze the audio
        
        # Step 2: Detect stutter using the detector service
        detection= await self.detector_service.detect_stutters(
            audio=audio_path,
            transcription=transcription,
            sr=sr,
            alignment=alignment,
            mfcc=mfcc
        )
        return detection