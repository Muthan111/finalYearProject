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
            return {
                "audioPath":cleaned_audio["cleanedAudio"],
                "sr": cleaned_audio["sr"],
            }
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
                    
    async def detectRepeatedSyllables(self, audio,sr):
        try:
            mfcc = await self.audio_analysis_service.extractMFCC(audio,sr)
            repeatedSyllables = self.audio_analysis_service.detect_repetitions(mfcc["sr"], mfcc["mfcc"])
            return repeatedSyllables
        except Exception as e:
            logger.error(f"Repeated syllables detection failed: {e}")
            repeatedSyllables = None
            return repeatedSyllables
    def detectProlongation(self, audio, sr):
        try:
            prolongations = self.audio_analysis_service.detect_prolongation(audio, sr)
            return prolongations
        except Exception as e:
            logger.error(f"Prolongation detection failed: {e}")
            prolongations = None
            return prolongations
    def detectBlock(self, audio, sr):
        try:
            blocks = self.audio_analysis_service.detect_block(audio, sr)
            return blocks
        except Exception as e:
            logger.error(f"Block detection failed: {e}")
            blocks = None
            return blocks
        




    async def detect_stutter(self):
        #  ===================
        # Audio input 
        # ===================    
        audio = await self.start_microphone_service()
        print(audio)

        cleaned_audio = await self.audioCleaning_service(audio)
        print(cleaned_audio["audioPath"])
        transcription = await self.audioTranscription_service(audio)
        print(transcription)
        fillers = await self.detect_fillers(transcription)
        print(fillers)
        repeatedWords = await self.detectRepeatedWords(transcription)
        print(repeatedWords)
        cleanedAudioPath = cleaned_audio["audioPath"]
        sr = cleaned_audio["sr"]
        repeatedSyllables = await self.detectRepeatedSyllables(cleanedAudioPath, sr)
        blocks = self.detectBlock(cleanedAudioPath, sr)
        prolongations = self.detectProlongation(cleanedAudioPath, sr)
        print(f"repeatedSyllables: {repeatedSyllables}")
        print(f"blocks: {blocks}")
        print(f"prolongations: {prolongations}")
        