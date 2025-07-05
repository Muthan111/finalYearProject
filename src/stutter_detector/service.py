import logging
from fastapi import HTTPException
from src.stutter_detector.microphoneService import MicrophoneService
from src.stutter_detector.audioCleanService import AudioCleanService
from src.stutter_detector.audioAnalysisService import AudioAnalysisService
from src.stutter_detector.whisperService import WhisperService
from src.stutter_detector.feedbackService import FeedbackService
from src.stutter_detector.detector_service import DetectorService
from src.stutter_detector.UploadService import UploadService
import asyncio
import traceback
from src.utils.logger import logger
# testing blocks here



class stutterDetectorService:
    def __init__(self):
        self.result = None
        self.microphone_service = MicrophoneService()
        self.audio_clean_service = AudioCleanService()
        self.audio_analysis_service = AudioAnalysisService()
        self.whisper_service = WhisperService()
        self.feedback = FeedbackService()
        self.detector_service = DetectorService()
        self.upload_service = UploadService()
        self.language = "en"

    
    
    
   
    
    
    
    




    async def detect_stutter(self,file):
        # ===================
        # clear previous feedback
        # ===================
        self.feedback.clear_feedback()
        #  ===================
        # Start Microphone 
        # ===================    
        # audio = await self.microphone_service.start_recording()
        # audioPath = audio["audiofilepath"]
        # audioDisplayURL = audio["audioDisplayURL"]

        audio =  self.upload_service.audio_upload(file)
        if "error" in audio:
            raise HTTPException(status_code=500, detail=audio["error"])
        audioPath = audio["filepath"]
        audioDisplayURL = audio["audioDisplayURL"]

        # ===================
        # Clean Audio
        # ===================
        cleaned_audio = await self.audio_clean_service.preprocess_audio(audioPath)
        cleanedAudioPath = cleaned_audio["cleanedAudio"]
        sr = cleaned_audio["sr"]

        # # ===================
        # # Transcribe Audio
        # # ===================
        transcription = await self.whisper_service.transcribe(audioPath)
        text_transcription = transcription["text"]
        alignment = transcription["words"]

        # ===================
        # Extract MFCC
        # ===================
        mfcc = await self.audio_analysis_service.extractMFCC(cleanedAudioPath, sr)
        extracted_mfcc = mfcc["mfcc"]
        sr = mfcc["sr"]
        
        # ===================
        # Detect Stutters
        # ===================
        detection= await self.detector_service.detect_stutters(
            audio=cleanedAudioPath,
            transcription=text_transcription,
            sr=sr,
            alignment=alignment,
            mfcc=extracted_mfcc
        )
        data = {
            
            "transcription": transcription['text'],
            
            "detection": detection,
            "audioDisplayURL": audioDisplayURL
        }
        return data
        # final_result = self.feedback.personalized_feedback(detection)
        # return final_result
    def test_upload(self, file):
        try:
            upload_result = self.upload_service.audio_upload(file)
            if "error" in upload_result:
                raise HTTPException(status_code=500, detail=upload_result["error"])
            return upload_result
        except Exception as e:
            logger.error(f"Error in file upload: {e}")
            logger.error(traceback.format_exc())
            raise HTTPException(status_code=500, detail=str(e))

        
        
        

        
        