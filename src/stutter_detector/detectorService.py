import logging
from fastapi import HTTPException
from src.stutter_detector.microphoneService import MicrophoneService
from src.stutter_detector.audioCleanService import AudioCleanService
from src.stutter_detector.audioAnalysisService import audioAnalysisService
from src.stutter_detector.whisperService import WhisperService
from src.stutter_detector.feedbackService import FeedbackService
from src.stutter_detector.mockComponentsService import MockComponentsService
import asyncio
import traceback

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

    async def start_microphone_service(self):
        max_retries = 2
        for attempt in range(max_retries):
            try:
                logger.info("starting stutter detection...")
                logger.info("Recording")
                raw_audio = await self.microphone_service.start_recording()  
                logger.info("Recording stopped")
                break
            except Exception as e:
                logger.error(f"Error in recording audio function: {e}")
                if attempt < max_retries - 1:
                    logger.info(f"Retrying recording in 5 seconds...")
                    await asyncio.sleep(5)  # Wait for 5 seconds before retrying
                else:
                    raise HTTPException(status_code=500, detail="Error in recording audio function")
        recorded_audio = raw_audio["audiofilepath"]
        return recorded_audio
    async def audioCleaning_service(self, audioPath):
        try: 
            logger.info("Cleaning audio...")
            cleaned_audio = await self.audio_clean_service.preprocess_audio(audioPath)
            logger.info("Cleaning done")
            return cleaned_audio["processedAudio"]["filepath"]
        except Exception as e:
            logger.error(f"Audio cleaning failed: {e}")
            logger.error(traceback.format_exc())
            raise HTTPException(status_code=500, detail="Audio cleaning failed")
    
    async def audioTranscription_service(self, audioPath):
        max_retries = 2
        for attempt in range(max_retries):
            try: 
                logger.info("Transcribing audio...")
                transcription = await self.whisper_service.transcribe(audioPath)
                logger.info("Transcription done")
                break
            except Exception as e:
                logger.error(f"Transcription failed: {e}")
                logger.error(traceback.format_exc())
                if attempt < max_retries - 1:
                    logger.info(f"Retrying recording in 5 seconds...")
                    await asyncio.sleep(5)  # Wait for 5 seconds before retrying
                else:
                    raise HTTPException(status_code=500, detail="Error in recording audio function")
        transcribedText = transcription
        return transcribedText
    async def detect_fillers(self, transcription):
        max_retries = 2
        for attempt in range(max_retries):
            try:
                fillers = self.whisper_service.fillers(transcription)
                break
            except Exception as e:
                if attempt < max_retries - 1:
                    logger.info(f"Retrying recording in 5 seconds...")
                    await asyncio.sleep(5)  # Wait for 5 seconds before retrying
                else:
                    fillers = None
        fillers_detected = fillers
        return fillers_detected
    
    async def detectRepeatedWords(self, transcription):
        max_retries = 2
        for attempt in range(max_retries):
            try:
                repeatedWords = self.whisper_service.repeatedWords(transcription)
                break
            except Exception as e:
                if attempt < max_retries - 1:
                    logger.info(f"Retrying recording in 5 seconds...")
                    await asyncio.sleep(5)

                else:
                    repeatedWords = None
        repeatedWords_detected = repeatedWords
        return repeatedWords_detected
                    



    # async def detect_stutter(self):
    #     # ===================
    #     # Audio input 
    #     # ===================    
    #     max_retries = 2
    #     for attempt in range(max_retries):
    #         try:
    #             logger.info("starting stutter detection...")
    #             logger.info("Recording")
    #             raw_audio = await self.microphone_service.start_recording()  
    #             logger.info("Recording stopped")
    #             break
    #         except Exception as e:
    #             logger.error(f"Error in recording audio function: {e}")
    #             if attempt < max_retries - 1:
    #                 logger.info(f"Retrying recording in 5 seconds...")
    #                 await asyncio.sleep(5)  # Wait for 5 seconds before retrying
    #             else:
    #                 raise HTTPException(status_code=500, detail="Error in recording audio function")

    #     audioPath = raw_audio["audiofilepath"]

    #     # ===================
    #     # Audio Cleaning 
    #     # ===================
    #     # logger.info()
    #     try: 
    #         logger.info("Cleaning audio...")
    #         cleaned_audio = await self.audio_clean_service.preprocess_audio(audioPath)
    #         logger.info("Cleaning done")
    #     except Exception as e:
    #         logger.error(f"Audio cleaning failed: {e}")
    #         logger.error(traceback.format_exc())
    #         raise HTTPException(status_code=500, detail="Audio cleaning failed")


    #     # ===================
    #     # Audio Transcription 
    #     # =================== 
    #     # logger.info()
    #     for attempt in range(max_retries):
    #         try: 
    #             logger.info("Transcribing audio...")
    #             transcription = await self.whisper_service.transcribe(raw_audio["audiofilepath"])
    #             logger.info("Transcription done")
    #             break
    #         except Exception as e:
    #             logger.error(f"Transcription failed: {e}")
    #             logger.error(traceback.format_exc())
    #             if attempt == max_retries - 1:
    #             # fallback: partial result
    #                 logger.warning("Transcription failed after retries. Returning partial results.")
    #                 return {
    #                     "repetitions": [],
    #                     "blocks": [],
    #                     "prolongations": [],
    #                     "transcription": None,
    #                     "fillers": [],
    #                     "repeated_words": []
    #                 }
            
        

        


        # ===================
        # Audio Analysis 
        # ===================
        # logger.info
        # try: 
        #     logger.info("Analysing Audio")
        #     mfccFeatures = await self.audio_analysis_service.extractMFCC(cleaned_audio["cleanedAudio"], cleaned_audio["sr"])
            
            
        # except Exception as e:
        #     logger.error(f"MFCC extraction failed: {e}")
        

        # ===================
        # Feature detection
        # ===================
        # logger.info
        # logger.info("Detecting Stutters...")
        # repetitions = self.audio_analysis_service.detect_repetitions(mfccFeatures["sr"], mfccFeatures["mfcc"])
        # prolongations = self.audio_analysis_service.detect_prolongation(cleaned_audio["cleanedAudio"], cleaned_audio["sr"])
        # blocks = self.audio_analysis_service.detect_block(cleaned_audio["cleanedAudio"], cleaned_audio["sr"])
        # repeatedWords = self.whisper_service.repeatedWords(transcription)
        # fillers = self.whisper_service.fillers(transcription)
        # logger.info("detection done")
        # # logger.info

        # # 
        # return {
        #     "repetitions": repetitions,
        #     "blocks": blocks,
        #     "prolongations": prolongations,
        #     "transcription": transcription,
        #     "fillers": fillers,
        #     "repeated_words": repeatedWords
        # }
        
        
    # logger.info(" displaying results now")
        # self.feedback.repetions_feedback(repetitions)
        # self.feedback.blocks_feedback(blocks)
        # self.feedback.prolongations_feedback(prolongations)
        # self.feedback.repeated_words_feedback(repeatedWords)
        # self.feedback.fillers_feedback(fillers)

    async def detect_stutter(self):
        #  ===================
        # Audio input 
        # ===================    
        audio = await self.start_microphone_service()
        print(audio)

        cleaned_audio = await self.audioCleaning_service(audio)
        print(cleaned_audio)
        transcription = await self.audioTranscription_service(audio)
        print(transcription)
        fillers = await self.detect_fillers(transcription)
        print(fillers)
        repeatedWords = await self.detectRepeatedWords(transcription)
        print(repeatedWords)
        # ===================
        # Audio Cleaning 
        # ===================
        # logger.info()
        # logger.info("Cleaning audio...")
        # cleaned_audio = await self.audio_clean_service.preprocess_audio(raw_audio["audiofilepath"])
        # if not cleaned_audio:
        #     raise HTTPException(status_code=400, detail="Error in cleaning audio function")
        # logger.info("Cleaning done")

        # ===================
        # Audio Transcription 
        # =================== 
        # logger.info()
        # logger.info("Transcribing audio from raw audio...")
        # transcription = await self.whisper_service.transcribe(raw_audio["audiofilepath"])
        # if not transcription:
        #     raise HTTPException(status_code=400, detail="Error in transcribing audio function")
        # logger.info("Transcription donw")

        # logger.info("Transcribing audio from clean audio...")
        # transcriptionCleaned = await self.whisper_service.transcribe(cleaned_audio["processedAudio"]["filepath"])
        # if not transcription:
        #     raise HTTPException(status_code=400, detail="Error in transcribing audio function")
        # logger.info("Transcription donw")

        # mockAudioProcessing = self.MockComponents.MockAudioProcessing()
        # mockAudioAnalysis = self.MockComponents.MockAudioAnalysis()
        # mockRepetitionDetection = self.MockComponents.MockRepetitionDetection()
        # mockProlongationDetection = self.MockComponents.MockProlongationDetection()
        # mockStutterDetection = self.MockComponents.MockStutterDetection()
        # mockStutterAnalysis = self.MockComponents.MockStutterAnalysis()
        # mockStutterReport = self.MockComponents.MockStutterReport()
        # # mockFeedback = self.MockComponents.MockFeedback()

        # print("Mock components initialized successfully")
        # return {
        #     "Microphone": raw_audio,
        #     "AudioProcessing": cleaned_audio["processedAudio"]["filepath"],
        #     "rawAudioTranscription": transcription,
        #     "cleanedAudioTranscription": transcriptionCleaned,
        #     # "mockFeedback": mockFeedback
        # }