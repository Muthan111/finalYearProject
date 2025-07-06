from src.stutter_detector.UploadService import UploadService
from src.stutter_detector.microphoneService import MicrophoneService
from src.stutter_detector.audioCleanService import AudioCleanService

class AudioPipeline:
    def __init__(self):
        self.upload_service = UploadService()
        self.microphone_service = MicrophoneService()
        self.audio_clean_service = AudioCleanService()
        

    async def run_pipeline(self,file):
        # Step 1: Upload the audio file
        audio = self.upload_service.audio_upload(file)
        if "error" in audio:
            return {"error": audio["error"]}
        
        audio_path = audio["filepath"]
        audio_display_url = audio["audioDisplayURL"]

        # Step 2: Clean the audio
        cleaned_audio =await self.audio_clean_service.preprocess_audio(audio_path)
        if "error" in cleaned_audio:
            return {"error": cleaned_audio["error"]}
        cleaned_audio_path = cleaned_audio['cleanedAudio']
        sr = cleaned_audio['sr']

        
       
        # Return the paths and URLs
        return {
            "original_audio_path": audio_path,
            "cleaned_audio_path": cleaned_audio_path,
            "audio_display_url": audio_display_url,
            "sr": sr

        }