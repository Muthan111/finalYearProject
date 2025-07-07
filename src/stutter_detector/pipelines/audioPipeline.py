from src.stutter_detector.modules.Upload_module import UploadService
from src.stutter_detector.modules.microphone_module import MicrophoneService
from src.stutter_detector.modules.audio_clean_module import AudioCleanService
from src.utils.logger import logger
import traceback
class AudioPipeline:
    def __init__(self):
        
        self.upload_service = UploadService()
        self.microphone_service = MicrophoneService()
        self.audio_clean_service = AudioCleanService()
        

    async def run_pipeline(self,file):
        """
        Runs the audio processing pipeline:
        1. Uploads the audio file.
        2. Cleans the audio file.
        3. Returns the paths and URLs of the original and cleaned audio files.
        """
        logger.info(f"[AudioPipeline] Running audio pipeline")
        try: 
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
            logger.info(f"[AudioPipeline] Audio processing completed successfully.")
            return {
                "original_audio_path": audio_path,
                "cleaned_audio_path": cleaned_audio_path,
                "audio_display_url": audio_display_url,
                "sr": sr
            }
        except Exception as e:
            logger.error(f"[AudioPipeline] Error in AudioPipeline: {e}")
            logger.error(traceback.format_exc())
            return {"error": "Audio processing failed"}
        