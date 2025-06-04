from fastapi import FastAPI
# from src.calculator.router import calculator_router
from src.whisperAi.router import whisper_router
from src.stutter_detector.router import stutter_router
app = FastAPI()

app.include_router(whisper_router)
app.include_router(stutter_router)