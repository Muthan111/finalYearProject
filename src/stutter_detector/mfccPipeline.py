from src.stutter_detector.audioAnalysisService import AudioAnalysisService
class MfccPipeline:
    def __init__(self):
        self.audio_analysis_service = AudioAnalysisService()

    async def run_pipeline(self, audio_path, sr):
        # Step 1: Extract MFCC features from the audio file
        mfcc_features = await self.audio_analysis_service.extractMFCC(audio_path, sr)
        if "error" in mfcc_features:
            return {"error": mfcc_features["error"]}

        # Return the MFCC features
        return {
            "mfcc_features": mfcc_features["mfcc"],
            "sr": sr
        }