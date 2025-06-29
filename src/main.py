from fastapi import FastAPI,Request
from src.stutter_detector.router import stutter_router
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
templates = Jinja2Templates(directory="frontend")
from fastapi.staticfiles import StaticFiles
import os
from src.middleware.loggerMiddleware import LoggingMiddleware
app = FastAPI(
    title="Stutter Detection API",
    description="API for detecting stutter in audio files using Whisper AI and custom stutter detection logic.",
    version="1.0.0",
)
app.add_middleware(LoggingMiddleware)


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RECORDING_PATH = os.path.join(BASE_DIR, 'recordings')

app.mount("/static", StaticFiles(directory=RECORDING_PATH), name="static")
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