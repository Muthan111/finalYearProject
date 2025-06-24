import logging
from fastapi import HTTPException
from src.stutter_detector.microphoneService import MicrophoneService
from src.stutter_detector.audioCleanService import AudioCleanService
from src.stutter_detector.audioAnalysisService import audioAnalysisService
from src.stutter_detector.whisperService import WhisperService
from src.stutter_detector.feedbackService import FeedbackService
from src.stutter_detector.mockComponentsService import MockComponentsService

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    filename="detector.log",  # Log output will go to detector.log in the current directory
    filemode="w"
)
logger = logging.getLogger(__name__)


class DetectorService:
    def __init__(self):
        self.result = None
        self.microphone_service = MicrophoneService()
        self.audio_clean_service = AudioCleanService()
        self.audio_analysis_service = audioAnalysisService()
        self.whisper_service = WhisperService()
        self.feedback = FeedbackService()
        self.MockComponents = MockComponentsService()
        self.language = "en"
    
    async def detect_stutter(self):
        # ===================
        # Audio input 
        # ===================    
        logger.info("starting stutter detection...")
        logger.info("Recording")
        raw_audio = await self.microphone_service.start_recording()  
        if not raw_audio:
            raise HTTPException(status_code=400, detail="Error in recording audio function")
        logger.info("Recording stopped")

        # ===================
        # Audio Cleaning 
        # ===================
        # logger.info()
        logger.info("Cleaning audio...")
        cleaned_audio = await self.audio_clean_service.preprocess_audio(raw_audio["audiofilepath"])
        if not cleaned_audio:
            raise HTTPException(status_code=400, detail="Error in cleaning audio function")
        logger.info("Cleaning done")
        # ===================
        # Audio Transcription 
        # =================== 
        # logger.info()
        logger.info("Transcribing audio...")
        transcription = await self.whisper_service.transcribe(raw_audio["audiofilepath"])
        if not transcription:
            raise HTTPException(status_code=400, detail="Error in transcribing audio function")
        logger.info("Transcription donw")

        


        # ===================
        # Audio Analysis 
        # ===================
        # logger.info
        logger.info("Analysing Audio")
        mfccFeatures = await self.audio_analysis_service.extractMFCC(cleaned_audio["cleanedAudio"], cleaned_audio["sr"])
        if not mfccFeatures:
            raise HTTPException(status_code=400, detail="Error in extracting MFCC features function")

        # ===================
        # Feature detection
        # ===================
        # logger.info
        logger.info("Detecting Stutters...")
        repetitions = self.audio_analysis_service.detect_repetitions(mfccFeatures["sr"], mfccFeatures["mfcc"])
        prolongations = self.audio_analysis_service.detect_prolongation(cleaned_audio["cleanedAudio"], cleaned_audio["sr"])
        blocks = self.audio_analysis_service.detect_block(cleaned_audio["cleanedAudio"], cleaned_audio["sr"])
        repeatedWords = self.whisper_service.repeatedWords(transcription)
        fillers = self.whisper_service.fillers(transcription)
        logger.info("detection done")
        # logger.info

        # 
        return {
            "repetitions": repetitions,
            "blocks": blocks,
            "prolongations": prolongations,
            "transcription": transcription,
            "fillers": fillers,
            "repeated_words": repeatedWords
        }
        
        
    # logger.info(" displaying results now")
        # self.feedback.repetions_feedback(repetitions)
        # self.feedback.blocks_feedback(blocks)
        # self.feedback.prolongations_feedback(prolongations)
        # self.feedback.repeated_words_feedback(repeatedWords)
        # self.feedback.fillers_feedback(fillers)

    # async def detect_stutter(self):
    #     #  ===================
    #     # Audio input 
    #     # ===================    
    #     logger.info("starting stutter detection...")
    #     logger.info("Recording")
    #     raw_audio = await self.microphone_service.start_recording()  
    #     if not raw_audio:
    #         raise HTTPException(status_code=400, detail="Error in recording audio function")
    #     logger.info("Recording stopped")

    #     # ===================
    #     # Audio Cleaning 
    #     # ===================
    #     # logger.info()
    #     logger.info("Cleaning audio...")
    #     cleaned_audio = await self.audio_clean_service.preprocess_audio(raw_audio["audiofilepath"])
    #     if not cleaned_audio:
    #         raise HTTPException(status_code=400, detail="Error in cleaning audio function")
    #     logger.info("Cleaning done")

    #     # ===================
    #     # Audio Transcription 
    #     # =================== 
    #     # logger.info()
    #     logger.info("Transcribing audio from raw audio...")
    #     transcription = await self.whisper_service.transcribe(raw_audio["audiofilepath"])
    #     if not transcription:
    #         raise HTTPException(status_code=400, detail="Error in transcribing audio function")
    #     logger.info("Transcription donw")

    #     logger.info("Transcribing audio from clean audio...")
    #     transcriptionCleaned = await self.whisper_service.transcribe(cleaned_audio["processedAudio"]["filepath"])
    #     if not transcription:
    #         raise HTTPException(status_code=400, detail="Error in transcribing audio function")
    #     logger.info("Transcription donw")

    #     mockAudioProcessing = self.MockComponents.MockAudioProcessing()
    #     mockAudioAnalysis = self.MockComponents.MockAudioAnalysis()
    #     mockRepetitionDetection = self.MockComponents.MockRepetitionDetection()
    #     mockProlongationDetection = self.MockComponents.MockProlongationDetection()
    #     mockStutterDetection = self.MockComponents.MockStutterDetection()
    #     mockStutterAnalysis = self.MockComponents.MockStutterAnalysis()
    #     mockStutterReport = self.MockComponents.MockStutterReport()
    #     # mockFeedback = self.MockComponents.MockFeedback()

    #     print("Mock components initialized successfully")
    #     return {
    #         "Microphone": raw_audio,
    #         "AudioProcessing": cleaned_audio["processedAudio"]["filepath"],
    #         "rawAudioTranscription": transcription,
    #         "cleanedAudioTranscription": transcriptionCleaned,
    #         # "mockFeedback": mockFeedback
    #     }