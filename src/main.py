from fastapi import FastAPI
# from src.calculator.router import calculator_router
from src.whisperAi.router import whisper_router
from src.stutter_detector.router import stutter_router
app = FastAPI(
    title="Stutter Detection API",
    description="API for detecting stutter in audio files using Whisper AI and custom stutter detection logic.",
    version="1.0.0",
)

app.include_router(whisper_router)
app.include_router(stutter_router)