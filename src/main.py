from fastapi import FastAPI,Request
# from src.calculator.router import calculator_router
from src.whisperAi.router import whisper_router
from src.stutter_detector.router import stutter_router
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
templates = Jinja2Templates(directory="frontend")
app = FastAPI(
    title="Stutter Detection API",
    description="API for detecting stutter in audio files using Whisper AI and custom stutter detection logic.",
    version="1.0.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.include_router(whisper_router)
app.include_router(stutter_router)
@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})