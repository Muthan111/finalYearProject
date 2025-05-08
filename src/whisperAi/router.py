from fastapi import APIRouter, File, UploadFile
from fastapi.responses import HTMLResponse
whisper_router = APIRouter()
from src.whisperAi.service import WhisperAiService
whisper_service = WhisperAiService()
import os
from fastapi.responses import JSONResponse


UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
@whisper_router.get("/", response_class=HTMLResponse)
async def read_root():
    return """
    <html>
        <head>
            <title>Whisper AI</title>
        </head>
        <body>
            <h1>Welcome to the Whisper AI API</h1>
            <p>Use the endpoints to interact with the Whisper AI service.</p>
        </body>
    </html>
    """

@whisper_router.post("/upload/")
async def upload_audio(file: UploadFile = File(...)):
    try:
        # Save the uploaded file
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        with open(file_path, "wb") as f:
            f.write(await file.read())

        # Transcribe the audio file
        transcription = await whisper_service.transcribe(file_path)

        return JSONResponse(content={"message": "File uploaded successfully", "transcription": transcription})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)