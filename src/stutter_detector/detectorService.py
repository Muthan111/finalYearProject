from fastapi import HTTPException
from src.stutter_detector.microphoneService import MicrophoneService
from src.stutter_detector.audioCleanService import AudioCleanService
from src.stutter_detector.audioAnalysisService import audioAnalysisService
from src.stutter_detector.whisperService import WhisperService
class DetectorService:
    def __init__(self):
        self.result = None
        self.microphone_service = MicrophoneService()
        self.audio_clean_service = AudioCleanService()
        self.audio_analysis_service = audioAnalysisService()
        self.whisper_service = WhisperService()
        self.language = "en"
    
    async def detect_stutter(self):
        print("starting stutter detection...")
        print()
        raw_audio = await self.microphone_service.start_recording()  # Example usage
        if not raw_audio:
            raise HTTPException(status_code=400, detail="Error in recording audio function")
        
        print()
        print("Transcribing audio...")
        transcription = await self.whisper_service.transcribe(raw_audio["audiofilepath"])
        print()
        print("Cleaning audio...")
        cleaned_audio = await self.audio_clean_service.preprocess_audio(raw_audio["audiofilepath"])

        print()
        print("Analysing Audio")
        mfccFeatures = await self.audio_analysis_service.extractMFCC(cleaned_audio["cleanedAudio"], cleaned_audio["sr"])

        print()
        print("Detecting Stutters...")
        repetitions = self.audio_analysis_service.detect_repetitions(mfccFeatures["sr"], mfccFeatures["mfcc"])
        prolongations = self.audio_analysis_service.detect_prolongation(cleaned_audio["cleanedAudio"], cleaned_audio["sr"])
        blocks = self.audio_analysis_service.detect_block(cleaned_audio["cleanedAudio"], cleaned_audio["sr"])
        repeatedWords = self.whisper_service.repeatedWords(transcription)
        fillers = self.whisper_service.fillers(transcription)
        return {
            "repetitions": repetitions,
            "prolongations": prolongations,
            "blocks": blocks,
            "transcription": transcription,
            "repeatedWords": repeatedWords,
            "fillers": fillers,
        }
        
    