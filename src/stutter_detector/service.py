import logging
from fastapi import HTTPException

from src.stutter_detector.component_services.feedback_service import FeedbackService

from src.stutter_detector.pipelines.audioPipeline import AudioPipeline
from src.stutter_detector.pipelines.transcribePipeline import TranscribePipeline
from src.stutter_detector.pipelines.DetectionPipeline import DetectionPipeline
from src.stutter_detector.pipelines.mfccPipeline import MfccPipeline

import asyncio
import traceback
from src.utils.logger import logger
# testing blocks here



class stutterDetectorService:
    def __init__(self):
        self.result = None
        self.language = "en"
        self.audio_pipeline = AudioPipeline()
        self.transcribe_pipeline = TranscribePipeline()
        self.detection_pipeline = DetectionPipeline()
        self.mfcc_pipeline = MfccPipeline()
        self.feedback = FeedbackService()
    async def detect_stutter(self, file):
        # ===================
        # clear previous feedback
        # ===================
        # self.feedback.clear_feedback()
        try:
            # Step 1: Upload the audio file
            self.feedback.clear_feedback()
            audio = await self.audio_pipeline.run_pipeline(file)
            if "error" in audio:
                raise HTTPException(status_code=500, detail=audio["error"])
            audioPath = audio["original_audio_path"]
            audioDisplayURL = audio["audio_display_url"]
            cleanedAudioPath = audio["cleaned_audio_path"]
            sr = audio["sr"]

            

            
            
            transcription = await self.transcribe_pipeline.run_pipeline(audioPath)
            if "error" in transcription:
                raise HTTPException(status_code=500, detail=transcription["error"])
            text_transcription = transcription["text_transcription"]
            alignment = transcription["alignment"]
            
            

            mfcc = await self.mfcc_pipeline.run_pipeline(cleanedAudioPath, sr)
            if "error" in mfcc:
                raise HTTPException(status_code=500, detail=mfcc["error"])
            mfcc_features = mfcc["mfcc_features"]
            sr1 = mfcc["sr"]
            detection = await self.detection_pipeline.run_pipeline(
                cleanedAudioPath,
                sr1,
                text_transcription,
                alignment,
                mfcc_features
            )
            general_Feedback = self.feedback.convert_feedback_to_string(
                detection["fillers"],
                detection["repeated_words"],
                detection["blocks"],
                detection["prolongations"],
                detection["repeated_syllables"]
            )
            word_and_timestamps_string = self.feedback.convert_alignment_to_string(alignment)

            personalized_feedback = self.feedback.personalized_feedback(detection)
            return {
                "transcription": text_transcription,
                "detection": general_Feedback,
                "audioDisplayURL": audioDisplayURL,
                "alignment": word_and_timestamps_string,
                "personalized_feedback": personalized_feedback
                
            }


            
        except Exception as e:
            logger.error(f"Error in detect_stutter: {e}")
            logger.error(traceback.format_exc())
            raise HTTPException(status_code=500, detail=str(e))

    
    
    
   
    
    
    
    




    

        
        
        

        
        