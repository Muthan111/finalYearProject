from fastapi import FastAPI
from src.calculator.router import calculator_router
from src.whisperAi.router import whisper_router
app = FastAPI()
app.include_router(calculator_router)
app.include_router(whisper_router)